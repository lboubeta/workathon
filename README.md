# Workathon AAP (3 horas)

Workathon práctico para perfiles técnicos (sistemas Linux/Windows, comunicaciones, middleware, infraestructura y cloud) que empiezan a automatizar con **Ansible Automation Platform**.

**Entorno del lab:** OCP · AAP · Gitea · DevSpaces · cuenta AWS (EC2)

---

## Principio de diseño

1. **Plataforma primero.** La primera mitad se centra en configurar AAP (RBAC, credenciales, projects) con un **pack de datos facilitado**.
2. **Automatizar después.** Inventarios dinámicos, workflows con surveys/Jinja y tareas Windows.
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
- Tags AWS: `Team=N`, `OS=linux|windows`, `Role=web`, `Env=dev|prod`.

---

## Parte A — Configurar la plataforma

### Lab 1 — RBAC y organización (30 min)

Con el pack facilitado (`pack/rbac-matrix.csv`), modelar en Controller:

- Organization + Team del equipo
- Users y membership
- Asignación de roles (Execute / Use / Admin según matriz)

**Entregable:** usuario *operator* lanza jobs; *viewer* solo lee; demo de denegación de permiso; nadie ve secrets en claro.

Guía: [`docs/labs/01-rbac.md`](docs/labs/01-rbac.md)

### Lab 2 — Credenciales y Projects (35 min)

Crear y asociar credenciales tipadas; enlazar Project SCM al repo Gitea del equipo.

| Tipo | Uso |
|------|-----|
| Machine (SSH) | Hosts Linux seed |
| Machine (WinRM) | Hosts Windows seed |
| Amazon Web Services | Inventory source + módulos cloud |
| Source Control | Sync del Project desde Gitea |
| Vault (opcional) | Lookup de secretos |

**Entregable:** Project en verde; credenciales con rol **Use** para el Team (no Admin innecesario).

Guía: [`docs/labs/02-credentials-projects.md`](docs/labs/02-credentials-projects.md)

---

## Parte B — Usar la plataforma

### Lab 3 — Inventarios dinámicos (+ Windows) (40 min)

Inventory source **AWS EC2** con la credencial del Lab 2. Construir grupos dinámicos por tags/labels, incluyendo Windows en el mismo inventario (`os_windows` / `os_linux`).

**Entregable:** grupos `env_*`, `role_*`, `os_*` y compuesto (ej. `web_prod`). Ad-hoc: `ping` (Linux) + `win_ping` (Windows) contra sus grupos — nunca `all` a ciegas.

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

> **Tarea Windows obligatoria:** al menos un Job Template del workflow debe ejecutarse solo en `os_windows` (WinRM).

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
| Lab 3 | Host Windows en inventario dinámico; `win_ping` |
| Lab 4 | Nodo workflow: IIS / `win_feature` / `win_copy` / `win_service` |
| Challenge (opc.) | Path CaC que actualiza contenido en IIS |

No hay un lab “solo Windows”: todos los equipos lo tocan en el camino feliz.

---

## Pack de datos a facilitar

Ver carpeta [`pack/`](pack/) — rellenar antes del evento:

| Pack | Contenido |
|------|-----------|
| Identidad | Users, passwords temporales, matriz RBAC |
| SCM | URL repo Gitea, token, branch lab |
| Cloud | Access key / rol, región, tags `Team=N` |
| Hosts seed | 1–2 Linux + 1 Windows por equipo (o compartido) |
| Jinja starter | Ya en `starter/templates/` |
| EDA starter | Rulebook stub + instrucciones webhook |

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

## Puntuación sugerida (opcional)

| Hito | Pts |
|------|-----|
| RBAC demo (execute vs deny) | 15 |
| Creds + Project sync OK | 15 |
| Grupos dinámicos + `win_ping` | 15 |
| Workflow web Jinja + nodo Windows | 30 |
| Challenge: push Gitea → job vía EDA | 25 |
| **Total** | **100** |

---

## Estructura de este directorio

```
bankinter/workathon/
├── README.md                 ← este plan
├── docs/labs/                ← guías paso a paso por lab
├── pack/                     ← datos a rellenar por equipo
├── starter/                  ← repo plantilla (Gitea / DevSpaces)
│   ├── playbooks/
│   ├── templates/
│   ├── group_vars/
│   ├── eda/
│   ├── aac/
│   ├── ansible.cfg
│   └── devfile.yaml
└── facilitator/              ← checklist y notas internas
```

---

## Próximos pasos (facilitación)

1. Rellenar `pack/` con datos reales del lab.
2. Publicar `starter/` en Gitea y crear forks `t1`…`tN`.
3. Ejecutar [`facilitator/checklist.md`](facilitator/checklist.md) el día anterior.
4. Imprimir o compartir las guías de `docs/labs/` con cada equipo.
