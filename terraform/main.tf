# resource "aws_instance" "backend_server" {
#   ami = "ami-091138d0f0d41ff90"
#   instance_type = "t3.micro"
#
#   tags = {
#     Name = "backend-server"
#   }
# }
#
locals {
  extra_tag = "extra-tag"
}

resource "aws_instance" "instance_1" {
  ami = var.ami
  instance_type = var.instance_type

  security_groups = [aws_security_group.instances.name]
  tags = {
    Name = "instance_number_1"
  }
  user_data = <<-EOF
          #!/bin/bash
          echo "Hello, World 1" > index.html
          python3 -m http.server 8080 &
          EOF
}

resource "aws_instance" "instance_2" {
  ami = var.ami
  instance_type = var.instance_type

  security_groups = [aws_security_group.instances.name]
  tags = {
    Name = "instance_number_2"
  }
  user_data = <<-EOF
          #!/bin/bash
          echo "Hello, World 2" > index.html
          python3 -m http.server 8080 &
          EOF
}

resource "aws_s3_bucket" "bucket" {
  bucket = var.bucket_name
  force_destroy = true
}

resource "aws_s3_bucket_ownership_controls" "example" {
  bucket = aws_s3_bucket.bucket.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_public_access_block" "example" {
  bucket = aws_s3_bucket.bucket.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_acl" "example" {
  depends_on = [
    aws_s3_bucket_ownership_controls.example,
    aws_s3_bucket_public_access_block.example,
  ]

  bucket = aws_s3_bucket.bucket.id
  acl    = "public-read-write"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "bucket_encryption" {
  bucket = aws_s3_bucket.bucket.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_versioning" "bucket_versioning" {
  bucket = aws_s3_bucket.bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

data "aws_vpc" "default_vpc" {
  default = true
}

data "aws_subnets" "default_subnet" {
  filter {
    name = "vpc-id"
    values = [data.aws_vpc.default_vpc.id]
  }
}

resource "aws_security_group" "instances" {
  name = "instance-security-group"
  description = "Allows funky fresh new security"
}

resource "aws_security_group_rule" "allow_http_inbound" {
  type = "ingress"
  security_group_id = aws_security_group.instances.id

  from_port   = 8080
  to_port     = 8080
  protocol    = "tcp"
  cidr_blocks = ["0.0.0.0/0"]
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.load_balancer.arn

  port = 80

  protocol = "HTTP"

  # By default, return a simple 404 page
  default_action {
    type = "fixed-response"

    fixed_response {
      content_type = "text/plain"
      message_body = "404: Not Found"
      status_code  = "404"
    }
  }
}

resource "aws_lb_target_group" "instances" {
  name = "example-target-group"
  port = 8080
  protocol = "HTTP"
  vpc_id = data.aws_vpc.default_vpc.id

  health_check {
    path = "/"
    protocol = "HTTP"
    matcher = "200"
    interval = 15
    timeout = 3
    healthy_threshold = 2
    unhealthy_threshold = 2
  }
}

resource "aws_lb_target_group_attachment" "instance_1" {
  target_group_arn = aws_lb_target_group.instances.arn
  target_id = aws_instance.instance_1.id
  port = 8080
}

resource "aws_lb_target_group_attachment" "instance_2" {
  target_group_arn = aws_lb_target_group.instances.arn
  target_id = aws_instance.instance_2.id
  port = 8080
}

resource "aws_lb_listener_rule" "instances" {
  listener_arn = aws_lb_listener.http.arn
  priority = 100

  condition {
    path_pattern {
      values = ["*"]
    }
  }

  action {
    type = "forward"
    target_group_arn = aws_lb_target_group.instances.arn
  }
}

resource "aws_security_group" "alb" {
  name = "alb-security-group"
}

resource "aws_security_group_rule" "allow_alb_http_inbound" {
  type = "ingress"
  security_group_id = aws_security_group.alb.id

  from_port = 80
  to_port = 80
  protocol = "tcp"
  cidr_blocks = ["0.0.0.0/0"]
}

resource "aws_security_group_rule" "allow_alb_all_outbound" {
  type = "egress"
  security_group_id = aws_security_group.alb.id

  from_port = 0
  to_port = 0
  protocol = "-1"
  cidr_blocks = ["0.0.0.0/0"]
}

resource "aws_lb" "load_balancer" {
  name = "web-app-lb"
  load_balancer_type = "application"
  subnets = data.aws_subnets.default_subnet.ids
  security_groups = [aws_security_group.alb.id]
}

resource "aws_db_instance" "db_instance" {
  # identifier = "notes-rds-database"

  tags = {
    Name = "my-totally-awesome-funtime-database"
    Environment = "prod"
  }

  allocated_storage = 10
  storage_type = "standard"
  engine = "postgres"
  engine_version = "18.3"
  instance_class = "db.t3.micro"
  db_name = var.db_name
  username = var.db_user
  password = var.db_pass
  skip_final_snapshot = true
}
