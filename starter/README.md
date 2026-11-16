# workathon-starter

Repo plantilla para el Workathon AAP (Bankinter). Se publica en Gitea y cada equipo trabaja sobre su fork (`tN-starter`).

## Contenido

| Path | Descripción |
|------|-------------|
| `playbooks/` | Baseline, web Linux (Jinja), IIS Windows, smoke, apply-cac |
| `templates/` | `index.html.j2`, nginx/httpd, IIS web.config |
| `group_vars/` | Defaults + vars WinRM para `os_windows` |
| `eda/rulebook-cac.yml` | Esqueleto webhook → JT |
| `aac/job_templates.yml` | Ejemplo AAP as Code (challenge B) |
| `devfile.yaml` | DevSpaces |

## Uso local / DevSpaces

```bash
ansible-playbook --syntax-check playbooks/site_linux_web.yml
```

En AAP: Project SCM → este repo → Job Templates según `docs/labs/` del workathon.

## Variables clave (survey)

`env`, `server_name`, `http_port`, `welcome_message`, `deploy_windows`
