# EC2 variables

# variable "instance_name" {
#   description = "Name of EC2 instance"
#   type = string
# }

variable "ami" {
  description = "Amazon machine image to use for EC2 instance"
  type = string
  default = "ami-091138d0f0d41ff90"
}

variable "instance_type" {
  description = "EC2 instance type"
  type = string
  default = "t3.micro"
}

# RDS variables

variable "db_user" {
  description = "Username for database"
  type = string
  default = "foo"
}

variable "db_pass" {
  description = "Password for database"
  type = string
  sensitive = true
}

variable "db_name" {
  description = "Name of DB"
  type = string
  default = "woopdidoodatabase"
}

# S3 Bucket

variable "bucket_name" {
  description = "Name of the S3 bucket"
  type = string
  default = "super-cool-lion"
}
