# Lab account may have no default VPC — create a minimal public VPC.
resource "aws_vpc" "workathon" {
  cidr_block           = "10.42.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "bankinter-workathon-vpc"
  }
}

resource "aws_internet_gateway" "workathon" {
  vpc_id = aws_vpc.workathon.id

  tags = {
    Name = "bankinter-workathon-igw"
  }
}

resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.workathon.id
  cidr_block              = "10.42.1.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "${var.aws_region}a"

  tags = {
    Name = "bankinter-workathon-public"
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.workathon.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.workathon.id
  }

  tags = {
    Name = "bankinter-workathon-public-rt"
  }
}

resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}

resource "aws_security_group" "workathon" {
  name        = "bankinter-workathon-sg"
  description = "Workathon lab: SSH, WinRM, RDP, HTTP"
  vpc_id      = aws_vpc.workathon.id

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.allowed_cidr]
  }

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = [var.allowed_cidr]
  }

  ingress {
    description = "HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = [var.allowed_cidr]
  }

  ingress {
    description = "WinRM HTTP"
    from_port   = 5985
    to_port     = 5985
    protocol    = "tcp"
    cidr_blocks = [var.allowed_cidr]
  }

  ingress {
    description = "WinRM HTTPS"
    from_port   = 5986
    to_port     = 5986
    protocol    = "tcp"
    cidr_blocks = [var.allowed_cidr]
  }

  ingress {
    description = "RDP"
    from_port   = 3389
    to_port     = 3389
    protocol    = "tcp"
    cidr_blocks = [var.allowed_cidr]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "bankinter-workathon-sg"
  }
}
