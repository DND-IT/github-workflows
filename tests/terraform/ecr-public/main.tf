terraform {
  required_version = ">= 1.7"
  backend "s3" {
    use_lockfile = true
    region       = "eu-central-1"
  }
  required_providers {
    helm = {
      source  = "hashicorp/helm"
      version = "~> 3.0"
    }
  }
}

data "helm_template" "karpenter_crd" {
  name       = "karpenter-crd"
  repository = "oci://public.ecr.aws/karpenter"
  chart      = "karpenter-crd"
  version    = "1.14.0"
}

output "karpenter_crd_manifest_count" {
  value = length(data.helm_template.karpenter_crd.manifests)
}
