# Lab 3 — Inventarios dinámicos (+ Windows) (40 min)

## Objetivo

Crear un Inventory + source **AWS EC2** con la credencial `tN-aws` del Lab 2. Los **nombres de host** deben ser el **Name** de la instancia EC2; los **grupos** se generan desde los labels/tags (`linux`, `windows`, `web`, `db`).

**Seed por equipo (2 VMs):** Linux = `web`, Windows = `db`.

## Pasos

1. Crear Inventory **`tN-aws`** (nombre exacto) en `tN-org`.
2. Añadir **Inventory Source** (nombre sugerido `tN-ec2`):
   - Source: Amazon EC2
   - Credential: `tN-aws`
   - Regions: `eu-west-1` (pack)
   - Update on launch: sí
   - **Source variables** (usar este esqueleto; ajustar `Team`):

```yaml
# Filtrar solo las VMs del equipo (obligatorio)
filters:
  tag:Team: "N"

compose:
  ansible_host: public_ip_address | default(private_ip_address)

# Nombre en inventario = tag Name de la instancia (ej. t1-linux)
hostnames:
  - tag:Name

# Grupos = valor del label (sin prefijo os_/role_)
keyed_groups:
  - key: tags.OS
    separator: ""
  - key: tags.Role
    separator: ""
  - key: tags.Env
    prefix: env
  - key: tags.Team
    prefix: team
```

> Objetivo pedagógico: grupos **`linux`**, **`windows`**, **`web`**, **`db`** (valores de `OS` / `Role`), no `os_linux` / `role_web`.

3. **Sync** del source.
4. Verificar hosts:
   - Exactamente **2 hosts**: `tN-linux`, `tN-windows` (coinciden con el tag `Name` en AWS)
   - Grupos presentes: `linux`, `windows`, `web`, `db` (+ `team_N`, `env_dev`…)
   - Membresía: `tN-linux` ∈ `linux` ∩ `web`; `tN-windows` ∈ `windows` ∩ `db`
5. En el grupo `windows` (o inventory `group_vars` del Project), vars WinRM:

```yaml
ansible_connection: winrm
ansible_winrm_transport: ntlm
ansible_port: 5985
ansible_winrm_server_cert_validation: ignore
```

El starter ya trae `group_vars/windows.yml` alineado con el grupo `windows`.

6. Ad-hoc (o JT seed) — **nunca** `all` a ciegas:
   - `ping` → límite `linux` (o `web`)
   - `win_ping` → límite `windows` (o `db`)

## Tags EC2 esperados (seed Terraform)

| Tag | Valores | Grupo dinámico |
|-----|---------|----------------|
| `Name` | `tN-linux`, `tN-windows` | = hostname en inventario |
| `OS` | `linux`, `windows` | grupos `linux` / `windows` |
| `Role` | `web` (Linux), `db` (Windows) | grupos `web` / `db` |
| `Team` | `1`\|`2`\|`3` | `team_N` + filtro source |
| `Env` | `dev`\|`prod` | `env_*` |

## Criterio de éxito (puntuable)

- [ ] Inventory `tN-aws` + sync Successful
- [ ] Hostnames = instance `Name` (`tN-linux`, `tN-windows` — no IP ni `i-…`)
- [ ] Grupos `linux`, `windows`, `web`, `db` existen
- [ ] Hosts en los grupos correctos (`web`↔linux, `db`↔windows)
- [ ] `ping` OK en `linux` del equipo
- [ ] `win_ping` OK en `windows` del equipo

## Notas

El objetivo pedagógico es el **source dinámico**, **hostnames desde Name** y **keyed_groups desde labels**. El scoring del facilitador comprueba nombres y grupos vía API.
