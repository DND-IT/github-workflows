import io
import json
import shlex
import shutil
import subprocess
import sys
import urllib.error
from pathlib import Path

import pytest
import yaml

import validate

FIXTURES = Path(__file__).parent


def write_manifests(directory, *docs):
    (directory / "1-test.yaml").write_text(yaml.safe_dump_all(docs))


def monitor(name="mon", **spec):
    return {"apiVersion": "datadoghq.com/v1alpha1", "kind": "DatadogMonitor", "metadata": {"name": name}, "spec": spec}


def dashboard(name="dash", **spec):
    return {
        "apiVersion": "datadoghq.com/v1alpha1",
        "kind": "DatadogDashboard",
        "metadata": {"name": name},
        "spec": spec,
    }


class FakeResponse(io.BytesIO):
    status = 200


@pytest.fixture
def datadog_env(monkeypatch):
    monkeypatch.setenv("DD_SITE", "datadoghq.eu")
    monkeypatch.setenv("DD_API_KEY", "api-key")
    monkeypatch.setenv("DD_APP_KEY", "app-key")


def test_render_passes_helm_arguments_and_skips_blank_lines(tmp_path, monkeypatch):
    calls = []

    def run(command, stdout):
        calls.append(command)
        return subprocess.CompletedProcess(command, 0)

    monkeypatch.setattr(validate.subprocess, "run", run)
    charts = 'deploy/monitoring\n\n  deploy/agent --set clusterName=validate --set-string "note=a b"\n'

    assert not validate.render(charts, tmp_path)
    assert calls == [
        ["helm", "template", "monitoring", "deploy/monitoring"],
        ["helm", "template", "agent", "deploy/agent", "--set", "clusterName=validate", "--set-string", "note=a b"],
    ]
    assert sorted(path.name for path in tmp_path.iterdir()) == ["1-monitoring.yaml", "2-agent.yaml"]


