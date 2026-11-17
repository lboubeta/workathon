# Workathon AAP (3 horas)

Workathon práctico para perfiles técnicos (sistemas Linux/Windows, comunicaciones, middleware, infraestructura y cloud) que empiezan a automatizar con **Ansible Automation Platform**.

**Entorno del lab:** OCP · AAP · Gitea · DevSpaces · cuenta AWS (EC2)

---

## Principio de diseño

1. **Plataforma primero.** La primera mitad se centra en configurar AAP (RBAC; **credenciales y projects los crean los equipos**) con un **pack de datos facilitado**.
2. **Automatizar después.** Inventarios dinámicos (hostname = `Name`, grupos desde labels), workflows con surveys/Jinja y tareas Windows.
3. **Challenge al final.** DevSpaces → push a Gitea → webhook → EDA → despliegue CaC.
4. **Pre-bake obligatorio.** Lo lento (hosts seed, EE/DE base, rulebook stub, WinRM) lo prepara el facilitador; los equipos cablean y demuestran.

Cada lab deja artefactos que reutiliza el siguiente.

---

## Agenda

| Bloque | Duración | Objetivo | Dificultad |
|--------|----------|----------|------------|
| 0. Kickoff | 0:00–0:15 | Mapa de plataforma, pack de datos, reglas | Intro |
| 1. RBAC y organización | 0:15–0:45 | Orgs, teams, usuarios, roles | Esencial |
| 2. Credenciales + Projects | 0:45–1:20 | Machine/AWS/SCM/WinRM + Projects Gitea | Esencial |
| *Pausa* | ~15 min | — | — |
| 3. Inventarios dinámicos | 1:35–2:15 | AWS source, labels, grupos Linux+Windows | Esencial+ |
| 4. Workflows, surveys, Jinja | 2:15–3:10 | Despliegue web (Jinja) + nodo Windows | Intermedio |
| 5. Challenge CaC | 3:10–3:45 | DevSpaces → webhook Gitea→EDA → deploy | Avanzado |
| Wrap / demos | 3:45–4:00 | Demos cortas + cleanup | Cierre |

**Resumen de tiempo:** ~15 min kickoff · ~95 min config plataforma · ~95 min automatizar · ~35 min challenge.

---

## Formación de equipos

- **3–4 personas**, perfiles cruzados.
- Roles sugeridos dentro del equipo:
  - **Piloto plataforma** — RBAC, credenciales, projects
  - **Piloto dominio** — web / Windows / cloud
  - **Copiloto Git** — DevSpaces, commits, webhook
- Prefijo de objetos en AAP: `tN-` (ej. `t1-inventory`, `t2-deploy-web`).
- Tags AWS: `Team=N`, `OS=linux|windows`, `Role=web|db`, `Env=dev|prod`.
- **2 VMs/equipo:** `tN-linux` (Role=web) y `tN-windows` (Role=db).
- Inventario: hostname = tag `Name`; grupos = valores de labels (`linux`, `windows`, `web`, `db`).

---

## Parte A — Configurar la plataforma

### Lab 1 — RBAC y organización (30 min)

Con el pack facilitado (`starter/pack/rbac-matrix.csv`), modelar en Controller:

- Organization + Team del equipo
- Users y membership
- Asignación de roles (Execute / Use / Admin según matriz)

**Entregable:** usuario *operator* lanza jobs; *viewer* solo lee; demo de denegación de permiso; nadie ve secrets en claro.

Guía: [`docs/labs/01-rbac.md`](docs/labs/01-rbac.md)

### Lab 2 — Credenciales y Projects (35 min)

Los participantes **crean** (nombres exactos) y asocian:

| Nombre | Tipo | Uso |
|--------|------|-----|
| `tN-machine-linux` | Machine (SSH) | Hosts Linux seed |
| `tN-machine-windows` | Machine (WinRM) | Hosts Windows seed |
| `tN-aws` | Amazon Web Services | Inventory source + módulos cloud |
| `tN-scm-gitea` | Source Control | Sync del Project desde Gitea |
| `tN-starter` | Project | Repo Gitea del equipo |

