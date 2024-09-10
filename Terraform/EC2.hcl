provider "aws" {
  region = "us-east-1" # Change this to your preferred region
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.medium"
}

variable "key_name" {
  description = "Name of an existing EC2 KeyPair to enable SSH access"
  type        = string
}

resource "aws_security_group" "kali_sg" {
  name        = "kali_sg"
  description = "Security group for Kali Linux instance"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Allow SSH from any IP; change for more security
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "kali_instance" {
  ami             = "ami-xxxxxxxxxxxxxxxxx"  # Replace with the Kali Linux AMI ID for your region
  instance_type   = var.instance_type
  key_name        = var.key_name
  security_groups = [aws_security_group.kali_sg.name]

  tags = {
    Name = "KaliLinuxInstance"
  }
}

output "instance_id" {
  description = "The Instance ID of the Kali Linux EC2 instance"
  value       = aws_instance.kali_instance.id
}

output "public_ip" {
  description = "The public IP address of the Kali Linux EC2 instance"
  value       = aws_instance.kali_instance.public_ip
}
