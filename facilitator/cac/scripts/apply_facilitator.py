#!/usr/bin/env python3
"""Apply facilitator CaC to AAP (Gateway + Controller API paths).

Env:
  CONTROLLER_HOST   https://bankinter-aap.apps.hetzner.calopezb.com
  CONTROLLER_TOKEN  OAuth token
  AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY
  FACILITATOR_STARTER_URL  presigned archive URL
  INSTANCE_PASSWORD  default Workathon123!
  VERIFY_SSL=0
"""

from __future__ import annotations

import json
import os
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
VARS_FILE = ROOT / "vars" / "facilitator.yml"


def env_bool(name: str, default: bool = False) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() not in {"0", "false", "no", "off"}


class Api:
    def __init__(self, host: str, token: str, verify: bool):
        self.host = host.rstrip("/")
        self.token = token
        self.ctx = None if verify else ssl._create_unverified_context()

    def _req(self, method: str, path: str, body: dict | None = None) -> dict | list | None:
        url = f"{self.host}{path}"
        data = None if body is None else json.dumps(body).encode()
        req = urllib.request.Request(
            url,
            data=data,
            method=method,
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
                "Accept": application_json(),
            },
        )
        try:
            with urllib.request.urlopen(req, context=self.ctx, timeout=120) as resp:
                raw = resp.read().decode()
                return json.loads(raw) if raw else None
        except urllib.error.HTTPError as e:
            err = e.read().decode(errors="replace")
            raise RuntimeError(f"{method} {path} -> HTTP {e.code}: {err[:500]}") from e

    def get(self, path: str, params: dict | None = None):
        qs = f"?{urllib.parse.urlencode(params)}" if params else ""
        return self._req("GET", path + qs)

    def get_all(self, path: str, params: dict | None = None) -> list:
        params = dict(params or {})
        params.setdefault("page_size", 200)
        data = self.get(path, params)
        results = list(data.get("results", []))
        while data.get("next"):
            nxt = data["next"]
            if nxt.startswith("http"):
                parsed = urllib.parse.urlparse(nxt)
                data = self.get(parsed.path, dict(urllib.parse.parse_qsl(parsed.query)))
            else:
                data = self.get(nxt)
            results.extend(data.get("results", []))
        return results

    def post(self, path: str, body: dict):
        return self._req("POST", path, body)

    def patch(self, path: str, body: dict):
        return self._req("PATCH", path, body)

    def find_one(self, path: str, name: str, extra: dict | None = None):
        params = {"name": name}
        if extra:
            params.update(extra)
        rows = self.get_all(path, params)
        for r in rows:
            if r.get("name") == name:
                return r
        return None

    def upsert(self, list_path: str, name: str, body: dict, extra_lookup: dict | None = None):
        existing = self.find_one(list_path, name, extra_lookup)
        if existing:
            print(f"  update {list_path} id={existing['id']} name={name}")
            return self.patch(f"{list_path}{existing['id']}/", body)
        print(f"  create {list_path} name={name}")
        return self.post(list_path, body)


def application_json() -> str:
    return "application/json"


def wait_project(api: Api, project_id: int, timeout: int = 300) -> dict:
    deadline = time.time() + timeout
    while time.time() < deadline:
        p = api.get(f"/api/controller/v2/projects/{project_id}/")
        status = (p.get("status") or "").lower()
        print(f"  project status={status}")
        if status in {"successful", "failed", "error", "canceled"}:
            return p
        time.sleep(5)
    raise TimeoutError(f"project {project_id} sync timeout")


def wait_inventory_update(api: Api, source_id: int, timeout: int = 300) -> dict:
    # launch update
    api.post(f"/api/controller/v2/inventory_sources/{source_id}/update/", {})
    deadline = time.time() + timeout
    while time.time() < deadline:
        src = api.get(f"/api/controller/v2/inventory_sources/{source_id}/")
        status = (src.get("status") or "").lower()
        print(f"  inventory_source status={status}")
        if status in {"successful", "failed", "error", "canceled"}:
            return src
        time.sleep(5)
    raise TimeoutError(f"inventory source {source_id} update timeout")