def test_render_reports_a_failing_chart(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(validate.subprocess, "run", lambda command, stdout: subprocess.CompletedProcess(command, 1))

    assert validate.render("deploy/broken", tmp_path)
    assert "::error title=Chart deploy/broken::helm template failed" in capsys.readouterr().out


@pytest.mark.skipif(shutil.which("helm") is None, reason="helm is not installed")
def test_render_renders_the_fixture_chart(tmp_path):
    assert not validate.render(f"{shlex.quote(str(FIXTURES / 'chart'))} --set team=validate", tmp_path)
    assert [m["metadata"]["name"] for m in validate.resources(tmp_path, "DatadogMonitor")] == [
        "datadog-cr-validate-test"
    ]
    assert not validate.dashboards(tmp_path)


def test_resources_skips_empty_documents_other_kinds_and_other_files(tmp_path):
    (tmp_path / "1-a.yaml").write_text(
        "---\n# Source: chart/templates/empty.yaml\n"
        "---\nkind: ConfigMap\n"
        "---\nkind: DatadogMonitor\nmetadata: {name: a}\n"
    )
    (tmp_path / "2-b.yaml").write_text("kind: DatadogMonitor\nmetadata: {name: b}\n")
    (tmp_path / "notes.txt").write_text("kind: DatadogMonitor\nmetadata: {name: c}\n")

    assert [r["metadata"]["name"] for r in validate.resources(tmp_path, "DatadogMonitor")] == ["a", "b"]


def test_dashboards_accepts_a_valid_dashboard(tmp_path, capsys):
    widgets = [
        {"definition": {"type": "group", "widgets": [{"definition": {"type": "timeseries", "title": "CPU in $env"}}]}}
    ]
    write_manifests(tmp_path, dashboard(widgets=json.dumps(widgets), templateVariables=[{"name": "env"}]))

    assert not validate.dashboards(tmp_path)
    assert capsys.readouterr().out == "Linted dashboard dash\n"


@pytest.mark.parametrize("spec", [{"widgets": '{"not": "an array"}'}, {"widgets": "not json"}, {}])
def test_dashboards_rejects_widgets_that_are_not_a_json_array(tmp_path, capsys, spec):
    write_manifests(tmp_path, dashboard(**spec))

    assert validate.dashboards(tmp_path)
    assert "::error title=DatadogDashboard dash::spec.widgets is not a JSON array" in capsys.readouterr().out


def test_dashboards_counts_untyped_widgets_inside_groups(tmp_path, capsys):
    widgets = [
        {"definition": {"type": "group", "widgets": [{"definition": {}}, {"definition": {"type": 1}}]}},
        {},
    ]
    write_manifests(tmp_path, dashboard(widgets=json.dumps(widgets)))

    assert validate.dashboards(tmp_path)
    assert "::error title=DatadogDashboard dash::3 widget(s) have no definition.type" in capsys.readouterr().out


def test_dashboards_reports_undeclared_template_variables(tmp_path, capsys):
    widgets = [
        {
            "definition": {
                "type": "timeseries",
                "title": "$service",
                "requests": [{"q": "avg:system.cpu.user{env:$env,cluster:$cluster}"}],
            }
        }
    ]
    write_manifests(tmp_path, dashboard(widgets=json.dumps(widgets), templateVariables=[{"name": "env"}]))

    assert validate.dashboards(tmp_path)
    assert "::error title=DatadogDashboard dash::Undeclared template variables: cluster, service" in (
        capsys.readouterr().out
    )


def test_dashboards_rejects_the_invalid_fixture(capsys):
    assert validate.dashboards(FIXTURES)
    assert "Undeclared template variables: cluster" in capsys.readouterr().out


def test_monitor_payload_matches_the_operator_request():
    spec = {
        "name": "High restarts",
        "query": "avg(last_5m):avg:kubernetes.containers.restarts{*} > 1.5",
        "type": "query alert",
        "controllerOptions": {"disableRequiredTags": True},
        "options": {
            "notifyNoData": False,
            "evaluationDelay": 60,
            "thresholds": {"critical": "1.5", "warning": 1, "criticalRecovery": "0"},
        },
        "tags": ["team:validate"],
    }

    assert validate.monitor_payload(spec) == {
        "name": "High restarts",
        "query": "avg(last_5m):avg:kubernetes.containers.restarts{*} > 1.5",
        "type": "query alert",
        "options": {
            "notify_no_data": False,
            "evaluation_delay": 60,
            "thresholds": {"critical": 1.5, "warning": 1.0, "critical_recovery": 0.0},
        },
        "tags": ["team:validate"],
    }


def test_snake_case_converts_keys_in_nested_lists_and_leaves_values_alone():
    value = {"schedulingOptions": {"evaluationWindow": [{"dayStarts": "camelCase"}]}, "tags": ["teamName:x"]}

    assert validate.snake_case(value) == {
        "scheduling_options": {"evaluation_window": [{"day_starts": "camelCase"}]},
        "tags": ["teamName:x"],
    }


def test_datadog_sends_the_keys_and_json_body(monkeypatch, datadog_env):
    requests = []

    def urlopen(request):
        requests.append(request)
        return FakeResponse(b'{"ok": true}')

    monkeypatch.setattr(validate.urllib.request, "urlopen", urlopen)

    assert validate.datadog("POST", "/api/v1/monitor/validate", body={"query": "q"}) == (200, {"ok": True})
    [request] = requests
    assert request.get_method() == "POST"
    assert request.full_url == "https://api.datadoghq.eu/api/v1/monitor/validate"
    assert request.get_header("Dd-api-key") == "api-key"
    assert request.get_header("Dd-application-key") == "app-key"
    assert json.loads(request.data) == {"query": "q"}


def test_datadog_encodes_query_parameters(monkeypatch, datadog_env):
    requests = []

    def urlopen(request):
        requests.append(request)
        return FakeResponse(b"{}")

    monkeypatch.setattr(validate.urllib.request, "urlopen", urlopen)
    validate.datadog("GET", "/api/v2/metrics/system.cpu.user/all-tags", params={"window[seconds]": 604800})

    [request] = requests
    assert (
        request.full_url
        == "https://api.datadoghq.eu/api/v2/metrics/system.cpu.user/all-tags?window%5Bseconds%5D=604800"
    )
    assert request.data is None


def test_datadog_returns_the_error_body(monkeypatch, datadog_env):
    def urlopen(request):
        raise urllib.error.HTTPError(request.full_url, 400, "Bad Request", {}, io.BytesIO(b'{"errors":["bad query"]}'))

    monkeypatch.setattr(validate.urllib.request, "urlopen", urlopen)

    assert validate.datadog("POST", "/api/v1/monitor/validate", body={}) == (400, '{"errors":["bad query"]}')


def test_monitors_validates_each_monitor_and_reports_rejections(tmp_path, monkeypatch, capsys):
    write_manifests(tmp_path, monitor("good", query="good query"), monitor("bad", query="bad query"))
    posted = []

    def datadog(method, path, params=None, body=None):
        posted.append((method, path, body["query"]))
        return (200, {}) if body["query"] == "good query" else (400, '{"errors":["bad query"]}')

    monkeypatch.setattr(validate, "datadog", datadog)

    assert validate.monitors(tmp_path)
    assert posted == [
        ("POST", "/api/v1/monitor/validate", "good query"),
        ("POST", "/api/v1/monitor/validate", "bad query"),
    ]
    out = capsys.readouterr().out
    assert "Validated monitor good" in out
    assert '::error title=DatadogMonitor bad::HTTP 400: {"errors":["bad query"]}' in out


def test_metric_filters_collects_metrics_and_concrete_tag_filters(tmp_path):
    widgets = [
        {
            "definition": {
                "type": "timeseries",
                "requests": [{"q": "p95:trace.http.request{service:web OR (env:prod),!host:a} by {pod:x}"}],
            }
        }
    ]
    write_manifests(
        tmp_path,
        monitor("restarts", query="sum(last_5m):sum:k8s.restarts{team:x, reason:oomkilled, env:$env, kube_*} > 1"),
        monitor("agent", query="avg(last_5m):avg:datadog.agent.running{*} < 1"),
        dashboard(widgets=json.dumps(widgets)),
    )

    assert validate.metric_filters(tmp_path) == {
        "k8s.restarts": {"team:x", "reason:oomkilled"},
        "datadog.agent.running": set(),
        "trace.http.request": {"service:web", "env:prod"},
    }


def all_tags_responses(monkeypatch, responses):
    requested = []

    def datadog(method, path, params=None, body=None):
        requested.append((method, path, params))
        return responses[path.split("/")[4]]

    monkeypatch.setattr(validate, "datadog", datadog)
    return requested


def test_tags_fails_on_missing_or_unreadable_metrics(tmp_path, monkeypatch, capsys):
    write_manifests(tmp_path, monitor("a", query="avg:missing.metric{*}"), monitor("b", query="avg:broken.metric{*}"))
    requested = all_tags_responses(monkeypatch, {"missing.metric": (404, "{}"), "broken.metric": (500, "oops")})

    assert validate.tags(tmp_path)
    assert requested == [
        ("GET", "/api/v2/metrics/broken.metric/all-tags", {"window[seconds]": 604800}),
        ("GET", "/api/v2/metrics/missing.metric/all-tags", {"window[seconds]": 604800}),
    ]
    out = capsys.readouterr().out
    assert "::error title=Metric not found::missing.metric has not been reported in the last 7 days" in out
    assert "::error title=Metric broken.metric::HTTP 500: oops" in out


def test_tags_only_warns_on_unindexed_tag_values(tmp_path, monkeypatch, capsys):
    write_manifests(tmp_path, monitor(query="avg:present.metric{team:x,team:y}"))
    all_tags_responses(monkeypatch, {"present.metric": (200, {"data": {"attributes": {"tags": ["team:x"]}}})})

    assert not validate.tags(tmp_path)
    out = capsys.readouterr().out
    assert "::warning title=Tag value not found::present.metric{team:y} has not been indexed in the last 7 days" in out
    assert "present.metric{team:x}" not in out
    assert "Checked metric present.metric" in out


@pytest.mark.parametrize(("directory", "code"), [(FIXTURES, 1), (FIXTURES / "chart", 0)])
def test_main_exit_code_reflects_the_check_result(monkeypatch, directory, code):
    monkeypatch.setattr(sys, "argv", ["validate.py", "dashboards", str(directory)])

    with pytest.raises(SystemExit) as exit_info:
        validate.main()
    assert exit_info.value.code == code
