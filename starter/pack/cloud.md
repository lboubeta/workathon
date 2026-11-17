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
| `Name` | `t1-linux` / `t1-windows` (2 VMs/equipo) |
| `Team` | `1` |
| `OS` | `linux` o `windows` → grupos inventario `linux` / `windows` |
| `Role` | `web` o `db` → grupos inventario `web` / `db` |
| `Env` | `dev` o `prod` |

Inventario: hostname = `Name`. Ejemplo source vars: [`inventory-source.example.yml`](inventory-source.example.yml).

## Límites

- Máx. instancias adicionales por equipo: **2**
- Cleanup: lanzar JT de terminate al final del wrap (facilitador).
