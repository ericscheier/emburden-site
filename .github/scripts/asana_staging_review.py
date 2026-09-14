#!/usr/bin/env python3
"""Staging-review loop for emburden-site.

Runs from `.github/workflows/notify-staging-review.yml` after
`deploy-staging.yml` publishes to `staging.emburden.org`. Ensures the
user's todojor Asana project holds at most one open review task per
site, that trivial deploys don't wake the user, and that new material
changes append comments instead of piling up duplicates.

Dedupe pattern is the in-house `Genesis:` marker convention from
`workbench/claude-orchestration-system/adapters/asana/adapter.py` —
first line of a task's notes carries
`Genesis: <site_key> · source:gh-actions · by:staging-review-loop`.
We paginate the project's task list (never rely on the first page
alone — the 250k-dupe incident cited in that repo is the reason).

Environment (all set by the workflow):
  ASANA_TOKEN           PAT with write access to the todojor project
  ASANA_WORKSPACE_GID   K&E workspace GID
  ASANA_PROJECT_GID     todojor project GID
  ASANA_ASSIGNEE_GID    user's Asana GID (assignee for new tasks)
  STAGING_URL           the URL to review
  SITE_KEY              site-scoped id embedded in Genesis marker
  REPO_SLUG             owner/repo of the source (for compare URLs)
  REVIEW_SHA            SHA that was just deployed to staging
  GITHUB_STEP_SUMMARY   (optional) path to append job summary
"""
from __future__ import annotations

import datetime as dt
import os
import subprocess
import sys
import textwrap
from typing import Any, Dict, List, Optional

import requests

BASE = "https://app.asana.com/api/v1"
NOTES_MARKER = "Genesis:"
LAST_REVIEWED_KEY = "last-reviewed-sha:"
LAST_NOTIFIED_KEY = "last-notified-sha:"


# --------------------------------------------------------------------- utils
def env(key: str, default: Optional[str] = None) -> str:
    v = os.environ.get(key, default)
    if v is None or v == "":
        raise SystemExit(f"missing required env var: {key}")
    return v


def api(method: str, path: str, **kw: Any) -> Dict[str, Any]:
    kw.setdefault("headers", {})["Authorization"] = f"Bearer {env('ASANA_TOKEN')}"
    kw["headers"]["Accept"] = "application/json"
    r = requests.request(method, f"{BASE}{path}", timeout=30, **kw)
    if not r.ok:
        raise SystemExit(f"asana {method} {path}: {r.status_code} {r.text[:400]}")
    return r.json()


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], capture_output=True, text=True, check=True
    ).stdout.strip()


