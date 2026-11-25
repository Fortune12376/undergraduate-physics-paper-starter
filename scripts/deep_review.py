"""Run or resume one free Google Deep Review during checkpoint 3."""

import argparse
from datetime import date
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sqlite3
import subprocess
import time
from urllib.error import HTTPError
from urllib.request import HTTPRedirectHandler, Request, build_opener


BASE = "https://deepreview.googleapis.com"
LOCAL = Path("paper/.local")
PDF = Path("paper/paper.pdf")
LOG = Path("paper/review.md")


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def google_request():
    if "GOOGLE_APPLICATION_CREDENTIALS" in os.environ:
        raise RuntimeError("Unset GOOGLE_APPLICATION_CREDENTIALS to use local user ADC.")

    def gcloud(*args):
        executable = shutil.which("gcloud")
        if not executable:
            raise RuntimeError("Install the Google Cloud CLI and add it to PATH.")
        return subprocess.check_output([executable, *args], text=True, timeout=60).strip()

    project = gcloud("config", "get-value", "project")
    if not project or project == "(unset)":
        raise RuntimeError("Set the active Google Cloud project first.")
    token = gcloud("auth", "application-default", "print-access-token")
    opener = build_opener(NoRedirect())

    def request(method, path, data=None, content_type=None):
        headers = {"Authorization": f"Bearer {token}", "x-goog-user-project": project}
        if content_type:
            headers["Content-Type"] = content_type
        try:
            with opener.open(Request(BASE + path, data, headers, method=method), timeout=45) as response:
                return json.load(response)
        except HTTPError as exc:
            if exc.code == 429:
                raise
            raise RuntimeError(f"Deep Review returned HTTP {exc.code} for {method} {path}.") from None

    return request


def write_json(path, data):
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    temporary.replace(path)


def log(message):
    entry = f"- {date.today().isoformat()} · Checkpoint 3 · Google Deep Review · {message}"
    exists = LOG.exists()
    previous = LOG.read_text(encoding="utf-8") if exists else ""
    if entry not in previous.splitlines():
        with LOG.open("a", encoding="utf-8") as stream:
            if not exists:
                stream.write("# Paper review\n\n")
            elif previous and not previous.endswith("\n"):
                stream.write("\n")
            stream.write(entry + "\n")
    print(message)


def name_of(resource, pattern):
    name = resource.get("name", "")
    if not re.fullmatch(pattern, name):
        raise RuntimeError("Google returned an unexpected resource name.")
    return name


def has_quota(request):
    quota = request("GET", "/v1/userQuota")
    remaining = quota.get("remainingReviewCount", 0)
    if type(remaining) is int and remaining > 0:
        return True
    next_time = quota.get("nextAvailableTime")
    availability = f" Next available at {next_time}." if next_time else ""
    log(f"No free review slot confirmed.{availability} Pending author decision to wait or finish.")
    return False


def run(request_factory=google_request, *, polls=30, pause=time.sleep):
    LOCAL.mkdir(parents=True, exist_ok=True)
    # Keep a process lock across API calls. SQLite releases it if the process exits.
    lock = sqlite3.connect(LOCAL / "deep-review.lock", timeout=1)
    try:
        lock.execute("BEGIN EXCLUSIVE")
        return run_locked(request_factory, polls, pause)
    finally:
        lock.close()


def run_locked(request_factory, polls, pause):
    state_path = LOCAL / "deep-review-state.json"
    result_path = LOCAL / "deep-review.json"
    state = json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else {}
    if result_path.exists():
        record_result(state, result_path)
        return
    request = request_factory()

    if not state:
        if not has_quota(request):
            return
        pdf = PDF.read_bytes()
        if not pdf.startswith(b"%PDF-") or len(pdf) > 20_000_000:
            raise RuntimeError("Expected a complete PDF within Google's 20 MB limit.")
        digest = hashlib.sha256(pdf).hexdigest()
        snapshot = LOCAL / f"reviewed-{digest}.pdf"
        snapshot.write_bytes(pdf)
        state = {"sha256": digest, "pdf": snapshot.as_posix(), "stage": "uploading"}
        write_json(state_path, state)
        upload = request("POST", "/upload/v1/documents?uploadType=media", pdf, "application/pdf")
        state.update(document=name_of(upload, r"documents/[\w-]+"), stage="uploaded")
        write_json(state_path, state)
    elif state["stage"] == "uploading":
        raise RuntimeError("Upload outcome unknown. Reconcile the document in Google before continuing.")

    document = state["document"]
    reviews_url = f"/v1/{document}/reviews"
    review_pattern = re.escape(document) + r"/reviews/[\w-]+"
    operation_pattern = r"operations/" + review_pattern
    if state["stage"] == "uploaded":
        if not has_quota(request):
            return
        state["stage"] = "submitting"
        write_json(state_path, state)
        try:
            operation = request("POST", reviews_url, b'{"runConfig":{"topology":"MID"}}', "application/json")
        except HTTPError as exc:
            if exc.code != 429:
                raise
            state["stage"] = "uploaded"
            write_json(state_path, state)
            has_quota(request)
            log("Google rate-limited review creation. Resume the existing document later.")
            return
        state.update(operation=name_of(operation, operation_pattern), stage="polling")
        write_json(state_path, state)
    elif state["stage"] == "submitting":
        # This document was created for this run. Seek its review before any retry.
        # An empty list may reflect propagation delay, so leave the outcome pending.
        listing = request("GET", reviews_url)
        reviews = listing.get("reviews", [])
        if len(reviews) != 1 or listing.get("nextPageToken"):
            log("Submission outcome unresolved after listing document reviews. Resume later.")
            return
        review = name_of(reviews[0], review_pattern)
        state.update(operation=f"operations/{review}", stage="polling")
        write_json(state_path, state)

    for attempt in range(polls):
        operation = request("GET", f"/v1/{state['operation']}")
        if operation.get("error"):
            raise RuntimeError(f"Google review operation failed ({state['operation']}).")
        if operation.get("done"):
            review = name_of(operation["response"], review_pattern)
            result = request("GET", f"/v1/{review}")
            if name_of(result, review_pattern) != review or result.get("result", {}).get("error"):
                raise RuntimeError("Google returned an unexpected or failed review.")
            write_json(result_path, result)
            record_result(state, result_path)
            return
        if attempt + 1 < polls:
            pause(10)
    log(f"Review pending. Resume operation `{state['operation']}` with the same command.")


def record_result(state, path):
    log(
        f"Full review `{path.as_posix()}` for `{state['pdf']}` "
        f"(SHA-256 `{state['sha256']}`). Document `{state['document']}`, "
        f"operation `{state['operation']}`."
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint-3", action="store_true", required=True,
                        help="Confirm author opt-in and completion of the near-final internal audit.")
    parser.parse_args()
    try:
        run()
    except (OSError, RuntimeError, ValueError, KeyError, sqlite3.Error, subprocess.SubprocessError) as exc:
        parser.exit(1, f"Deep Review paused. {exc}\n")
