resource "aws_instance" "instance" {
  ami = var.ami
  instance_type = var.instance_type
  vpc_security_group_ids = [aws_security_group.ec2_sg.id]
  subnet_id = aws_subnet.public.id

  key_name = aws_key_pair.this.key_name

  tags = {
    Name = "notes-app-ec2"
  }

  associate_public_ip_address = true
}

resource "aws_key_pair" "this" {
  key_name = "ec2-key"
  public_key = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIMQesKKH0FDpSocoh6Sl6U2vw+xbbREcI600piEET9Eb ec2-key"
}
