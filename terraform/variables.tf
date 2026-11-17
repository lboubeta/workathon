variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "eu-west-1"
}

variable "teams" {
  description = "Team identifiers (one Linux + one Windows per team)"
  type        = list(string)
  default     = ["1", "2", "3"]
}

variable "instance_password" {
  description = "Password for ansible/Administrator users (lab only)"
  type        = string
  default     = "Ansible123!"
  sensitive   = true
}

variable "allowed_cidr" {
  description = "CIDR allowed to reach SSH/WinRM/RDP/HTTP (lab: 0.0.0.0/0)"
  type        = string
  default     = "0.0.0.0/0"
}

variable "linux_instance_type" {
  type    = string
  default = "t3.small"
}

variable "windows_instance_type" {
  type    = string
  default = "t3.medium"
}

variable "key_name" {
  description = "Optional existing EC2 key pair (SSH/RDP fallback). Leave empty to skip."
  type        = string
  default     = ""
}

variable "env_tag" {
  type    = string
  default = "dev"
}
