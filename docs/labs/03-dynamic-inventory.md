# Lab 3 — Inventarios dinámicos (+ Windows) (40 min)

## Objetivo

Conectar un inventory source AWS EC2, construir grupos dinámicos por tags (incl. OS Windows) y validar con `ping` / `win_ping` selectivos.

## Pasos

1. Crear Inventory `tN-aws`
2. Añadir **Inventory Source**:
   - Source: Amazon EC2
   - Credential: `tN-aws`
   - Regions: la del pack
   - Update on launch: sí
   - Source variables (ejemplo):

```yaml
compose:
  ansible_host: public_ip_address | default(private_ip_address)
keyed_groups:
  - key: tags.Env
    prefix: env
  - key: tags.Role
    prefix: role
  - key: tags.OS
    prefix: os
  - key: tags.Team
    prefix: team
groups:
  web_prod: "'web' in (role_web | default([])) and 'prod' in (env_prod | default([]))"
hostnames:
  - tag:Name
  - private-ip-address
```

3. Ajustar `groups` / filtros para limitar a `tags.Team == N` (evitar ver hosts de otros equipos).
4. **Sync** del source.
5. Revisar hosts y grupos generados: `env_*`, `role_*`, `os_linux`, `os_windows`, `team_N`.
6. En hosts Windows, verificar variables (group_vars o host_vars):

```yaml
ansible_connection: winrm
ansible_winrm_transport: ntlm
ansible_port: 5985
```

7. Ad-hoc (o JT seed):
   - Módulo `ping` → límite `os_linux:&team_N`
   - Módulo `win_ping` → límite `os_windows:&team_N`

## Criterio de éxito

- [ ] Sync inventory Successful
- [ ] Existen grupos dinámicos por Env, Role, OS
- [ ] Al menos un host Linux y uno Windows del equipo
- [ ] `ping` OK solo en Linux del equipo
- [ ] `win_ping` OK solo en Windows del equipo

## Notas

Si el facilitador usa inventory estático seed además de AWS, documentad ambos; el objetivo pedagógico es el **source dinámico** y los **keyed_groups**.
