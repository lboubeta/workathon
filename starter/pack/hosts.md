# Hosts seed (pack)

## Linux

| Campo | Valor |
|-------|-------|
| User SSH | `ansible` (también `ec2-user`) |
| Auth | password `Ansible123!` (creada por Terraform user-data) |
| Puerto | `22` |
| Python | `/usr/bin/python3` |

## Windows

| Campo | Valor |
|-------|-------|
| User WinRM | `ansible` (también `Administrator`) |
| Password | `Ansible123!` |
| Puerto | `5985` (HTTP) / `5986` (HTTPS) |
| Transport | `ntlm` |
| Server | `http` o `https` según lab |

VMs provisionadas con [`../../terraform`](../../terraform): **2 por equipo** — `tN-linux` (`OS=linux`, `Role=web`) y `tN-windows` (`OS=windows`, `Role=db`).

### Variables de inventario sugeridas (Windows)

```yaml
ansible_connection: winrm
ansible_user: ansible
ansible_password: "{{ vault_or_credential }}"
ansible_port: 5985
ansible_winrm_transport: ntlm
ansible_winrm_server_cert_validation: ignore
```

> Preferible: password solo en credencial Machine AAP, no en Git.
