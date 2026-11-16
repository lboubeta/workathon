# Lab 2 — Credenciales y Projects (35 min)

## Objetivo

Crear credenciales tipadas y un Project SCM apuntando al repo Gitea del equipo. Verificar sync en verde y prueba WinRM.

## Datos del pack

- `pack/scm.md` — URL Gitea, branch, token/clave
- `pack/cloud.md` — AWS access/secret o rol
- `pack/hosts.md` — usuario SSH, usuario WinRM, puertos

## Credenciales a crear

| Nombre sugerido | Tipo | Campos |
|-----------------|------|--------|
| `tN-scm-gitea` | Source Control | Usuario/token Gitea |
| `tN-machine-linux` | Machine | SSH user + key/password |
| `tN-machine-windows` | Machine | WinRM user/password; connection WinRM |
| `tN-aws` | Amazon Web Services | Access key + secret (o assume role) |

Asignar cada credencial al Team con rol **Use**.

### WinRM (Machine)

En la credencial Machine para Windows:

- Username / Password del pack
- En el Job Template (Lab 4) o en variables de inventario: `ansible_connection=winrm`, `ansible_winrm_transport=ntlm` (o el valor validado por el facilitador), `ansible_port=5985|5986`

## Project

1. Crear Project `tN-starter`
2. SCM Type: Git
3. URL: la del pack
4. Branch: `main` (o la indicada)
5. Credential: `tN-scm-gitea`
6. Options: Update Revision on Launch (recomendado)
7. Guardar → **Sync**

## Criterio de éxito

- [ ] Project sync **Successful**
- [ ] Playbooks visibles bajo el Project (`playbooks/*.yml`)
- [ ] Credenciales creadas y visibles solo para el Team
- [ ] (Opcional) Job ad-hoc o JT seed de conectividad Linux OK
- [ ] Prueba WinRM: ad-hoc `win_ping` o JT seed Windows OK

## Troubleshooting rápido

| Síntoma | Comprobar |
|---------|-----------|
| Project failed | Token Gitea, URL, branch, conectividad Controller→Gitea |
| WinRM timeout | SG/firewall, puerto, `ansible_winrm_*`, credencial |
| AWS cred inválida | Reloj, políticas IAM, región |
