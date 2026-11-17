# Lab 2 — Credenciales y Projects (35 min)

## Objetivo

**Vosotros** creáis en Controller todas las credenciales tipadas y el Project SCM del equipo (el facilitador no los deja hechos). Sync del Project en verde y prueba de conectividad.

## Datos del pack

- `pack/scm.md` — URL Gitea, branch, token/clave
- `pack/cloud.md` — AWS access/secret o rol
- `pack/hosts.md` — usuario SSH, usuario WinRM, puertos
- Prefijo obligatorio: `tN-` (ej. equipo 1 → `t1-…`)

## Credenciales a crear (obligatorio)

| Nombre exacto | Tipo | Campos |
|---------------|------|--------|
| `tN-scm-gitea` | Source Control | Usuario/token Gitea |
| `tN-machine-linux` | Machine | SSH user + password/key (`ansible` / pack) |
| `tN-machine-windows` | Machine | WinRM user/password; connection WinRM |
| `tN-aws` | Amazon Web Services | Access key + secret (o assume role) |

Asignar cada credencial al Team con rol **Use** (no hace falta Admin).

### WinRM (Machine)

En la credencial Machine para Windows:

- Username / Password del pack
- En Lab 3–4 (vars de inventario / JT): `ansible_connection=winrm`, `ansible_winrm_transport=ntlm`, `ansible_port=5985|5986`

## Project (obligatorio)

1. Crear Project **`tN-starter`** (nombre exacto)
2. SCM Type: Git
3. URL: la del pack (`pack/scm.md`)
4. Branch: `main` (o la indicada)
5. Credential: `tN-scm-gitea`
6. Options: **Update Revision on Launch** (recomendado)
7. Organization: `tN-org`
8. Guardar → **Sync**

## Criterio de éxito (puntuable)

- [ ] Las 4 credenciales existen con los nombres `tN-*` (**vosotros las creáis**; el facilitador no las pre-crea)
- [ ] Project `tN-starter` sync **Successful**
- [ ] Playbooks visibles (`playbooks/*.yml`)
- [ ] Credenciales con **Use** para el Team (secrets no visibles en claro)

> Recuento automático: `facilitator/scoring/score_teams.py` (labs 2–3, 30 pts).

## Troubleshooting rápido

| Síntoma | Comprobar |
|---------|-----------|
| Project failed | Token Gitea, URL, branch, conectividad Controller→Gitea |
| WinRM timeout | SG/firewall, puerto, `ansible_winrm_*`, credencial |
| AWS cred inválida | Reloj, políticas IAM, región |
