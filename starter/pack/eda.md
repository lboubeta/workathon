# EDA (pack)

## Facilitator (org `facilitator`) — desplegado

| Campo | Valor |
|-------|-------|
| AAP / EDA URL | `https://bankinter-aap.apps.hetzner.calopezb.com` |
| Decision Environment | `workathon-de` (`registry.redhat.io/ansible-automation-platform-27/de-supported-rhel9:latest`) |
| SCM (Gitea) | `http://gitea-gitea.apps.hetzner.calopezb.com/user-10/facilitators.git` |
| EDA Project | `facilitator-eda-cac` (branch `main`, path `rulebooks/`) |
| Rulebook | `rulebook-cac.yml` (source `workathon_webhook`) |
| Activation | `facilitator-cac-activation` |
| Event Stream | `facilitator-gitea-webhook` |
| Event Stream URL (webhook) | `https://bankinter-aap.apps.hetzner.calopezb.com/eda-event-streams/api/eda/v1/external_event_stream/d4e1880c-57b1-4bd1-ab54-445ef00a4780/post/` |
| Auth Event Stream (Basic) | user `workathon` / password `WorkathonStream123!` |
| Credencial AAP en EDA | `facilitator-aap-controller` |
| Credencial SCM Gitea | `facilitator-gitea-scm` (`user-10`) |
| JT disparado | `facilitator-apply-cac` (org `facilitator`) |

## Equipos (plantilla)

| Campo | Valor |
|-------|-------|
| Decision Environment | `workathon-de` (reutilizar) |
| Event Stream URL | crear uno por equipo o compartir el del facilitador en demo |
| Webhook auth | Basic (facilita Gitea) o Token según lab |
| Rulebook activado | `tN-cac` o shared `rulebook-cac.yml` |
| Credencial AAP en EDA | token Controller del equipo |

## Job Template que debe existir

| JT | Playbook / acción |
|----|-------------------|
| `facilitator-apply-cac` | CaC facilitator (demo) |
| `tN-apply-cac` | Redeploy web o apply AAC |
| Alternativa | Reutilizar `tN-deploy-linux-web` |

## Filtros sugeridos en rulebook

- Repo: `tN-starter` (demo facilitator: `.*starter.*` / `facilitators`)
- Branch: `main`
- Paths: `group_vars/**`, `templates/**`, `aac/**`, `facilitator/**`

## Webhook Gitea → Event Stream

1. Gitea → Settings → Webhooks → Add Webhook (HTTP).
2. URL = Event Stream URL de arriba.
3. HTTP Basic: `workathon` / `WorkathonStream123!`.
4. Trigger: **Push**.
5. Content type: `application/json`.
