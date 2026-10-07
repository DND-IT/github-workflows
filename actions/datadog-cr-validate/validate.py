"""Validate Datadog Operator resources rendered from Helm charts."""

import argparse
import http.client
import json
import os
import re
import shlex
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import yaml

CRDS_CATALOGS = [
    "https://raw.githubusercontent.com/DND-IT/CRDs-catalog/main/{{.Group}}/{{.ResourceKind}}_{{.ResourceAPIVersion}}.json",
    "https://raw.githubusercontent.com/datreeio/CRDs-catalog/main/{{.Group}}/{{.ResourceKind}}_{{.ResourceAPIVersion}}.json",
]
METRIC_QUERY = re.compile(r"(?:avg|sum|min|max|count|p[0-9]+):([A-Za-z0-9_.]+)\{([^}]*)\}")
TAG_FILTER = re.compile(r"[A-Za-z][^:]*:[^*$]+")
TAG_SEPARATOR = re.compile(r"[\s,()]+")
CLAUSE_TOKEN = re.compile(r"(,|\(|\)|\sAND\s)")
TEMPLATE_VARIABLE = re.compile(r"\$([A-Za-z_][A-Za-z0-9_]*)")
CAMEL_CASE_HUMP = re.compile(r"([a-z0-9])([A-Z])")
TAG_WINDOW_SECONDS = 7 * 24 * 3600
DATADOG_ATTEMPTS = 3


def annotate(level, title, message):
    print(f"::{level} title={title}::{message}")


def manifests(rendered):
    return sorted(Path(rendered).glob("*.yaml"))


def resources(rendered, kind):
    for path in manifests(rendered):
        for doc in yaml.safe_load_all(path.read_text()):
            if isinstance(doc, dict) and doc.get("kind") == kind:
                yield doc


def strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from strings(item)


def datadog(method, path, params=None, body=None):
    url = f"https://api.{os.environ['DD_SITE']}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(
        url,
        method=method,
        data=json.dumps(body).encode() if body is not None else None,
        headers={
            "DD-API-KEY": os.environ["DD_API_KEY"],
            "DD-APPLICATION-KEY": os.environ["DD_APP_KEY"],
            "Content-Type": "application/json",
        },
    )
    for attempt in range(1, DATADOG_ATTEMPTS + 1):
        try:
            with urllib.request.urlopen(request) as response:
                return response.status, json.load(response)
        except urllib.error.HTTPError as error:
            return error.code, error.read().decode()
        except http.client.IncompleteRead:
            if attempt == DATADOG_ATTEMPTS:
                raise


def render(charts, rendered):
    Path(rendered).mkdir(parents=True, exist_ok=True)
    failed = False
    lines = [line for line in charts.splitlines() if line.strip()]
    for i, line in enumerate(lines, 1):
        chart, *args = shlex.split(line)
        name = Path(chart).name
        print(f"Rendering {line}", flush=True)
        with open(Path(rendered) / f"{i}-{name}.yaml", "w") as out:
            if subprocess.run(["helm", "template", name, chart, *args], stdout=out).returncode:
                annotate("error", f"Chart {chart}", "helm template failed")
                failed = True
    return failed


def schemas(rendered):
    locations = [arg for location in ["default", *CRDS_CATALOGS] for arg in ("-schema-location", location)]
    command = ["kubeconform", "-strict", "-summary", *locations]
    return subprocess.run([*command, *map(str, manifests(rendered))]).returncode != 0


def nested_widgets(widgets):
    for widget in widgets:
        yield widget
        yield from nested_widgets(widget.get("definition", {}).get("widgets", []))


def dashboards(rendered):
    failed = False
    for cr in resources(rendered, "DatadogDashboard"):
        name = cr["metadata"]["name"]
        title = f"DatadogDashboard {name}"
        try:
            widgets = json.loads(cr["spec"].get("widgets"))
        except (TypeError, json.JSONDecodeError):
            widgets = None
        if not isinstance(widgets, list):
            annotate("error", title, "spec.widgets is not a JSON array")
            failed = True
            continue
        untyped = sum(not isinstance(w.get("definition", {}).get("type"), str) for w in nested_widgets(widgets))
        if untyped:
            annotate("error", title, f"{untyped} widget(s) have no definition.type")
            failed = True
        declared = {variable["name"] for variable in cr["spec"].get("templateVariables") or []}
        used = {variable for text in strings(widgets) for variable in TEMPLATE_VARIABLE.findall(text)}
        if undeclared := sorted(used - declared):
            annotate("error", title, f"Undeclared template variables: {', '.join(undeclared)}")
            failed = True
        print(f"Linted dashboard {name}")
    return failed


