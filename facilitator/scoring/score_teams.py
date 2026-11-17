#!/usr/bin/env python3
"""Score workathon labs 2–3 against AAP Controller API.

Participants must create credentials + project (lab 2) and a dynamic
inventory whose hostnames are EC2 Name tags and groups come from OS/Role
labels (lab 3). Seed: 2 VMs/team — Linux=web, Windows=db.

Env:
  CONTROLLER_HOST   e.g. https://controller.example.com
  CONTROLLER_TOKEN  OAuth2 token (or CONTROLLER_USERNAME + CONTROLLER_PASSWORD)
  TEAMS             optional, default 1,2,3
  VERIFY_SSL        default true; set 0/false to disable

Usage:
  export CONTROLLER_HOST=... CONTROLLER_TOKEN=...
  python3 score_teams.py
  python3 score_teams.py --json > scores.json
"""

from __future__ import annotations

import argparse
import json
import os
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from typing import Any


def env_bool(name: str, default: bool = True) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() not in {"0", "false", "no", "off"}


@dataclass
class CheckResult:
    id: str
    description: str
    points: int
    ok: bool
    detail: str = ""


@dataclass
class TeamScore:
    team: str
    checks: list[CheckResult] = field(default_factory=list)

    @property
    def earned(self) -> int:
        return sum(c.points for c in self.checks if c.ok)

    @property
    def max_points(self) -> int:
        return sum(c.points for c in self.checks)