def load_vars() -> dict:
    data = yaml.safe_load(VARS_FILE.read_text())
    # Resolve simple jinja-ish defaults used in YAML
    prefix = data.get("prefix", "facilitator")
    data["prefix"] = prefix
    data["org_name"] = os.environ.get("ORG_NAME", data.get("org_name", "facilitator"))
    data["team_name"] = data.get("team_name", "facilitator-team")
    data["project_name"] = f"{prefix}-starter"
    data["inventory_name"] = f"{prefix}-aws"
    data["inventory_source_name"] = f"{prefix}-ec2"
    data["credential_names"] = {
        "scm": f"{prefix}-scm",
        "machine_linux": f"{prefix}-machine-linux",
        "machine_windows": f"{prefix}-machine-windows",
        "aws": f"{prefix}-aws",
    }
    data["project_scm_url"] = os.environ.get("FACILITATOR_STARTER_URL", "").strip().strip("'\"")
    data["aws_access_key"] = os.environ.get("AWS_ACCESS_KEY_ID", "")
    data["aws_secret_key"] = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
    data["machine_password"] = os.environ.get("INSTANCE_PASSWORD", "Workathon123!")
    data["machine_username"] = data.get("machine_username", "ansible")
    data["job_templates"] = [
        {
            "name": f"{prefix}-baseline",
            "playbook": "playbooks/baseline.yml",
            "limit": "",
            "description": "Baseline OS (linux+windows)",
            "creds": ["machine_linux"],
        },
        {
            "name": f"{prefix}-deploy-linux-web",
            "playbook": "playbooks/site_linux_web.yml",
            "limit": "linux:&web",
            "description": "Deploy web on linux/web",
            "creds": ["machine_linux"],
        },
        {
            "name": f"{prefix}-deploy-windows-iis",
            "playbook": "playbooks/site_windows_iis.yml",
            "limit": "windows:&db",
            "description": "Windows companion (IIS) on windows/db",
            "creds": ["machine_windows"],
        },
        {
            "name": f"{prefix}-smoke",
            "playbook": "playbooks/smoke.yml",
            "limit": "",
            "description": "HTTP smoke test",
            "creds": ["machine_linux"],
        },
    ]
    return data


