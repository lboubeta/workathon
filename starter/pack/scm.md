# SCM / Gitea (pack)

## Facilitator (desplegado)

| Campo | Valor |
|-------|-------|
| Gitea URL | `http://gitea-gitea.apps.hetzner.calopezb.com/` |
| Repo | [`user-10/facilitators`](http://gitea-gitea.apps.hetzner.calopezb.com/user-10/facilitators) |
| Clone URL | `http://gitea-gitea.apps.hetzner.calopezb.com/user-10/facilitators.git` |
| Branch | `main` |
| Credencial AAP/EDA | `facilitator-gitea-scm` (`user-10`) |

Projects apuntando a este repo (git, **no** S3/archive):

| Project | Producto | Notas |
|---------|----------|-------|
| `facilitator-starter` | Controller | playbooks bajo `starter/playbooks/` |
| `facilitator-eda-cac` | EDA | rulebooks bajo `rulebooks/` |

## Equipos (plantilla)

| Campo | Valor |
|-------|-------|
| Gitea URL | `http://gitea-gitea.apps.hetzner.calopezb.com/` |
| Org/user | `workathon` / `user-N` |
| Repo equipo | `tN-starter` |
| Clone URL | `http://gitea-gitea.apps.hetzner.calopezb.com/<user>/tN-starter.git` |
| Branch | `main` |
| Deploy user / token | Credencial **Source Control** en AAP |
| Webhook → EDA | Event Stream del pack (`eda.md`) |

## Notas

- El token solo necesita lectura del repo para el Project; para el challenge, el usuario de DevSpaces necesita push.
- Credencial AAP tipo **Source Control**: username + password/token.
