terraform {
  required_version = "= 1.10.5"
  backend "s3" {
    use_lockfile = true
    region       = "eu-central-1"
  }
}

resource "random_pet" "this" {
  length = 2
}

output "random_pet" {
  value = random_pet.this.id
}
