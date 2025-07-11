## Simulating step
# - name: Find files matching pattern
patterns="**/*.yaml,**/*.tf,**/*.tfvars"

IFS=',' read -ra globs <<< "$patterns"
> files.txt
for glob in "${globs[@]}"; do
  find . -type f -name "${glob// /}" >> files.txt || true
done
sort -u files.txt -o files.txt
cat files.txt

## Simulating step
# - name: Update files with latest RDS version
set -e
changed=0
while read -r file; do
  # Search for annotated lines
  grep -n '#dai-renovate-rds' "$file" | while IFS=: read -r lineno line; do
    # Parse annotation: #dai-renovate-rds engine:postgres version:16
    # Check dnd-it/github-workflows/tests/terraform/dai-renovate-rds/* for patterns
    if [[ "$line" =~ ([a-zA-Z0-9_]+)[[:space:]]*[:=][[:space:]]*(optional\([a-zA-Z0-9_]+,\s*)?"([0-9]+\.[0-9]+)"\)?[[:space:]]*#dai-renovate-rds[[:space:]]+engine:([a-zA-Z0-9_-]+)[[:space:]]+version:([0-9]+) ]]; then
      varname="${BASH_REMATCH[1]}"
      current="${BASH_REMATCH[3]}"
      engine="${BASH_REMATCH[4]}"
      major="${BASH_REMATCH[5]}"
      
      # Query AWS for latest version
      echo "Checking latest version for engine: $engine, major: $major in file: $file"
      latest=$(aws rds describe-db-engine-versions --engine "$engine" --engine-version "$major" --query 'DBEngineVersions[*].EngineVersion' --output text | tr '\t' '\n' | sort -V | tail -1)
      
      if [[ "$current" != "$latest" && -n "$latest" ]]; then
        echo "Updating $varname in $file from $current to $latest"
        # Use line number to update in-place
        sed -i "${lineno}s/\"$current\"/\"$latest\"/" "$file"
        changed=1
      fi
    fi
  done
done < files.txt
echo "latest=$latest"
echo "changed=$changed"
