# Checklist facilitador — día anterior

## Identidad / RBAC

- [ ] Orgs `tN-org` creadas (o plantilla)
- [ ] Users del `pack/rbac-matrix.csv` creados con passwords temporales
- [ ] Documentada matriz de roles (los equipos asignan en Lab 1)
- [ ] Usuario facilitador System/Org Admin

## Gitea

- [ ] Repo base `workathon-starter` con contenido de `starter/`
- [ ] Forks `t1-starter` … `tN-starter`
- [ ] Token SCM read para Projects
- [ ] Users DevSpaces con permiso push a su fork

## AWS

- [ ] IAM mínimo para inventory + ec2 describe/tags
- [ ] `terraform apply` en `terraform/` → 2 VMs/equipo: `tN-linux` + `tN-windows` (`Team`, `OS`, `Role=web|db`, `Env`)
- [ ] Password lab `Ansible123!` operativa (SSH + WinRM); Windows user-data terminado
- [ ] Security Groups: SSH/WinRM/HTTP/RDP (lab) o restringir `allowed_cidr`
- [ ] Cuota / límite comunicado a equipos
- [ ] Tras el evento: `terraform destroy`
- [ ] Scoring labs 2–3 listo: `facilitator/scoring/score_teams.py` + token Controller

## Windows

- [ ] WinRM escuchando; prueba `win_ping` desde un EE de AAP
- [ ] Usuario `ansible` + pertenencia a grupo adecuado
- [ ] Documentado HTTP vs HTTPS y transport (`ntlm` / `credssp` / `basic`)

## AAP Controllers

- [ ] Execution Environment por defecto con collections: `amazon.aws`, `ansible.windows`, `ansible.controller` (si AAC)
- [ ] (Opcional) Workflow seed `tN-deploy-web` esqueleto
- [ ] JT placeholder para demo RBAC Lab 1

## EDA

- [ ] Decision Environment publicado
- [ ] Event Stream creado; URL + secret en `pack/eda.md`
- [ ] Rulebook stub importado (`starter/eda/rulebook-cac.yml`)
- [ ] Credencial AAP token para `run_job_template`
- [ ] Activation de prueba recibe un webhook sintético

## DevSpaces

- [ ] Devfile validado (clone + ansible + git)
- [ ] Cuota de workspaces suficiente

## Día del evento

- [ ] Pack PDF/impreso o enlace por equipo
- [ ] Credenciales de emergencia rotuladas
- [ ] JT de cleanup AWS listo para el wrap
- [ ] Canal de soporte (chat/sala)

## Riesgos conocidos

| Riesgo | Mitigación |
|--------|------------|
| WinRM rompe el ritmo | Validar la víspera; JT seed Windows |
| Build EE lento | No es camino crítico en v2; EE ya publicado |
| Lab 4 justos 55 min | Workflow + Jinja pre-esqueleto |
| Webhook EDA fallido | Activation pre-creada; equipos solo conectan Gitea |
