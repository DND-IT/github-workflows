terraform {
  required_version = ">= 1.7"
  backend "s3" {
    use_lockfile = true
    region       = "eu-central-1"
  }
}

module "workflow_test_docker_buildx_ecr" {
  source  = "terraform-aws-modules/ecr/aws"
  version = "2.4.0"

  repository_name               = "test-docker-buildx-push"
  repository_image_scan_on_push = false
  repository_lifecycle_policy = jsonencode({
    rules = [
      {
        rulePriority = 1,
        description  = "Remove Images older than 1 day",
        selection = {
          tagStatus   = "tagged",
          countType   = "sinceImagePushed",
          countNumber = 1
        },
        action = {
          type = "expire"
        }
      }
    ]
  })

  tags = {
    Usage = "Automated tests from github-workflows/_test-docker.yaml"
  }
}
