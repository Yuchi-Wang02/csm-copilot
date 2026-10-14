"""Build a reproducible static interview bundle from a committed Git tree."""

import argparse
import hashlib
import io
import json
import posixpath
import subprocess
import tomllib
import zipfile
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PREFIX = "csm-copilot-demo/"
FORMAT = "csm-interview-bundle-v1"


def git(root, *args):
    return subprocess.check_output(["git", *args], cwd=root, stderr=subprocess.PIPE)


class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.paths = []

    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if value and ((tag == "script" and key == "src") or key == "href"):
                self.paths.append(value)


def validate_references(files):
    for name, content in files.items():
        if not name.endswith(".html"):
            continue
        parser = References()
        parser.feed(content.decode("utf-8"))
        for reference in parser.paths:
            url = urlsplit(reference)
            if url.scheme or url.netloc or not url.path:
                continue
            path = unquote(url.path)
            if path.startswith("/"):
                raise ValueError(f"Root-relative link is not portable: {name}: {reference}")
            target = posixpath.normpath(posixpath.join(posixpath.dirname(name), path))
            if target not in files:
                raise ValueError(f"Missing packaged link: {name}: {reference}")


def start_guide(version, commit, *, can_resume=False):
    practice = (
        "Use Save or resume practice progress to download a local JSON progress file.\n"
        "On a later visit, choose that file, inspect the preview, then explicitly\n"
        "replace the current work to resume. Readable Markdown notes are a separate\n"
        "download and cannot restore progress. No notes are uploaded. The saved file\n"
        "is editable; it does not verify authorship, timing or personal mastery.\n"
        if can_resume
        else "Download readable notes before closing or reloading; this version has no\n"
        "progress-file restore control.\n"
    )
    return f"""CSM COPILOT — INTERVIEW DEMO {version}

Extract the entire ZIP and read this guide before opening index.html.
Start with the three-minute review route, or open project-brief.pdf.

Discuss one customer decision, one recorded AI mistake and one next learning
step. Write your own reasoning in Practice before revealing the guidance.
{practice}
Reloading clears the in-page notes. The package includes no personal responses.

This is an independent, AI-assisted portfolio project with synthetic records.
It is not affiliated with Unity. The static replay does not run a model, send
messages or connect to customer systems. External documentation links require
internet access. Copy controls prepare public URLs, not local-file links.

The application has been browser-tested over HTTP. Direct file opening was not
browser-verified because the automated browser policy disallows file URLs.
Local script and clipboard behavior depends on the reader's browser. Use the
PDF or hosted demo if your browser restricts local files.

Hosted review: https://yuchi-wang02.github.io/csm-copilot/#start
For a local HTTP review, if Python is already installed, open a terminal in the
extracted csm-copilot-demo folder and run:
  python -m http.server 8000 --bind 127.0.0.1
Then open http://127.0.0.1:8000/#start in your browser. Stop the server with Ctrl+C.
The PDF is a readable introduction if you do not want to run a local server.

Source: https://github.com/Yuchi-Wang02/csm-copilot
Source commit: {commit}
Project version: {version}
Bundle format: {FORMAT}

SHA256SUMS.json records each included file's digest and source identity.
These hashes establish file identity, not a signature or security audit.
AI-assisted implementation and tests do not establish personal mastery,
independent model reliability or customer usefulness.
""".encode()


def build_bundle(root=ROOT, ref="HEAD"):
    commit = git(root, "rev-parse", "--verify", "--end-of-options", f"{ref}^{{commit}}")
    commit = commit.decode().strip()
    project = tomllib.loads(git(root, "show", f"{commit}:pyproject.toml").decode())
    version = project["project"]["version"]
    entries = git(root, "ls-tree", "-rz", "--full-tree", commit, "--", "demo").split(b"\0")
    files = {}
    for entry in filter(None, entries):
        metadata, raw_path = entry.split(b"\t", 1)
        mode, kind, blob = metadata.decode().split()
        path = PurePosixPath(raw_path.decode("utf-8"))
        if mode != "100644" or kind != "blob":
            raise ValueError(f"Only regular static files may be packaged: {path}")
        if path.parts[0] != "demo" or ".." in path.parts or "\\" in str(path):
            raise ValueError(f"Invalid package path: {path}")
        name = str(path.relative_to("demo"))
        if name in {"START_HERE.txt", "SHA256SUMS.json"}:
            raise ValueError(f"Reserved bundle filename: {name}")
        files[name] = git(root, "cat-file", "blob", blob)
    if "index.html" not in files or "project-brief.pdf" not in files:
        raise ValueError("Committed demo needs index.html and project-brief.pdf")
    validate_references(files)
    source_hashes = {name: hashlib.sha256(data).hexdigest() for name, data in sorted(files.items())}
    files["START_HERE.txt"] = start_guide(
        version, commit, can_resume="practice-session.js" in files
    )
    manifest = {
        "bundle_format": FORMAT,
        "project_version": version,
        "source_commit": commit,
        "source_files": source_hashes,
        "package_additions": {
            "START_HERE.txt": hashlib.sha256(files["START_HERE.txt"]).hexdigest(),
        },
    }
    files["SHA256SUMS.json"] = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode()
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_STORED) as bundle:
        for name, data in sorted(files.items()):
            info = zipfile.ZipInfo(PREFIX + name, date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            bundle.writestr(info, data)
    return buffer.getvalue(), manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--ref", default="HEAD", help="Committed revision; worktree edits are excluded"
    )
    parser.add_argument("--output", type=Path, default=ROOT / "dist/interview-demo.zip")
    args = parser.parse_args()
    try:
        data, manifest = build_bundle(ref=args.ref)
    except (ValueError, subprocess.CalledProcessError) as error:
        parser.exit(2, f"Cannot build committed interview demo: {error}\n")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(data)
    print(
        json.dumps(
            {
                "output": str(args.output),
                "source_commit": manifest["source_commit"],
                "project_version": manifest["project_version"],
                "sha256": hashlib.sha256(data).hexdigest(),
                "bytes": len(data),
            }
        )
    )


if __name__ == "__main__":
    main()
