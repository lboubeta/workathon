# AWS (pack)

| Campo | Valor |
|-------|-------|
| Account / alias | |
| Region | `eu-west-1` |
| Access Key ID | `CHANGE_ME` |
| Secret Access Key | `CHANGE_ME` |
| Opcional: Role ARN | |

## Tags obligatorios en EC2 seed

| Tag | Ejemplo |
|-----|---------|
| `Name` | `t1-web-linux` |
| `Team` | `1` |
| `OS` | `linux` o `windows` |
| `Role` | `web` |
| `Env` | `dev` o `prod` |

## Límites

- Máx. instancias adicionales por equipo: **2**
- Cleanup: lanzar JT de terminate al final del wrap (facilitador).
