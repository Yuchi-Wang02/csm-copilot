import hashlib
import io
import json
import subprocess
import zipfile

import pytest

from scripts.build_interview_demo import PREFIX, build_bundle, validate_references


def command(root, *args, data=None):
    return subprocess.check_output(["git", *args], cwd=root, input=data, stderr=subprocess.PIPE)


@pytest.fixture
def source_repo(tmp_path):
    command(tmp_path, "init", "-q")
    command(tmp_path, "config", "user.name", "Bundle Test")
    command(tmp_path, "config", "user.email", "bundle-test@example.invalid")
    command(tmp_path, "config", "core.autocrlf", "false")
    (tmp_path / "demo").mkdir()
    (tmp_path / "pyproject.toml").write_text('[project]\nversion = "1.2.3"\n', encoding="utf-8")
    (tmp_path / "demo/index.html").write_bytes(
        b'<script src="app.js?v=1"></script><a href="project-brief.pdf">Brief</a>'
    )
    (tmp_path / "demo/app.js").write_bytes("const message = 'Hello / 你好';\n".encode())
    (tmp_path / "demo/project-brief.pdf").write_bytes(b"%PDF-1.4\n\x00\xff")
    command(tmp_path, "add", ".")
    command(tmp_path, "commit", "-qm", "Synthetic bundle fixture")
    return tmp_path


def test_bundle_is_identical_across_worktree_edits_and_line_ending_settings(source_repo):
    before, manifest = build_bundle(source_repo)
    command(source_repo, "config", "core.autocrlf", "true")
    (source_repo / "demo/app.js").write_bytes(b"uncommitted replacement\r\n")
    (source_repo / "demo/private-note.txt").write_text("Do not package untracked work.")
    after, _ = build_bundle(source_repo)
    assert before == after
    with zipfile.ZipFile(io.BytesIO(after)) as bundle:
        assert bundle.testzip() is None
        assert PREFIX + "private-note.txt" not in bundle.namelist()
        for name, expected_hash in manifest["source_files"].items():
            content = bundle.read(PREFIX + name)
            assert hashlib.sha256(content).hexdigest() == expected_hash
            assert content == command(source_repo, "show", "HEAD:demo/" + name)
        assert all(item.date_time == (1980, 1, 1, 0, 0, 0) for item in bundle.infolist())
        assert json.loads(bundle.read(PREFIX + "SHA256SUMS.json")) == manifest


def test_missing_local_asset_fails_instead_of_shipping_a_broken_demo(source_repo):
    command(source_repo, "rm", "-q", "demo/app.js")
    command(source_repo, "commit", "-qm", "Remove required asset")
    with pytest.raises(ValueError, match="Missing packaged link"):
        build_bundle(source_repo)


def test_commit_selection_keeps_old_demo_bytes_after_a_later_commit(source_repo):
    first_commit = command(source_repo, "rev-parse", "HEAD").decode().strip()
    before, _ = build_bundle(source_repo, first_commit)
    (source_repo / "demo/app.js").write_bytes(b"const message = 'new revision';\n")
    command(source_repo, "add", ".")
    command(source_repo, "commit", "-qm", "Change the example")
    assert build_bundle(source_repo, first_commit)[0] == before
    assert build_bundle(source_repo)[0] != before


def test_committed_symlinks_are_rejected_without_reading_the_target(source_repo):
    blob = command(source_repo, "hash-object", "-w", "--stdin", data=b"../private-note.txt")
    command(
        source_repo,
        "update-index",
        "--add",
        "--cacheinfo",
        "120000",
        blob.decode().strip(),
        "demo/link",
    )
    command(source_repo, "commit", "-qm", "Add a synthetic link")
    with pytest.raises(ValueError, match="Only regular static files"):
        build_bundle(source_repo)


def test_bundle_additions_cannot_overwrite_committed_content(source_repo):
    (source_repo / "demo/START_HERE.txt").write_text("Existing source content")
    command(source_repo, "add", ".")
    command(source_repo, "commit", "-qm", "Reserve a name")
    with pytest.raises(ValueError, match="Reserved bundle filename"):
        build_bundle(source_repo)


def test_link_check_keeps_queries_fragments_and_external_docs_separate():
    validate_references(
        {
            "index.html": b'<script src="app.js?v=1"></script><a href="#practice">Practice</a>'
            b'<a href="?probe=known#triage">Probe</a><a href="https://example.com/docs">Docs</a>',
            "app.js": b"",
        }
    )
    with pytest.raises(ValueError, match="Root-relative link"):
        validate_references({"index.html": b'<script src="/app.js"></script>', "app.js": b""})
