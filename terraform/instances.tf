locals {
  team_map = { for t in var.teams : t => t }

  common_linux_user_data = templatefile("${path.module}/templates/linux_userdata.sh.tftpl", {
    password = var.instance_password
  })

  common_windows_user_data = templatefile("${path.module}/templates/windows_userdata.ps1.tftpl", {
    password = var.instance_password
  })
}

# 2 VMs per team: Linux=web, Windows=db → inventory groups linux/windows/web/db
resource "aws_instance" "linux" {
  for_each = local.team_map

  ami                         = data.aws_ami.amazon_linux.id
  instance_type               = var.linux_instance_type
  subnet_id                   = aws_subnet.public.id
  vpc_security_group_ids      = [aws_security_group.workathon.id]
  associate_public_ip_address = true
  key_name                    = var.key_name != "" ? var.key_name : null
  user_data                   = local.common_linux_user_data
  user_data_replace_on_change = true

  root_block_device {
    volume_size = 30
    volume_type = "gp3"
  }

  tags = {
    Name = "t${each.key}-linux"
    Team = each.key
    OS   = "linux"
    Role = "web"
    Env  = var.env_tag
  }
}

resource "aws_instance" "windows" {
  for_each = local.team_map

  ami                         = data.aws_ami.windows_2022.id
  instance_type               = var.windows_instance_type
  subnet_id                   = aws_subnet.public.id
  vpc_security_group_ids      = [aws_security_group.workathon.id]
  associate_public_ip_address = true
  # Windows AMIs reject ED25519 key pairs; lab auth is password via user-data.
  key_name                    = null
  user_data                   = local.common_windows_user_data
  user_data_replace_on_change = true
  get_password_data           = false

  root_block_device {
    volume_size = 50
    volume_type = "gp3"
  }

  tags = {
    Name = "t${each.key}-windows"
    Team = each.key
    OS   = "windows"
    Role = "db"
    Env  = var.env_tag
  }
}
