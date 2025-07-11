## Dai Renovate AWS RDS

Automates the process of updating AWS RDS engine versions in the infrastructure code. It is designed to be **reusable** and configurable for different file patterns and schedules.

### Features

- **Annotation-based detection:**  
  Searches for lines annotated with `#dai-renovate-rds engine:<engine> version:<major>` in your codebase.  
  Example annotation:  
  ```
  engine_version = "16.7" #dai-renovate-rds engine:postgres version:16
  ```

- **AWS RDS version lookup:**  
  For each annotation, queries AWS to find the latest available engine version for the specified engine and major version.

- **Automated updates:**  
  If a newer version is available, updates the corresponding variable assignment in the file.

- **Pull request automation:**  
  Commits the changes and creates a pull request with a summary of the updates.

- **Configurable file search:**  
  Accepts a `files_pattern` input to specify which files to scan (default: `**/*.yaml,**/*.tf,**/*.tfvars`).

- **Flexible scheduling:**  
  Runs every 3 months by default, but can be triggered manually or configured with a custom schedule.

### Usage

- **Reusable:**  
  Can be called from other workflows using `workflow_call` and custom inputs.
- **Manual or scheduled:**  
  Supports manual dispatch and scheduled runs.

### Example

Add the annotation above any RDS engine version variable you want to keep updated:
```hcl
engine_version = "16.7" #dai-renovate-rds engine:postgres version:16
```
