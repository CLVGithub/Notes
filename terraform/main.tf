terraform {
  backend "s3" {
    bucket       = "conraad-tf-state"
    key          = "notes-app-module/terraform.tfstate"
    region       = "us-east-1"
    use_lockfile = true
    encrypt      = true
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

variable "db_pass" {
  description = "Password for the notes database"
  type        = string
  sensitive   = true
}

module "notes_app" {
  source = "./notes-module"

  db_pass = var.db_pass
}