**Entregable:** Project sync Successful; credenciales con rol **Use** para el Team. Puntuable vía [`facilitator/scoring/`](facilitator/scoring/).

Guía: [`docs/labs/02-credentials-projects.md`](docs/labs/02-credentials-projects.md)

---

## Parte B — Usar la plataforma

### Lab 3 — Inventarios dinámicos (+ Windows) (40 min)

Inventory `tN-aws` + source **AWS EC2** con `tN-aws`. Requisitos:

- **Hostname** = tag `Name` de la instancia (`tN-linux`, `tN-windows`)
- **Grupos** desde labels (sin prefijo): `linux`, `windows`, `web`, `db` (Linux→web, Windows→db)

**Entregable:** sync OK + ad-hoc `ping` / `win_ping` selectivos — nunca `all` a ciegas. Ejemplo source vars: [`starter/pack/inventory-source.example.yml`](starter/pack/inventory-source.example.yml).

Guía: [`docs/labs/03-dynamic-inventory.md`](docs/labs/03-dynamic-inventory.md)

### Lab 4 — Workflows, surveys y Jinja — caso servidor web (55 min)

Caso de uso concreto: desplegar un servidor web parametrizado.

| Nodo workflow | Qué hace |
|---------------|----------|
| 1. Sync inventory | Actualiza hosts/tags AWS |
| 2. Provision / baseline | Paquetes base según OS |
| 3. Render Jinja + deploy web | `templates/*.j2` → vhost + `index.html` |
| 4. Windows companion | IIS / `win_feature` / `win_copy` / `win_service` |
| 5. Smoke test | `uri` / `win_uri` |
| On-failure | Cleanup o notify (opcional) |

**Survey sugerido:** `env` (dev\|prod), `server_name`, `http_port`, `welcome_message`, `deploy_windows` (bool). En **prod**: nodo de aprobación antes del deploy.

**Jinja facilitado** en `starter/templates/` — los equipos completan tasks (`template`, `service`, handlers), no diseñan las plantillas desde cero.

> **Tarea Windows obligatoria:** al menos un Job Template del workflow debe ejecutarse solo en `windows` (WinRM).

Guía: [`docs/labs/04-workflow-web-jinja.md`](docs/labs/04-workflow-web-jinja.md)

---

## Parte C — Challenge

### Challenge — DevSpaces + webhook Gitea → EDA (CaC) (35 min)

Cambio en Git dispara automatización:

1. **Edit** en DevSpaces (fork del starter)
2. **Push** a Gitea
3. **Webhook** Gitea → Event Stream EDA
4. **Rulebook** filtra repo/branch/path y lanza Job Template
5. **CaC apply** — JT aplica config

| Opción | Descripción |
|--------|-------------|
| **A — App config** | Cambiar `welcome_message` / vhost en Git → redeploy web (Linux y/o IIS) |
| **B — AAP as Code** | Cambiar YAML de definición → job aplica config vía collection controller/gateway |

Guía: [`docs/labs/05-challenge-cac-eda.md`](docs/labs/05-challenge-cac-eda.md)

---

## Windows — integración transversal

| Dónde | Tarea |
|-------|-------|
| Lab 2 | Credencial Machine WinRM + prueba de conectividad |
| Lab 3 | Host en grupo `windows`; `win_ping` |
| Lab 4 | Nodo workflow: IIS / `win_feature` / `win_copy` / `win_service` |
| Challenge (opc.) | Path CaC que actualiza contenido en IIS |

No hay un lab “solo Windows”: todos los equipos lo tocan en el camino feliz.

---

## Starter + pack (mismo repo Gitea)

Todo lo que el equipo clona vive en [`starter/`](starter/):

