resource "aws_db_instance" "db_instance" {
  allocated_storage = 10
  engine = "postgres"
  engine_version = "18.3"
  instance_class = "db.t3.micro"

  username = var.db_user
  password = var.db_pass
  db_name = var.db_name

  skip_final_snapshot = true

  db_subnet_group_name = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.db_sg.id]
}

resource "aws_db_subnet_group" "main" {
  name = "main-db-subnet-group"
  subnet_ids = [
    aws_subnet.private_1.id,
    aws_subnet.private_2.id
  ]
}

resource "aws_subnet" "private_1" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.3.0/24"
  availability_zone = "us-east-1a"  # change to your region

  tags = {
    Name = "private-subnet-1"
  }
}

resource "aws_subnet" "private_2" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.4.0/24"
  availability_zone = "us-east-1b"

  tags = {
    Name = "private-subnet-2"
  }
}
