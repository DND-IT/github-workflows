terraform {
  backend "s3" {
    use_lockfile = true
    region       = "eu-central-1"
  }

  required_providers {
    github = {
      source  = "integrations/github"
      version = "~> 6.13"
    }
  }
}

provider "github" {
  owner = "DND-IT"
}

data "github_repository" "this" {
  full_name = "DND-IT/github-workflows"
}

resource "terraform_data" "always_changes" {
  input = timestamp()
}

output "repository" {
  value = data.github_repository.this.full_name
}
