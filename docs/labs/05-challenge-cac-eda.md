# Challenge — DevSpaces + webhook Gitea → EDA (CaC) (35 min)

## Objetivo

Demostrar Configuration as Code: un **push a Gitea** dispara un **rulebook EDA** que lanza un Job Template en AAP y aplica el cambio.

## Flujo

```
DevSpaces ──commit──► Gitea ──webhook──► EDA Event Stream
                                              │
                                              ▼
                                         Rulebook
                                              │
                                              ▼
                                    AAP Job Template
                                         apply-cac
```

## Opción A — App config (recomendada)

1. Abrir DevSpaces con el `devfile.yaml` del starter.
2. Editar `group_vars/all.yml` (o `templates/index.html.j2`) — cambiar `welcome_message` / texto.
3. Commit + push a la branch del lab.
4. Verificar en EDA que el evento llega y la regla dispara.
5. Comprobar job `tN-apply-cac` (o `tN-deploy-linux-web`) en Controller.
6. Recargar la web: el nuevo mensaje debe verse.

## Opción B — AAP as Code

1. Editar `aac/job_templates.yml` (definición deseada).
2. Push a Gitea.
3. EDA lanza JT que aplica el YAML con la collection `ansible.controller` / gateway.
4. Verificar en UI que el JT/survey default cambió.

## Webhook Gitea

1. En el repo Gitea → Settings → Webhooks → Add Webhook.
2. URL: Event Stream del pack (`starter/pack/eda.md`).
3. Secret: el facilitador os lo da.
4. Event: **Push**.
5. Probar con un commit vacío si hace falta.

## Rulebook

El esqueleto está en `starter/eda/rulebook-cac.yml`. El facilitador habrá publicado una Decision Environment y una regla base; vuestro trabajo es:

- Apuntar el webhook
- Ajustar filtros `repo` / `branch` / `paths` a vuestro equipo
- Verificar que `run_job_template` usa el nombre `tN-...` correcto

## Criterio de éxito

- [ ] Push desde DevSpaces visible en Gitea
- [ ] Evento recibido en EDA (activation running)
- [ ] Job disparado automáticamente en Controller
- [ ] Cambio aplicado (web o definición AAP)

## Si el tiempo aprieta

Priorizad Opción A con rulebook ya activado por el facilitador: solo conectad el webhook y haced el push demostrable.
