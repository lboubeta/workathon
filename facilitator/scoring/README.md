# Scoring — Labs 2 y 3

Automatismos para comprobar que cada equipo ha **creado** credenciales + project y un **inventario dinámico** con:

- hostname = tag EC2 `Name`
- grupos desde labels: `linux` / `windows` / `web` / `db`
- 2 VMs/equipo: `tN-linux` (Role=web) y `tN-windows` (Role=db)

## Rúbrica (30 pts)

| Lab | Hito | Pts |
|-----|------|-----|
| 2 | `tN-scm-gitea` | 3 |
| 2 | `tN-machine-linux` | 3 |
| 2 | `tN-machine-windows` | 3 |
| 2 | `tN-aws` | 3 |
| 2 | Project `tN-starter` sync successful | 3 |
| 3 | Inventory `tN-aws` | 2 |
| 3 | Hostnames = Name (`tN-linux`, `tN-windows`) | 4 |
| 3 | Grupo `linux` | 1 |
| 3 | Grupo `windows` | 1 |
| 3 | Grupo `web` | 1 |
| 3 | Grupo `db` | 1 |
| 3 | Membresía `tN-linux` ∈ linux∩web | 2 |
| 3 | Membresía `tN-windows` ∈ windows∩db | 3 |
| | **Total labs 2–3** | **30** |

Definición machine-readable: [`scorecard.yml`](scorecard.yml).

## Ejecutar (CLI)

```bash
export CONTROLLER_HOST=https://<controller>
export CONTROLLER_TOKEN=<oauth-token>
# opcional: TEAMS=1,2,3  VERIFY_SSL=0

cd bankinter/workathon/facilitator/scoring
python3 score_teams.py
python3 score_teams.py --json
```

O con Ansible:

```bash
ansible-playbook score_teams.yml \
  -e controller_host="$CONTROLLER_HOST" \
  -e controller_token="$CONTROLLER_TOKEN"
```

## Qué comprueba (y qué no)

- **Sí:** existencia de objetos por nombre exacto, sync del Project, hostnames, grupos y **membresía** host→grupo tras el sync del inventory source.
- **No:** `ping`/`win_ping` en vivo (validar a mano o con JT seed). El scoring API no depende de WinRM desde el portátil del facilitador.

## JT opcional en Controller

Crear Job Template `facilitator-score-labs` → playbook `score_teams.yml` (Project con este repo o copia), credencial Controller token en extra vars / credential type.