class ControllerClient:
    def __init__(self, host: str, token: str | None, user: str | None, password: str | None, verify_ssl: bool):
        self.base = host.rstrip("/")
        self.token = token
        self.user = user
        self.password = password
        self.ctx = None if verify_ssl else ssl._create_unverified_context()

    def _headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        qs = f"?{urllib.parse.urlencode(params)}" if params else ""
        url = f"{self.base}{path}{qs}"
        req = urllib.request.Request(url, headers=self._headers(), method="GET")
        if not self.token and self.user and self.password:
            import base64

            basic = base64.b64encode(f"{self.user}:{self.password}".encode()).decode()
            req.add_header("Authorization", f"Basic {basic}")
        try:
            with urllib.request.urlopen(req, context=self.ctx, timeout=60) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            body = e.read().decode(errors="replace")
            raise RuntimeError(f"HTTP {e.code} {path}: {body[:300]}") from e

    def get_all(self, path: str, params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        params = dict(params or {})
        params.setdefault("page_size", 200)
        results: list[dict[str, Any]] = []
        data = self.get(path, params)
        results.extend(data.get("results", []))
        while data.get("next"):
            next_url = data["next"]
            if next_url.startswith("http"):
                parsed = urllib.parse.urlparse(next_url)
                path_only = parsed.path
                q = dict(urllib.parse.parse_qsl(parsed.query))
                data = self.get(path_only, q)
            else:
                data = self.get(next_url)
            results.extend(data.get("results", []))
        return results


def score_team(client: ControllerClient, team: str) -> TeamScore:
    ts = TeamScore(team=team)
    prefix = f"t{team}-"
    host_linux = f"{prefix}linux"
    host_windows = f"{prefix}windows"

    # --- Lab 2: credentials + project (participants create these) ---
    creds = client.get_all("/api/v2/credentials/", {"search": prefix})
    cred_names = {c["name"] for c in creds}

    expected_creds = [
        (f"{prefix}scm-gitea", "cred_scm", 3, "Credencial Source Control tN-scm-gitea"),
        (f"{prefix}machine-linux", "cred_linux", 3, "Credencial Machine tN-machine-linux"),
        (f"{prefix}machine-windows", "cred_windows", 3, "Credencial Machine tN-machine-windows"),
        (f"{prefix}aws", "cred_aws", 3, "Credencial AWS tN-aws"),
    ]
    for exact, cid, pts, desc in expected_creds:
        ok = exact in cred_names
        ts.checks.append(
            CheckResult(cid, desc.replace("tN", f"t{team}"), pts, ok, exact if ok else f"missing {exact}")
        )

    projects = client.get_all("/api/v2/projects/", {"name": f"{prefix}starter"})
    project_ok = False
    detail = "project not found"
    if projects:
        p = projects[0]
        status = (p.get("status") or "").lower()
        project_ok = status == "successful"
        detail = f"status={p.get('status')}"
    ts.checks.append(
        CheckResult("project_sync", f"Project {prefix}starter sync successful", 3, project_ok, detail)
    )

    # --- Lab 3: dynamic inventory Name + keyed groups ---
    inventories = client.get_all("/api/v2/inventories/", {"name": f"{prefix}aws"})
    inv_ok = bool(inventories)
    ts.checks.append(
        CheckResult(
            "inventory_exists",
            f"Inventory {prefix}aws existe",
            2,
            inv_ok,
            inventories[0]["name"] if inv_ok else "missing",
        )
    )

    host_names: set[str] = set()
    group_names: set[str] = set()
    host_groups: dict[str, set[str]] = {}
    if inv_ok:
        inv_id = inventories[0]["id"]
        hosts = client.get_all(f"/api/v2/inventories/{inv_id}/hosts/")
        host_names = {h["name"] for h in hosts}
        groups = client.get_all(f"/api/v2/inventories/{inv_id}/groups/")
        group_names = {g["name"] for g in groups}
        group_by_name = {g["name"]: g for g in groups}
        for gname in ("linux", "windows", "web", "db"):
            g = group_by_name.get(gname)
            if not g:
                continue
            g_hosts = client.get_all(f"/api/v2/groups/{g['id']}/hosts/")
            for h in g_hosts:
                host_groups.setdefault(h["name"], set()).add(gname)

    expected_hosts = [host_linux, host_windows]
    host_ok = all(h in host_names for h in expected_hosts)
    if not host_ok and host_names:
        host_ok = all(
            any(exp == h or h.endswith(exp) or exp in h for h in host_names) for exp in expected_hosts
        )
    ts.checks.append(
        CheckResult(
            "hostnames_name",
            "Hosts nombrados como tag Name (linux + windows)",
            4,
            host_ok,
            f"found={sorted(host_names) or '[]'}",
        )
    )

    for gname, cid, pts in [
        ("linux", "group_linux", 1),
        ("windows", "group_windows", 1),
        ("web", "group_web", 1),
        ("db", "group_db", 1),
    ]:
        ok = gname in group_names
        ts.checks.append(
            CheckResult(
                cid,
                f"Grupo dinámico {gname}",
                pts,
                ok,
                "present" if ok else f"missing; have={sorted(group_names)}",
            )
        )

    def membership_ok(hostname: str, required: set[str]) -> tuple[bool, str]:
        # Resolve exact or fuzzy hostname match from inventory
        match = hostname if hostname in host_groups else next(
            (h for h in host_groups if h == hostname or h.endswith(hostname) or hostname in h),
            None,
        )
        if match is None:
            # host may exist but without group membership fetched
            if hostname in host_names or any(hostname in h or h.endswith(hostname) for h in host_names):
                return False, f"host present but not in {sorted(required)}"
            return False, f"host missing; groups_map={ {k: sorted(v) for k, v in host_groups.items()} }"
        have = host_groups.get(match, set())
        ok = required.issubset(have)
        return ok, f"{match} groups={sorted(have)}"

    web_ok, web_detail = membership_ok(host_linux, {"linux", "web"})
    ts.checks.append(
        CheckResult(
            "membership_web_linux",
            f"{host_linux} ∈ linux y web",
            2,
            web_ok,
            web_detail,
        )
    )

    db_ok, db_detail = membership_ok(host_windows, {"windows", "db"})
    ts.checks.append(
        CheckResult(
            "membership_db_windows",
            f"{host_windows} ∈ windows y db",
            3,
            db_ok,
            db_detail,
        )
    )

    return ts


def print_table(scores: list[TeamScore]) -> None:
    print("")
    print(f"{'Team':<8}{'Earned':>8}{'Max':>8}  Detail")
    print("-" * 72)
    for s in scores:
        print(f"t{s.team:<7}{s.earned:>8}{s.max_points:>8}")
        for c in s.checks:
            mark = "OK" if c.ok else "FAIL"
            print(f"  [{mark:<4}] +{c.points:<2} {c.description} ({c.detail})")
    print("-" * 72)
    total_e = sum(s.earned for s in scores)
    total_m = sum(s.max_points for s in scores)
    print(f"{'TOTAL':<8}{total_e:>8}{total_m:>8}")
    print("")


def main() -> int:
    parser = argparse.ArgumentParser(description="Score workathon labs 2–3 on AAP Controller")
    parser.add_argument("--json", action="store_true", help="Emit JSON scoreboard")
    parser.add_argument("--teams", default=os.environ.get("TEAMS", "1,2,3"))
    args = parser.parse_args()

    host = os.environ.get("CONTROLLER_HOST") or os.environ.get("TOWER_HOST")
    token = os.environ.get("CONTROLLER_TOKEN") or os.environ.get("TOWER_OAUTH_TOKEN")
    user = os.environ.get("CONTROLLER_USERNAME") or os.environ.get("TOWER_USERNAME")
    password = os.environ.get("CONTROLLER_PASSWORD") or os.environ.get("TOWER_PASSWORD")
    verify = env_bool("VERIFY_SSL", True)

    if not host:
        print("CONTROLLER_HOST is required", file=sys.stderr)
        return 2
    if not token and not (user and password):
        print("CONTROLLER_TOKEN or CONTROLLER_USERNAME/PASSWORD required", file=sys.stderr)
        return 2

    client = ControllerClient(host, token, user, password, verify)
    teams = [t.strip() for t in args.teams.split(",") if t.strip()]
    scores = [score_team(client, t) for t in teams]

    if args.json:
        payload = {
            "teams": [
                {
                    "team": s.team,
                    "earned": s.earned,
                    "max_points": s.max_points,
                    "checks": [c.__dict__ for c in s.checks],
                }
                for s in scores
            ]
        }
        print(json.dumps(payload, indent=2))
    else:
        print_table(scores)
    return 0


if __name__ == "__main__":
    sys.exit(main())
