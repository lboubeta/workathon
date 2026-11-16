# EDA (pack)

| Campo | Valor |
|-------|-------|
| EDA Controller URL | `https://eda.EXAMPLE/` |
| Decision Environment | `workathon-de` (pre-publicado) |
| Event Stream URL (webhook) | `https://eda.EXAMPLE/api/.../CHANGE_ME` |
| Webhook secret | `CHANGE_ME` |
| Rulebook activado | `tN-cac` o shared `workathon-cac` |
| AAP Contoller host (para run_job_template) | |
| Credencial AAP en EDA | `eda-aap-token` (facilitador) |

## Job Template que debe existir

| JT | Playbook / acción |
|----|-------------------|
| `tN-apply-cac` | Redeploy web o apply AAC |
| Alternativa | Reutilizar `tN-deploy-linux-web` |

## Filtros sugeridos en rulebook

- Repo: `tN-starter`
- Branch: `main`
- Paths: `group_vars/**`, `templates/**`, `aac/**`
