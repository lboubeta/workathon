#!/usr/bin/env python3
"""Validate facilitator inventory design (Name hostnames + OS/Role groups)."""

from __future__ import annotations

import os
import sys

# Reuse API client from apply script
sys.path.insert(0, str(__file__.rsplit("/", 1)[0]))
from apply_facilitator import Api, env_bool  # noqa: E402


def main() -> int:
    host = os.environ.get("CONTROLLER_HOST")
    token = os.environ.get("CONTROLLER_TOKEN")
    if not host or not token:
        print("CONTROLLER_HOST and CONTROLLER_TOKEN required", file=sys.stderr)
        return 2

    org = os.environ.get("ORG_NAME", "facilitator")
    inv_name = os.environ.get("INVENTORY_NAME", "facilitator-aws")
    api = Api(host, token, verify=env_bool("VERIFY_SSL", False))

    inv = api.find_one("/api/controller/v2/inventories/", inv_name)
    if not inv:
        print(f"FAIL inventory {inv_name} missing", file=sys.stderr)
        return 1

    hosts = {h["name"] for h in api.get_all(f"/api/controller/v2/inventories/{inv['id']}/hosts/")}
    groups = {g["name"]: g for g in api.get_all(f"/api/controller/v2/inventories/{inv['id']}/groups/")}

    expected_hosts = [f"t{n}-linux" for n in (1, 2, 3)] + [f"t{n}-windows" for n in (1, 2, 3)]
    expected_groups = ["linux", "windows", "web", "db"]

    ok = True
    for h in expected_hosts:
        if h in hosts:
            print(f"  [OK] host {h}")
        else:
            print(f"  [FAIL] host {h} missing; have={sorted(hosts)}")
            ok = False

    for g in expected_groups:
        if g in groups:
            print(f"  [OK] group {g}")
        else:
            print(f"  [FAIL] group {g} missing; have={sorted(groups)}")
            ok = False

    host_groups: dict[str, set[str]] = {}
    for gname in expected_groups:
        g = groups.get(gname)
        if not g:
            continue
        for h in api.get_all(f"/api/controller/v2/groups/{g['id']}/hosts/"):
            host_groups.setdefault(h["name"], set()).add(gname)

    checks = [
        ("t1-linux", {"linux", "web"}),
        ("t1-windows", {"windows", "db"}),
    ]
    for hostname, need in checks:
        have = host_groups.get(hostname, set())
        if need.issubset(have):
            print(f"  [OK] {hostname} ∈ {sorted(need)} (have={sorted(have)})")
        else:
            print(f"  [FAIL] {hostname} need={sorted(need)} have={sorted(have)}")
            ok = False

    print("")
    print(f"RESULT: {'PASS — design viable in org ' + org if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
