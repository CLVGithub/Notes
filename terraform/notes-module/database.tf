resource "aws_db_instance" "db_instance" {
  allocated_storage = 10
  engine = "postgres"
  engine_version = "18.3"
  instance_class = "db.t3.micro"
  username = var.db_user
  password = var.db_pass
  db_name = var.db_name
  skip_final_snapshot = true
}
