## Simulating step
# - name: Find files matching pattern
patterns="*.yaml,*.tf,*.tfvars"

IFS=',' read -ra globs <<< "$patterns"
> files.txt
for glob in "${globs[@]}"; do
  # If the pattern is a directory, search all files recursively inside it
  if [ -d "$glob" ]; then
    find "$glob" -type f >> files.txt || true
  else
    find . -type f -name "$glob" >> files.txt || true
  fi
done
sort -u files.txt -o files.txt
echo "Found files:"
cat files.txt

## Simulating step
# - name: Update files with latest RDS version
set -e
while read -r file; do
  echo "\n>> Processing file: $file"
  # Search for annotated lines
  grep -n '#dai-renovate-rds' "$file" | while IFS=: read -r lineno line; do
    echo "Processing line: $line (line number: $lineno)"
    # Parse annotation: #dai-renovate-rds engine:postgres version:16
    # Check dnd-it/github-workflows/tests/terraform/dai-renovate-rds/* for patterns
    if [[ "$line" =~ ([a-zA-Z0-9_]+)[[:space:]]*[:=][[:space:]]*(optional\([a-zA-Z0-9_]+,[[:space:]]*)?\"([0-9]+\.[0-9]+)\"(\))?[[:space:]]*#dai-renovate-rds[[:space:]]+engine:([a-zA-Z0-9_-]+)[[:space:]]+version:([0-9]+) ]]; then
      echo "Matched patter found"
      varname="${BASH_REMATCH[1]}"
      current="${BASH_REMATCH[3]}"
      engine="${BASH_REMATCH[5]}"
      major="${BASH_REMATCH[6]}"
      
      # Query AWS for latest version
      echo "Checking latest version for var: $varname, current: $current, engine: $engine, major: $major in file: $file"
      latest=$(aws rds describe-db-engine-versions --engine "$engine" --engine-version "$major" --query 'DBEngineVersions[*].EngineVersion' --output text | tr '\t' '\n' | sort -V | tail -1)
      
      if [[ "$current" != "$latest" && -n "$latest" ]]; then
        echo "Updating $varname in $file from $current to $latest"
        # Use line number to update in-place
        # `sed -i ''` is used for macOS compatibility
        # remember to remove the `''` if running on Linux
        sed -i '' "${lineno}s/\"$current\"/\"$latest\"/" "$file"
      fi
    else
      echo "No match found"
    fi
  done
done < files.txt

rm -f files.txt

git status

echo "branch_name=dai-renovate/rds-update-$latest" >> $GITHUB_OUTPUT
echo "latest=$latest" >> $GITHUB_OUTPUT

if [[ -n "$(git status --porcelain)" ]]; then
  echo "files were modified"
fi