| Path | Rol |
|------|-----|
| [`starter/`](starter/) | Playbooks, templates Jinja, group_vars, EDA, AAC, Devfile |
| [`starter/pack/`](starter/pack/) | Datos del lab a rellenar (RBAC, SCM, AWS, hosts, EDA URLs) |

Rellenar el pack **antes** del evento:

| Pack | Contenido |
|------|-----------|
| Identidad | Users, passwords temporales, matriz RBAC |
| SCM | URL repo Gitea, token, branch lab |
| Cloud | Access key / rol, región, tags `Team=N` |
| Hosts seed | 2 VMs/equipo: Linux web + Windows db |
| Jinja / EDA | Ya en `starter/templates/` y `starter/eda/` |

---

## Uso del entorno

| Componente | Rol |
|------------|-----|
| AAP Controller | Inventarios, creds, RBAC, JT, workflows |
| AAP Hub / registry | Collections + EE images |
| EDA Controller | Rulebooks y activaciones (challenge) |
| Gitea | SCM de playbooks y definiciones CaC |
| DevSpaces | IDE en OCP; edit/commit |
| OCP | Host de AAP/DevSpaces |
| AWS EC2 | Inventory source + target de jobs |

---

## Pre-bake del facilitador

Checklist: [`facilitator/checklist.md`](facilitator/checklist.md)

| Área | Dejar listo |
|------|-------------|
| RBAC | Orgs “vacías” + users; ellos asignan roles |
| Gitea | Repo starter (este árbol) por equipo / fork |
| AWS | EC2 Linux+Windows tagged; SG SSH/WinRM desde Controllers |
| Windows | WinRM validado; usuario ansible |
| EDA | DE, Event Stream URL, rulebook stub, JT `apply-cac` |
| DevSpaces | Devfile → clone starter |

> **No subestimar WinRM/red.** Validar conectividad Windows antes del evento.

---

## Puntuación

| Hito | Pts | Automatizado |
|------|-----|--------------|
| RBAC demo (execute vs deny) | 15 | Manual / demo |
| Creds + Project sync OK (Lab 2) | 15 | [`facilitator/scoring/`](facilitator/scoring/) |
| Inventario Name + grupos + membresía web/db (Lab 3) | 15 | [`facilitator/scoring/`](facilitator/scoring/) |
| Workflow web Jinja + nodo Windows | 30 | Manual / demo |
| Challenge: push Gitea → job vía EDA | 25 | Manual / demo |
| **Total** | **100** |

```bash
export CONTROLLER_HOST=https://<controller> CONTROLLER_TOKEN=...
python3 facilitator/scoring/score_teams.py
```

---

## Estructura de este directorio

```
bankinter/workathon/
├── README.md                 ← este plan
├── docs/labs/                ← guías paso a paso por lab
├── starter/                  ← repo plantilla (Gitea / DevSpaces)
│   ├── pack/                 ← datos a rellenar por equipo
│   ├── playbooks/
│   ├── templates/
│   ├── group_vars/
│   ├── eda/
│   ├── aac/
│   ├── ansible.cfg
│   └── devfile.yaml
├── terraform/                ← 2 VMs/equipo: linux + windows (eu-west-1)
└── facilitator/              ← checklist, scoring labs 2–3, CaC org `facilitator`
```

Infra de lab: ver [`terraform/README.md`](terraform/README.md) (`terraform apply` → Name/OS/Role para inventario dinámico).

---

## Próximos pasos (facilitación)

1. Rellenar [`starter/pack/`](starter/pack/) con datos reales del lab.
2. Publicar [`starter/`](starter/) (incluye pack) en Gitea y crear forks `t1`…`tN`.
3. Ejecutar [`facilitator/checklist.md`](facilitator/checklist.md) el día anterior.
4. Imprimir o compartir las guías de `docs/labs/` con cada equipo.
