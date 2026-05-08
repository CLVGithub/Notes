resource "aws_instance" "backend_server" {
  ami = "ami-091138d0f0d41ff90"
  instance_type = "t3.micro"

  tags = {
    Name = "backend-server"
  }
}
