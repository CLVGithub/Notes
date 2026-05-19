# EC2 security group
resource "aws_security_group" "ec2_sg" {
  name        = "ec-security-group"
  description = "Allows incoming HTTP traffic for the notes app"
  vpc_id      = aws_vpc.main.id
}


resource "aws_security_group_rule" "allow_http_inbound" {
  type              = "ingress"
  security_group_id = aws_security_group.ec2_sg.id

  from_port   = 80
  to_port     = 80
  protocol    = "tcp"
  cidr_blocks = ["0.0.0.0/0"]
}

resource "aws_security_group_rule" "allow_ssh" {
  type              = "ingress"
  security_group_id = aws_security_group.ec2_sg.id

  from_port   = 22
  to_port     = 22
  protocol    = "tcp"
  cidr_blocks = ["0.0.0.0/0"]
}

resource "aws_security_group_rule" "allow_all_outbound" {
  type              = "egress"
  security_group_id = aws_security_group.ec2_sg.id

  from_port   = 0
  to_port     = 0
  protocol    = "-1"
  cidr_blocks = ["0.0.0.0/0"]
}

# RDS security group
resource "aws_security_group" "db_sg" {
  name        = "db-security-group"
  description = "Allows the notes-app to communicate with the database"
  vpc_id      = aws_vpc.main.id
}

resource "aws_security_group_rule" "allow_mysql_inbound" {
  type              = "ingress"
  security_group_id = aws_security_group.db_sg.id

  from_port                = 5432
  to_port                  = 5432
  protocol                 = "tcp"
  source_security_group_id = aws_security_group.ec2_sg.id
}
