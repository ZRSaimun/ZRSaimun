"""Shared GitHub readers for public profile panels."""
import json
import os
import urllib.request

USER = os.getenv("PROFILE_USER", "ZRSaimun")
HEADERS = {"Accept": "application/vnd.github+json", "User-Agent": "ZR-Live-Profile"}
token = os.getenv("GITHUB_TOKEN")
if token:
    HEADERS["Authorization"] = f"Bearer {token}"


def get(url):
    request = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.load(response)


def public_repositories():
    repos = []
    page = 1
    while True:
        batch = get(
            f"https://api.github.com/users/{USER}/repos"
            f"?type=owner&per_page=100&sort=updated&page={page}"
        )
        repos.extend(repo for repo in batch if not repo.get("fork") and not repo.get("private"))
        if len(batch) < 100:
            break
        page += 1
    return sorted(repos, key=lambda repo: repo.get("pushed_at") or "", reverse=True)
