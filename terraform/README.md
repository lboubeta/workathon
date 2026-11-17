# Terraform — VMs del workathon (AWS)

Crea una **VPC pública** (si la cuenta no tiene default VPC) y **6 instancias** en `eu-west-1` (**2 por equipo**):

| Equipo | Linux (`Role=web`) | Windows (`Role=db`) |
|--------|--------------------|---------------------|
| 1 | `t1-linux` | `t1-windows` |
| 2 | `t2-linux` | `t2-windows` |
| 3 | `t3-linux` | `t3-windows` |

Tags: `Team`, `OS` (`linux`\|`windows`), `Role` (`web`\|`db`), `Env=dev` — hostname inventario = `Name` (sin rol en el nombre); grupos = valores de `OS`/`Role`.

## Acceso

- IP pública en todas las VMs
- SG abierto (por defecto `0.0.0.0/0`) a SSH `22`, HTTP/S `80/443`, WinRM `5985/5986`, RDP `3389`
- Usuario Linux: `ansible` (también `ec2-user`)
- Usuario Windows: `ansible` y `Administrator`
- Password: `Ansible123!` (variable `instance_password`)
- Key pair EC2: útil en Linux (RSA o ED25519). Windows no acepta ED25519; el lab usa password vía user-data.

> Lab only: password en claro y SG abierto. Restringe `allowed_cidr` en un entorno real.

## Uso

```bash
cd bankinter/workathon/terraform
aws configure   # o AWS_PROFILE=...
terraform init
terraform plan
terraform apply
terraform output
```

Opcional: copiar `terraform.tfvars.example` → `terraform.tfvars`.

Tras el apply, Windows puede tardar **5–10 min** en aplicar el user-data (WinRM + usuario).

## Destroy

```bash
terraform destroy
```
