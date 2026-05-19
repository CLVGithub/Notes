variable "ami" {
  description = "Amazon machine image to use for EC2 instance"
  type        = string
  default     = "ami-091138d0f0d41ff90"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}

variable "db_user" {
  description = "Username for database"
  type        = string
  default     = "postgres"
}

variable "db_pass" {
  description = "Password for database"
  type        = string
  sensitive   = true
  default     = "postgres"
}

variable "db_name" {
  description = "Name of the database"
  type        = string
  default     = "notes_db"
}

# S3 Bucket

variable "bucket_name" {
  description = "Name of the S3 bucket"
  type        = string
  default     = "conraad-notes-bucket"
}
