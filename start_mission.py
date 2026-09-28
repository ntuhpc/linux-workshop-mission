#!/usr/bin/env python3
"""
Linux Workshop - recap mission.

Participants run:   python3 start_mission.py
It registers you with the mission server (this starts your timer!) and builds ~/linux_mission.
Running it again rebuilds the folder but does NOT reset your timer.
"""

import json
import os
import pwd
import shutil
import socket
import sys
import urllib.error
import urllib.request
from pathlib import Path

# >>> Instructor: point this at the machine running server.py (from the linux-workshop-mission-admin repo) <<<
SERVER_URL = os.environ.get("MISSION_SERVER", "http://127.0.0.1:8000")

MISSION = Path.home() / "linux_mission"
TOKEN_FILE = Path.home() / ".linux_mission_token"  # proves to the server that you are you


def register(user):
    token = TOKEN_FILE.read_text().strip() if TOKEN_FILE.exists() else ""
    payload = json.dumps({"username": user, "hostname": socket.gethostname(), "token": token}).encode()
    req = urllib.request.Request(SERVER_URL + "/api/start", data=payload,
                                 headers={"Content-Type": "application/json"})
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))  # ignore http_proxy - the server is local
    try:
        try:
            with opener.open(req, timeout=30) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            res = json.load(e)
            print(res.get("message", f"The server refused the request (HTTP {e.code})."))
            sys.exit(1)
    except (urllib.error.URLError, OSError, ValueError) as e:
        print(f"Could not talk to the mission server at {SERVER_URL} ({getattr(e, 'reason', e)}).")
        print("Ask your instructor - the mission can't start without it.")
        sys.exit(2)


def main():
    user = pwd.getpwuid(os.getuid()).pw_name  # same as `whoami`
    res = register(user)

    old_umask = os.umask(0o077)
    TOKEN_FILE.write_text(res["token"] + "\n")  # readable only by you
    os.umask(old_umask)

    if MISSION.exists():
        shutil.rmtree(MISSION)
    for rel, (content, mode) in res["files"].items():
        p = (MISSION / rel).resolve()
        if MISSION.resolve() not in p.parents:
            sys.exit(f"Refusing to write outside {MISSION}: {rel}")
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content.replace("__SERVER_URL__", SERVER_URL) if rel == "submit.py" else content)
        os.chmod(p, mode)

    print(f"Mission {'rebuilt (your timer was NOT reset)' if res['resumed'] else 'started'}, agent {user}!")
    print(f"Your mission folder is: {MISSION}")
    print("Begin with:   cd ~/linux_mission   and then read README.txt")


if __name__ == "__main__":
    main()