def snake_case(value):
    if isinstance(value, dict):
        return {CAMEL_CASE_HUMP.sub(lambda m: f"{m[1]}_{m[2].lower()}", k): snake_case(v) for k, v in value.items()}
    if isinstance(value, list):
        return [snake_case(item) for item in value]
    return value


def monitor_payload(spec):
    payload = snake_case({k: v for k, v in spec.items() if k != "controllerOptions"})
    if thresholds := payload.get("options", {}).get("thresholds"):
        payload["options"]["thresholds"] = {k: float(v) for k, v in thresholds.items()}
    return payload


def monitors(rendered):
    failed = False
    for cr in resources(rendered, "DatadogMonitor"):
        name = cr["metadata"]["name"]
        status, body = datadog("POST", "/api/v1/monitor/validate", body=monitor_payload(cr["spec"]))
        if status == 200:
            print(f"Validated monitor {name}")
        else:
            annotate("error", f"DatadogMonitor {name}", f"HTTP {status}: {body}")
            failed = True
    return failed


def clauses(tags):
    clause, depth = "", 0
    for token in CLAUSE_TOKEN.split(tags):
        depth += (token == "(") - (token == ")")
        if depth == 0 and token.strip() in (",", "AND"):
            yield clause
            clause = ""
        else:
            clause += token
    yield clause


def metric_filters(rendered):
    queries = [cr["spec"].get("query") or "" for cr in resources(rendered, "DatadogMonitor")]
    queries += [cr["spec"].get("widgets") or "" for cr in resources(rendered, "DatadogDashboard")]
    filters = {}
    for query in queries:
        for metric, tags in METRIC_QUERY.findall(query):
            groups = filters.setdefault(metric, set())
            for clause in clauses(tags):
                alternatives = frozenset(t for t in TAG_SEPARATOR.split(clause) if TAG_FILTER.fullmatch(t))
                if alternatives:
                    groups.add(alternatives)
    return filters


def tags(rendered):
    failed = False
    for metric, filters in sorted(metric_filters(rendered).items()):
        params = {"window[seconds]": TAG_WINDOW_SECONDS}
        if not filters:
            params["filter[include_tag_values]"] = "false"
        try:
            status, body = datadog("GET", f"/api/v2/metrics/{metric}/all-tags", params=params)
        except http.client.IncompleteRead:
            annotate("warning", "Tag check skipped", f"{metric} tag list was cut off by the Datadog API")
            continue
        if status == 404:
            annotate("error", "Metric not found", f"{metric} has not been reported in the last 7 days")
            failed = True
            continue
        if status != 200:
            annotate("error", f"Metric {metric}", f"HTTP {status}: {body}")
            failed = True
            continue
        # Only indexed tags can be queried, so ingested_tags are deliberately not consulted. A missing value only
        # warns: tags such as reason:oomkilled legitimately appear only when the event happens.
        indexed = set(body["data"]["attributes"].get("tags") or [])
        for alternatives in sorted(filters, key=sorted):
            if not alternatives & indexed:
                tag = " OR ".join(sorted(alternatives))
                annotate("warning", "Tag value not found", f"{metric}{{{tag}}} has not been indexed in the last 7 days")
        print(f"Checked metric {metric}")
    return failed


CHECKS = {"schemas": schemas, "dashboards": dashboards, "monitors": monitors, "tags": tags}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    render_command = commands.add_parser("render", help="render Helm charts, one per line with helm template arguments")
    render_command.add_argument("charts")
    render_command.add_argument("rendered")
    for name in CHECKS:
        commands.add_parser(name).add_argument("rendered")
    args = parser.parse_args()
    failed = render(args.charts, args.rendered) if args.command == "render" else CHECKS[args.command](args.rendered)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
