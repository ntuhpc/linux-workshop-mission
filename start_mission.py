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
import secrets
import shutil
import socket
import sys
import urllib.error
import urllib.request
from pathlib import Path

# >>> Instructor: point this at the machine running server.py (from the linux-workshop-mission-admin repo) <<<
SERVER_URL = os.environ.get("MISSION_SERVER", "").strip() or "http://127.0.0.1:8000"

MISSION = Path.home() / "linux_mission"
TOKEN_FILE = Path.home() / ".linux_mission_token"  # proves to the server that you are you


def load_token():
    """Read the saved token, or make and save a new one BEFORE contacting the server, so a lost
    reply on the first run doesn't leave the server knowing a token that we don't."""
    if TOKEN_FILE.exists():
        return TOKEN_FILE.read_text().strip()
    token = secrets.token_hex(16)
    save_token(token)
    return token


def save_token(token):
    old_umask = os.umask(0o077)
    TOKEN_FILE.write_text(token + "\n")  # readable only by you
    os.umask(old_umask)


def shell_is_inside(folder):
    """True if the terminal that ran us is inside `folder` (or in a folder that was deleted)."""
    try:
        cwd = Path(os.getcwd()).resolve()
    except FileNotFoundError:  # e.g. still sitting in a mission folder deleted by a previous rebuild
        return True
    return cwd == folder or folder in cwd.parents


def looks_like_a_mission(folder):
    """Any trace of a mission counts (people who broke theirs may have deleted parts), as does empty."""
    markers = ("submit.py", "README.txt", ".bunker", "archives", "vault", "workshop")
    return not any(folder.iterdir()) or any((folder / m).exists() for m in markers)


def register(user, token):
    payload = json.dumps({"username": user, "hostname": socket.gethostname(), "token": token}).encode()
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))  # ignore http_proxy - the server is local
    try:
        try:
            req = urllib.request.Request(SERVER_URL + "/api/start", data=payload,  # ValueError on a malformed URL
                                         headers={"Content-Type": "application/json"})
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
    if MISSION.is_symlink():
        sys.exit(f"{MISSION} is a link to another folder. Remove the link with:  rm {MISSION}  and run this again.")
    # A rebuild deletes the folder, so never delete something that isn't a mission (e.g. a git
    # clone that ended up there). Checked before registering, so the timer doesn't start yet.
    if MISSION.exists() and not looks_like_a_mission(MISSION):
        sys.exit(f"{MISSION} already exists but isn't a mission folder, so it wasn't touched.\n"
                 f"Move it out of the way with:  mv {MISSION} {MISSION}.old   and run this again.")
    res = register(user, load_token())
    if res["token"] != TOKEN_FILE.read_text().strip():
        save_token(res["token"])

    rebuilt = MISSION.exists()
    vault_was_open = (MISSION / "vault").exists()
    stranded = rebuilt and shell_is_inside(MISSION.resolve())
    if rebuilt:
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
    if vault_was_open:
        print("Everything was rebuilt from the start, so you'll need to unlock the vault again")
        print("(the log is new, so count the ERROR lines again). Fragments you already found stay the same.")
    if stranded:
        print()
        print("!! Your terminal is still inside the OLD folder, which no longer exists.")
        print("!! Run this before anything else:   cd ~/linux_mission")
    else:
        print("Begin with:   cd ~/linux_mission   and then read README.txt")


if __name__ == "__main__":
    main()
