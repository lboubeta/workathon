output "linux_instances" {
  description = "Linux web VMs per team (Role=web)"
  value = {
    for k, i in aws_instance.linux : k => {
      name       = i.tags["Name"]
      public_ip  = i.public_ip
      private_ip = i.private_ip
      id         = i.id
      ssh        = "ssh ansible@${i.public_ip}"
    }
  }
}

output "windows_instances" {
  description = "Windows DB VMs per team (Role=db)"
  value = {
    for k, i in aws_instance.windows : k => {
      name       = i.tags["Name"]
      public_ip  = i.public_ip
      private_ip = i.private_ip
      id         = i.id
      rdp        = "${i.public_ip}:3389"
      winrm      = "${i.public_ip}:5985"
    }
  }
}

output "inventory_hint" {
  description = "Tags aligned with workathon dynamic inventory"
  value       = "2 VMs/team: tN-linux (OS=linux,Role=web) + tN-windows (OS=windows,Role=db); hostname=Name; groups=OS+Role"
}

output "credentials_hint" {
  description = "Lab login (see var.instance_password)"
  value = {
    linux_user   = "ansible (also ec2-user)"
    windows_user = "ansible (also Administrator)"
    password     = "(sensitive — terraform output -raw not available; use var default Ansible123!)"
  }
}
