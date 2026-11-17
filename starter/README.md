# workathon-starter

Repo plantilla para el Workathon AAP (Bankinter). Se publica en Gitea y cada equipo trabaja sobre su fork (`tN-starter`).

Incluye **playbooks/templates** y el **pack de datos** del lab en el mismo árbol.

## Contenido

| Path | Descripción |
|------|-------------|
| [`pack/`](pack/) | Datos facilitados: RBAC, SCM, AWS, hosts, EDA (rellenar antes del evento) |
| `playbooks/` | Baseline, web Linux (Jinja), IIS Windows, smoke, apply-cac |
| `templates/` | `index.html.j2`, nginx/httpd, IIS web.config |
| `group_vars/` | Defaults + vars WinRM para grupo `windows` |
| `eda/rulebook-cac.yml` | Esqueleto webhook → JT |
| `aac/job_templates.yml` | Ejemplo AAP as Code (challenge B) |
| `devfile.yaml` | DevSpaces |

## Pack (datos del lab)

Ver [`pack/README.md`](pack/README.md). Ficheros clave:

| Fichero | Uso |
|---------|-----|
| `pack/rbac-matrix.csv` | Lab 1 — users/roles |
| `pack/team-sheet.md` | Org/Team y prefijo `tN-` |
| `pack/scm.md` / `pack/cloud.md` / `pack/hosts.md` | Lab 2 — creds + project |
| `pack/inventory-source.example.yml` | Lab 3 — source vars EC2 |
| `pack/eda.md` | Challenge — Event Stream |

Plan general del workathon: [`../README.md`](../README.md).

## Uso local / DevSpaces

```bash
ansible-playbook --syntax-check playbooks/site_linux_web.yml
```

En AAP: Project SCM → este repo → Job Templates según `docs/labs/` del workathon.

## Variables clave (survey)

`env`, `server_name`, `http_port`, `welcome_message`, `deploy_windows`
