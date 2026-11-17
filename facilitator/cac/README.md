# Facilitator CaC — org `facilitator`

Despliega en el cluster AAP una **organización sandbox** que replica el diseño del workathon (creds, project, inventario dinámico Name+labels, JTs) para validar que es viable antes del evento.

## Qué crea

| Objeto | Nombre |
|--------|--------|
| Organization | `facilitator` |
| Team | `facilitator-team` |
| Credentials | `facilitator-machine-linux`, `facilitator-machine-windows`, `facilitator-aws`, `facilitator-scm` |
| Project | `facilitator-starter` (archive SCM → starter + scoring) |
| Inventory | `facilitator-aws` |
| Inventory source | `facilitator-ec2` (EC2, hostnames=`Name`, grupos OS/Role) |
| Job Templates | `facilitator-baseline`, `facilitator-deploy-linux-web`, `facilitator-deploy-windows-iis`, `facilitator-smoke` |

Inventario esperado tras sync: hosts `tN-linux` / `tN-windows` y grupos `linux`, `windows`, `web`, `db`.

## Requisitos

- Token OAuth Controller (`CONTROLLER_TOKEN`) + `CONTROLLER_HOST`
- AWS keys con `ec2:Describe*` (mismas del lab)
- Archive del starter en S3 (`scripts/refresh_archive_url.py`)
- Python 3 + `PyYAML` + `boto3`

> Este AAP usa `/api/controller/v2` y `/api/gateway/v1` (no `/api/v2`). Por eso el apply canónico es el script Python, no `awx.awx` a pelo.

## Aplicar

```bash
cd bankinter/workathon/facilitator/cac

export CONTROLLER_HOST=https://bankinter-aap.apps.hetzner.calopezb.com
export CONTROLLER_TOKEN=<oauth>
export AWS_ACCESS_KEY_ID=... AWS_SECRET_ACCESS_KEY=...
export FACILITATOR_STARTER_URL=$(python3 scripts/refresh_archive_url.py)
export VERIFY_SSL=0

python3 scripts/apply_facilitator.py
python3 scripts/validate_facilitator.py
```

Playbooks Ansible (`playbooks/*.yml`) quedan como referencia / para cuando el cluster exponga `/api/v2`.

## Validación

`validate_facilitator.py` comprueba vía API:

1. Hosts con nombre = tag `Name` (`tN-linux` / `tN-windows`)
2. Grupos `linux` / `windows` / `web` / `db`
3. Membresía `t1-linux` ∈ linux∩web y `t1-windows` ∈ windows∩db

## Notas

- El Project usa **archive SCM** (tar.gz público en S3) porque Gitea del pack aún es placeholder. El día del evento los equipos usan Gitea + cred `tN-scm-gitea`.
- En `keyed_groups`, usar `tags.Team | string` (si no, el plugin EC2 falla con `Invalid group name format ... int`).
- No commitear `vars/secrets.yml` ni tokens.