def emit_summary(**fields: Any) -> None:
    """Write a GH Actions step summary if $GITHUB_STEP_SUMMARY is set."""
    dest = os.environ.get("GITHUB_STEP_SUMMARY")
    if not dest:
        return
    lines = ["## staging-review loop", ""]
    for k, v in fields.items():
        lines.append(f"- **{k}**: {v}")
    with open(dest, "a", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


# ------------------------------------------------- (1) find the review task
def find_task(project_gid: str, site_key: str) -> Optional[Dict[str, Any]]:
    """Paginated scan of a project's tasks for the Genesis marker."""
    marker_prefix = f"{NOTES_MARKER} {site_key} "
    offset: Optional[str] = None
    while True:
        params = {"limit": 100, "opt_fields": "name,notes,completed,resource_type"}
        if offset:
            params["offset"] = offset
        page = api("GET", f"/projects/{project_gid}/tasks", params=params)
        for stub in page.get("data", []):
            # stub already has notes since opt_fields includes it
            notes = stub.get("notes") or ""
            first_line = notes.split("\n", 1)[0].strip()
            if first_line.startswith(marker_prefix):
                return stub
        offset = page.get("next_page", {}).get("offset") if page.get("next_page") else None
        if not offset:
            return None


# ---------------------------------------------- (2) classify the current diff
def classify_diff(last_sha: Optional[str], current_sha: str) -> Dict[str, Any]:
    """Return {material: bool, reason: str, changed_files: [str], commit_titles: [str]}."""
    if not last_sha:
        return {
            "material": True,
            "reason": "first deploy for this site",
            "changed_files": [],
            "commit_titles": _commit_titles(f"{current_sha}~5..{current_sha}"),
        }
    try:
        raw = git("diff", "--name-only", f"{last_sha}..{current_sha}")
    except subprocess.CalledProcessError:
        # last_sha not in current history (force-push, rebase). Treat as material.
        return {
            "material": True,
            "reason": f"prior sha {last_sha[:8]} not reachable — force-push/rebase",
            "changed_files": [],
            "commit_titles": [],
        }
    files = [ln for ln in raw.split("\n") if ln.strip()]
    titles = _commit_titles(f"{last_sha}..{current_sha}")
    if not files:
        return {
            "material": False,
            "reason": "no file diff (re-deploy of same tree)",
            "changed_files": files,
            "commit_titles": titles,
        }
    # Non-material: build-output only, autosave-only.
    material_files = [
        f for f in files
        if not f.startswith("_build/") and not f.startswith("docs/")
    ]
    autosave_only = all(t.startswith("auto-save:") for t in titles) if titles else False
    if not material_files and not autosave_only:
        return {
            "material": False,
            "reason": f"only build-output changed ({len(files)} files under _build/ or docs/)",
            "changed_files": files,
            "commit_titles": titles,
        }
    if autosave_only:
        return {
            "material": False,
            "reason": f"only auto-save commits ({len(titles)})",
            "changed_files": files,
            "commit_titles": titles,
        }
    return {
        "material": True,
        "reason": f"{len(material_files)} source files changed",
        "changed_files": files,
        "commit_titles": titles,
    }


def _commit_titles(range_: str) -> List[str]:
    try:
        raw = git("log", "--oneline", "--no-decorate", range_)
    except subprocess.CalledProcessError:
        return []
    out = []
    for ln in raw.split("\n"):
        ln = ln.strip()
        if not ln:
            continue
        # drop the sha
        parts = ln.split(None, 1)
        out.append(parts[1] if len(parts) > 1 else parts[0])
    return out


# ----------------------------------------------------------- (3) act on task
def build_notes(
    site_key: str,
    staging_url: str,
    review_sha: str,
    last_reviewed: str,
    change_summary: str,
) -> str:
    return textwrap.dedent(f"""\
        {NOTES_MARKER} {site_key} · source:gh-actions · by:staging-review-loop
        {staging_url}

        {LAST_REVIEWED_KEY} {last_reviewed}
        {LAST_NOTIFIED_KEY} {review_sha}

        {change_summary}
        """)


def parse_last_reviewed(notes: str) -> Optional[str]:
    for ln in (notes or "").splitlines():
        ln = ln.strip()
        if ln.startswith(LAST_REVIEWED_KEY):
            v = ln[len(LAST_REVIEWED_KEY):].strip()
            return v or None
    return None


def format_summary(diff: Dict[str, Any], repo: str, last: Optional[str], cur: str) -> str:
    parts: List[str] = []
    if last:
        parts.append(f"Compare: https://github.com/{repo}/compare/{last[:12]}...{cur[:12]}")
    if diff["commit_titles"]:
        parts.append("Commits since last review:")
        for t in diff["commit_titles"][:12]:
            parts.append(f"  - {t}")
        if len(diff["commit_titles"]) > 12:
            parts.append(f"  … and {len(diff['commit_titles']) - 12} more")
    if diff["changed_files"]:
        parts.append(f"Files changed: {len(diff['changed_files'])}")
    return "\n".join(parts) if parts else "(no summary available)"


def act(
    task: Optional[Dict[str, Any]],
    diff: Dict[str, Any],
    site_key: str,
    staging_url: str,
    review_sha: str,
    project_gid: str,
    workspace_gid: str,
    assignee_gid: str,
    repo: str,
) -> Dict[str, Any]:
    last_reviewed = (
        parse_last_reviewed(task.get("notes", "") if task else "") or ""
    )
    change_summary = format_summary(diff, repo, last_reviewed or None, review_sha)

    # Non-material and no open task → do nothing.
    if not diff["material"] and (task is None or task.get("completed")):
        return {"action": "no-op", "detail": diff["reason"]}

    # Task open (whether material or not): comment on it, keep last_reviewed.
    if task and not task.get("completed"):
        comment_body = (
            f"New staging deploy at {review_sha[:12]}. {diff['reason']}.\n\n"
            + change_summary
        )
        api(
            "POST",
            f"/tasks/{task['gid']}/stories",
            json={"data": {"text": comment_body}},
        )
        # Update last-notified in notes but keep last-reviewed.
        new_notes = build_notes(
            site_key=site_key,
            staging_url=staging_url,
            review_sha=review_sha,
            last_reviewed=last_reviewed or review_sha,
            change_summary=change_summary,
        )
        api("PUT", f"/tasks/{task['gid']}", json={"data": {"notes": new_notes}})
        return {"action": "commented", "task_gid": task["gid"]}

    # Task completed AND material: reopen.
    if task and task.get("completed") and diff["material"]:
        new_notes = build_notes(
            site_key=site_key,
            staging_url=staging_url,
            review_sha=review_sha,
            last_reviewed=review_sha,   # user just reviewed; now we push forward
            change_summary=change_summary,
        )
        api(
            "PUT",
            f"/tasks/{task['gid']}",
            json={"data": {"completed": False, "notes": new_notes}},
        )
        api(
            "POST",
            f"/tasks/{task['gid']}/stories",
            json={"data": {"text": (
                f"Reopened for staging deploy {review_sha[:12]}.\n\n"
                + change_summary
            )}},
        )
        return {"action": "reopened", "task_gid": task["gid"]}

    # Fresh material deploy, no prior task: create.
    if task is None and diff["material"]:
        due = (dt.date.today() + dt.timedelta(days=1)).isoformat()
        new_notes = build_notes(
            site_key=site_key,
            staging_url=staging_url,
            review_sha=review_sha,
            last_reviewed=review_sha,
            change_summary=change_summary,
        )
        payload = {
            "data": {
                "name": f"Review {staging_url.replace('https://', '')}",
                "notes": new_notes,
                "projects": [project_gid],
                "workspace": workspace_gid,
                "assignee": assignee_gid,
                "due_on": due,
            }
        }
        created = api("POST", "/tasks", json=payload)
        return {"action": "created", "task_gid": created["data"]["gid"]}

    # Fallback shouldn't happen but be explicit.
    return {"action": "no-op", "detail": "no matching branch"}


# ------------------------------------------------------------------- driver
def main() -> int:
    project_gid   = env("ASANA_PROJECT_GID")
    workspace_gid = env("ASANA_WORKSPACE_GID")
    assignee_gid  = env("ASANA_ASSIGNEE_GID")
    site_key      = env("SITE_KEY")
    staging_url   = env("STAGING_URL")
    review_sha    = env("REVIEW_SHA", git("rev-parse", "HEAD"))
    repo          = env("REPO_SLUG", "ericscheier/emburden-site")

    task = find_task(project_gid, site_key)
    last_reviewed = parse_last_reviewed(task.get("notes", "")) if task else None
    diff = classify_diff(last_reviewed, review_sha)
    result = act(
        task=task,
        diff=diff,
        site_key=site_key,
        staging_url=staging_url,
        review_sha=review_sha,
        project_gid=project_gid,
        workspace_gid=workspace_gid,
        assignee_gid=assignee_gid,
        repo=repo,
    )

    print(f"result: {result}")
    emit_summary(
        action=result.get("action", "?"),
        detail=result.get("detail", "-"),
        task_gid=result.get("task_gid", "-"),
        review_sha=review_sha[:12],
        last_reviewed=(last_reviewed or "(none)")[:12] if last_reviewed else "(none)",
        material=diff["material"],
        material_reason=diff["reason"],
        changed_files=len(diff["changed_files"]),
        staging_url=staging_url,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
