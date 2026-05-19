# terraform {
#   backend "s3" {
#     bucket = "conraad-tf-state"
#     key = "notes-app/terraform.tfstate"
#     region = "us-east-1"
#     dynamodb_table = "terraform-state-locking"
#     encrypt = true
#   }
#
#   required_providers {
#     aws = {
#       source = "hashicorp/aws"
#       version = "~> 6.0"
#     }
#   }
# }
