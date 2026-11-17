# Lab 4 — Workflows, surveys y Jinja (caso web) (55 min)

## Objetivo

Orquestar el despliegue de un servidor web parametrizado: survey → Jinja → Linux web + nodo Windows (IIS) → smoke test.

## Artefactos del starter

| Path | Uso |
|------|-----|
| `playbooks/site_linux_web.yml` | Deploy nginx/httpd + template Jinja |
| `playbooks/site_windows_iis.yml` | IIS feature + contenido |
| `playbooks/smoke.yml` | Comprobación HTTP |
| `playbooks/baseline.yml` | Paquetes base |
| `templates/nginx.conf.j2` | Vhost Linux |
| `templates/index.html.j2` | Página de bienvenida |
| `templates/iis_web.config.j2` | Config auxiliar Windows (opcional) |

## Job Templates a crear

Prefijo `tN-`:

1. `tN-sync-inventory` — Update inventory (o mark source update)
2. `tN-baseline` — playbook `baseline.yml` · cred Linux/Windows según limit
3. `tN-deploy-linux-web` — `site_linux_web.yml` · limit `linux` o `web` · cred SSH
4. `tN-deploy-windows-iis` — `site_windows_iis.yml` · limit `windows` o `db` · cred WinRM
5. `tN-smoke` — `smoke.yml`

Prompt on launch / survey en el **Workflow** (no hace falta survey en cada JT si pasáis `workflow_job_extra_vars`).

## Survey del Workflow

| Variable | Tipo | Valores |
|----------|------|---------|
| `env` | multiple choice | `dev`, `prod` |
| `server_name` | text | ej. `web-tN.lab.local` |
| `http_port` | integer | `80` / `8080` |
| `welcome_message` | text | mensaje en `index.html.j2` |
| `deploy_windows` | bool | true/false |

## Workflow `tN-deploy-web`

```
[sync inventory]
        │
        ▼
   [baseline]
        │
        ├──────────────────────┐
        ▼                      ▼
[deploy-linux-web]    [deploy-windows-iis]  ← solo si deploy_windows
        │                      │
        └──────────┬───────────┘
                   ▼
               [smoke]
                   │
            (on failure → cleanup/notify opcional)
```

Para **prod**: insertar nodo de **Approval** antes de `deploy-linux-web`.

## Tasks que deben completar los equipos

En `site_linux_web.yml` hay `# TODO` para:

- Usar módulo `template` con `nginx.conf.j2` e `index.html.j2`
- Handler `reload nginx` / `reload httpd`
- Asegurar servicio enabled + started

En `site_windows_iis.yml`:

- `win_feature` para IIS
- `win_copy` o `win_template` del contenido
- `win_service` W3SVC started

## Criterio de éxito

- [ ] Workflow lanzado desde survey
- [ ] Página web Linux muestra `welcome_message` renderizado
- [ ] Nodo Windows ejecutado con éxito (si `deploy_windows=true`)
- [ ] Smoke test en verde
- [ ] En `env=prod`, el approval detiene el flujo hasta aceptar

## Tip de tiempo

No reinventéis el grafo: clonad el workflow seed del facilitador si existe y completad nodos/TODOs.