def main() -> int:
    host = os.environ.get("CONTROLLER_HOST")
    token = os.environ.get("CONTROLLER_TOKEN")
    if not host or not token:
        print("CONTROLLER_HOST and CONTROLLER_TOKEN required", file=sys.stderr)
        return 2

    cfg = load_vars()
    if not cfg["project_scm_url"]:
        print("FACILITATOR_STARTER_URL required", file=sys.stderr)
        return 2
    if not cfg["aws_access_key"] or not cfg["aws_secret_key"]:
        print("AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY required", file=sys.stderr)
        return 2

    api = Api(host, token, verify=env_bool("VERIFY_SSL", False))
    org_name = cfg["org_name"]
    prefix = cfg["prefix"]

    print(f"== Organization {org_name}")
    org = api.upsert(
        "/api/gateway/v1/organizations/",
        org_name,
        {"name": org_name, "description": "Workathon design validation sandbox"},
    )
    # Gateway returns object; Controller org id may match by name
    org_ctrl = api.find_one("/api/controller/v2/organizations/", org_name)
    if not org_ctrl:
        # wait briefly for sync gateway→controller
        for _ in range(10):
            time.sleep(2)
            org_ctrl = api.find_one("/api/controller/v2/organizations/", org_name)
            if org_ctrl:
                break
    if not org_ctrl:
        raise RuntimeError(f"Organization {org_name} not visible on Controller API yet")
    org_id = org_ctrl["id"]
    print(f"  controller org id={org_id}")

    print(f"== Team {cfg['team_name']}")
    api.upsert(
        "/api/gateway/v1/teams/",
        cfg["team_name"],
        {
            "name": cfg["team_name"],
            "organization": org.get("id") or org_id,
            "description": "Facilitator operators",
        },
        extra_lookup={"organization": org.get("id") or org_id},
    )

    # Credential types
    ctypes = {c["name"]: c["id"] for c in api.get_all("/api/controller/v2/credential_types/", {"managed": "true"})}
    # also unmanaged
    for c in api.get_all("/api/controller/v2/credential_types/"):
        ctypes.setdefault(c["name"], c["id"])

    print("== Credentials")
    cred_ids = {}
    machine_type = ctypes["Machine"]
    aws_type = ctypes["Amazon Web Services"]
    scm_type = ctypes["Source Control"]

    for key, name, ctype, inputs in [
        (
            "machine_linux",
            cfg["credential_names"]["machine_linux"],
            machine_type,
            {"username": cfg["machine_username"], "password": cfg["machine_password"]},
        ),
        (
            "machine_windows",
            cfg["credential_names"]["machine_windows"],
            machine_type,
            {"username": cfg["machine_username"], "password": cfg["machine_password"]},
        ),
        (
            "aws",
            cfg["credential_names"]["aws"],
            aws_type,
            {"username": cfg["aws_access_key"], "password": cfg["aws_secret_key"]},
        ),
        (
            "scm",
            cfg["credential_names"]["scm"],
            scm_type,
            {"username": "unused", "password": "unused"},
        ),
    ]:
        body = {
            "name": name,
            "organization": org_id,
            "credential_type": ctype,
            "inputs": inputs,
            "description": f"Facilitator CaC ({key})",
        }
        obj = api.upsert("/api/controller/v2/credentials/", name, body, extra_lookup={"organization": org_id})
        cred_ids[key] = obj["id"]

    print(f"== Project {cfg['project_name']}")
    proj_body = {
        "name": cfg["project_name"],
        "description": "Starter playbooks + scoring (archive SCM)",
        "organization": org_id,
        "scm_type": "archive",
        "scm_url": cfg["project_scm_url"],
        "scm_update_on_launch": True,
        "scm_delete_on_update": True,
    }
    project = api.upsert("/api/controller/v2/projects/", cfg["project_name"], proj_body, {"organization": org_id})
    # trigger update
    try:
        api.post(f"/api/controller/v2/projects/{project['id']}/update/", {})
    except RuntimeError as e:
        print(f"  update launch note: {e}")
    project = wait_project(api, project["id"])
    if (project.get("status") or "").lower() != "successful":
        raise RuntimeError(f"Project sync failed: {project.get('status')}")

    # playbooks check
    pbs = api.get(f"/api/controller/v2/projects/{project['id']}/playbooks/")
    print(f"  playbooks={pbs}")

    print(f"== Inventory {cfg['inventory_name']}")
    inv = api.upsert(
        "/api/controller/v2/inventories/",
        cfg["inventory_name"],
        {
            "name": cfg["inventory_name"],
            "description": "Dynamic EC2 — Name hostnames, OS/Role groups",
            "organization": org_id,
        },
        {"organization": org_id},
    )

    source_vars = cfg.get("inventory_source_vars")
    if isinstance(source_vars, str):
        # already YAML text
        pass
    else:
        source_vars = yaml.safe_dump(source_vars)

    print(f"== Inventory source {cfg['inventory_source_name']}")
    src_body = {
        "name": cfg["inventory_source_name"],
        "inventory": inv["id"],
        "source": "ec2",
        "credential": cred_ids["aws"],
        "source_vars": source_vars,
        "source_regions": cfg.get("aws_region", "eu-west-1"),
        "update_on_launch": True,
        "overwrite": True,
        "overwrite_vars": True,
    }
    # inventory sources list is nested; also top-level exists
    existing_src = None
    for s in api.get_all(f"/api/controller/v2/inventories/{inv['id']}/inventory_sources/"):
        if s["name"] == cfg["inventory_source_name"]:
            existing_src = s
            break
    if existing_src:
        print(f"  update inventory_source id={existing_src['id']}")
        src = api.patch(f"/api/controller/v2/inventory_sources/{existing_src['id']}/", src_body)
    else:
        print("  create inventory_source")
        src = api.post("/api/controller/v2/inventory_sources/", src_body)

    src = wait_inventory_update(api, src["id"])
    if (src.get("status") or "").lower() != "successful":
        raise RuntimeError(f"Inventory sync failed: {src.get('status')}")

    # Ensure windows group vars (WinRM) — group may exist from keyed_groups
    print("== Windows group vars")
    groups = {g["name"]: g for g in api.get_all(f"/api/controller/v2/inventories/{inv['id']}/groups/")}
    win_vars = yaml.safe_dump(
        {
            "ansible_connection": "winrm",
            "ansible_winrm_transport": "ntlm",
            "ansible_port": 5985,
            "ansible_winrm_server_cert_validation": "ignore",
        }
    )
    if "windows" in groups:
        api.patch(f"/api/controller/v2/groups/{groups['windows']['id']}/", {"variables": win_vars})
    else:
        api.post(
            "/api/controller/v2/groups/",
            {"name": "windows", "inventory": inv["id"], "variables": win_vars},
        )

    # EE
    ees = {e["name"]: e["id"] for e in api.get_all("/api/controller/v2/execution_environments/")}
    ee_id = ees.get("Default execution environment")

    print("== Job templates")
    for jt in cfg["job_templates"]:
        body = {
            "name": jt["name"],
            "description": jt["description"],
            "job_type": "run",
            "inventory": inv["id"],
            "project": project["id"],
            "playbook": jt["playbook"],
            "limit": jt.get("limit") or "",
            "ask_limit_on_launch": True,
            "ask_variables_on_launch": True,
            "execution_environment": ee_id,
        }
        obj = api.upsert("/api/controller/v2/job_templates/", jt["name"], body)
        # associate credentials
        for ck in jt.get("creds", []):
            cid = cred_ids[ck]
            try:
                api.post(
                    f"/api/controller/v2/job_templates/{obj['id']}/credentials/",
                    {"id": cid},
                )
                print(f"  associated cred {ck} -> {jt['name']}")
            except RuntimeError as e:
                if "already" in str(e).lower() or "400" in str(e):
                    print(f"  cred {ck} already on {jt['name']} ({e})")
                else:
                    raise

    hosts = [h["name"] for h in api.get_all(f"/api/controller/v2/inventories/{inv['id']}/hosts/")]
    groups = [g["name"] for g in api.get_all(f"/api/controller/v2/inventories/{inv['id']}/groups/")]
    print("== Done")
    print(f"  hosts={sorted(hosts)}")
    print(f"  groups={sorted(groups)}")
    print("  Next: python3 scripts/validate_facilitator.py")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
