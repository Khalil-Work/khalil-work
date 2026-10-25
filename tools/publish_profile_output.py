"""Publish generated assets to output, preserving history and unrelated files."""
import base64
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import urllib.error
import urllib.request


def main():
    token = os.environ["GH_TOKEN"]
    repo = os.environ["GITHUB_REPOSITORY"]
    if repo.lower() != "khalil-work/khalil-work":
        raise ValueError("Unexpected repository")

    def api(path, data=None, method=None):
        request = urllib.request.Request("https://api.github.com/repos/" + repo + path,
            data=None if data is None else json.dumps(data).encode(), method=method,
            headers={"Authorization": "Bearer " + token, "Accept": "application/vnd.github+json",
                     "Content-Type": "application/json", "User-Agent": "Khalil-Work-profile-assets"})
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.load(response)

    head = api("/git/ref/heads/output")["object"]["sha"]
    base = api("/git/commits/" + head)
    entries = []
    existing = {item["path"]: item["sha"] for item in api("/git/trees/" + base["tree"]["sha"] + "?recursive=1")["tree"]}
    for file in sorted(Path("dist").rglob("*")):
        if not file.is_file():
            continue
        path = file.relative_to("dist").as_posix()
        blob = api("/git/blobs", {"encoding": "base64", "content": base64.b64encode(file.read_bytes()).decode()})
        if existing.get(path) != blob["sha"]:
            entries.append({"path": path, "sha": blob["sha"], "type": "blob", "mode": "100644"})
    if not entries:
        print("Generated assets are unchanged")
        return
    tree = api("/git/trees", {"base_tree": base["tree"]["sha"], "tree": entries})
    stamp = datetime.now(timezone.utc).date().isoformat()
    commit = api("/git/commits", {"tree": tree["sha"], "parents": [head], "message": "Refresh daily profile assets · " + stamp,
        "author": {"name": "github-actions[bot]", "email": "41898282+github-actions[bot]@users.noreply.github.com"}})
    api("/git/refs/heads/output", {"sha": commit["sha"], "force": False}, "PATCH")
    print(f"Published {len(entries)} generated assets to output: {commit['sha']}")


if __name__ == "__main__":
    main()
