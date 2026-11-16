# Lab 1 — RBAC y organización (30 min)

## Objetivo

Modelar en AAP Controller la organización del equipo usando el pack facilitado. Demostrar que los permisos funcionan (execute vs deny).

## Datos del pack

- `pack/rbac-matrix.csv` — usuarios, teams y roles
- `pack/team-sheet.md` — nombre de Org/Team y prefijo `tN-`

## Pasos

1. Iniciar sesión en Controller con el usuario facilitador (o el user admin temporal del equipo).
2. Verificar/crear **Organization** `tN-org` y **Team** `tN-team`.
3. Añadir los usuarios del pack al Team.
4. Asignar roles según la matriz:
   - *operator* → Job Template **Execute**, Inventory **Use**, Credential **Use**
   - *viewer* → Organization / Job **Read**
   - *lead* → Team **Admin** (o Execute + Inventory Admin, según matriz)
5. **No** asignar System Administrator a usuarios de equipo.

## Criterio de éxito

- [ ] Login como *operator*: puede ver y lanzar (cuando existan) JT del equipo.
- [ ] Login como *viewer*: puede leer, **no** puede lanzar ni editar.
- [ ] Demo de denegación capturada (screenshot o anotación).
- [ ] Ningún usuario de equipo puede ver el secret de una credencial en claro.

## Notas

Los Job Templates se crean en labs posteriores; en este lab basta con asignar roles sobre objetos seed que el facilitador haya dejado (inventory vacío, JT placeholder) o documentar la asignación para aplicar en Lab 2–4.
