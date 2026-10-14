"""Install a built wheel in a fresh environment and exercise it outside the checkout."""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("wheel", type=Path, nargs="?", help="Default: current version in dist/")
    args = parser.parse_args()
    version = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"][
        "version"
    ]
    wheel = (args.wheel or ROOT / "dist" / f"csm_copilot-{version}-py3-none-any.whl").resolve()
    if not wheel.is_file():
        parser.error(f"Build the wheel first with python -m build: {wheel}")

    env = {k: v for k, v in os.environ.items() if k not in {"PYTHONPATH", "PYTHONHOME"}}
    env.update(PYTHONUTF8="1", PYTHONNOUSERSITE="1", PIP_DISABLE_PIP_VERSION_CHECK="1")
    with tempfile.TemporaryDirectory(prefix="csm-wheel-") as temporary:
        root = Path(temporary)
        outside = root / "outside checkout"
        outside.mkdir()
        venv = root / "isolated environment"

        def execute(command):
            result = subprocess.run(
                [str(part) for part in command],
                cwd=outside,
                env=env,
                text=True,
                encoding="utf-8",
                capture_output=True,
                timeout=180,
            )
            if result.returncode:
                raise RuntimeError(
                    f"Command failed ({result.returncode}): {command}\n"
                    f"{result.stdout}\n{result.stderr}"
                )
            return result.stdout

        execute([sys.executable, "-I", "-m", "venv", venv])
        binary_dir = venv / ("Scripts" if os.name == "nt" else "bin")
        suffix = ".exe" if os.name == "nt" else ""
        python = binary_dir / f"python{suffix}"
        execute([python, "-I", "-m", "pip", "install", "--quiet", wheel])
        origin = json.loads(
            execute(
                [
                    python,
                    "-I",
                    "-c",
                    "import json, csm_copilot; from importlib.metadata import version; "
                    "print(json.dumps({'file': csm_copilot.__file__, "
                    "'metadata_version': version('csm-copilot'), "
                    "'module_version': csm_copilot.__version__}))",
                ]
            )
        )
        assert Path(origin["file"]).resolve().is_relative_to(venv.resolve()), origin
        assert origin["metadata_version"] == origin["module_version"], origin
        demo = binary_dir / f"csm-demo{suffix}"
        actual = json.loads(execute([demo]))
        expected = json.loads((ROOT / "evidence/workflow.json").read_text(encoding="utf-8"))
        assert actual == expected, "Installed CLI JSON differs from the published workflow"
        for lang in ("en", "zh"):
            target = outside / "exports" / f"review-{lang}.md"
            execute([demo, "--format", "markdown", "--lang", lang, "--output", target])
            expected_text = (ROOT / f"evidence/morning-review-{lang}.md").read_text(
                encoding="utf-8"
            )
            assert target.read_text(encoding="utf-8") == expected_text, lang
        case_files = sorted((ROOT / "demo/case-briefs").glob("*.md"))
        expected_case_count = sum(len(p["integrations"]) for p in expected["packets"]) * 2
        assert len(case_files) == expected_case_count, "Missing or stale platform briefs"
        for case_file in case_files:
            integration_id, lang = case_file.stem.rsplit("-", 1)
            actual_text = execute(
                [demo, "--format", "markdown", "--integration", integration_id, "--lang", lang]
            )
            assert actual_text == case_file.read_text(encoding="utf-8"), case_file.name
        smoke = outside / "mcp_smoke.py"
        shutil.copyfile(ROOT / "scripts/mcp_smoke.py", smoke)
        transcript = outside / "mcp-transcript.json"
        execute(
            [
                python,
                "-I",
                smoke,
                "--server-command",
                binary_dir / f"csm-copilot{suffix}",
                "--output",
                transcript,
            ]
        )
        observed = json.loads(transcript.read_text(encoding="utf-8"))
        baseline = json.loads((ROOT / "evidence/mcp-transcript.json").read_text(encoding="utf-8"))
        assert observed == baseline, "Installed MCP behavior differs from the published transcript"
        print(
            f"PASS: wheel {origin['metadata_version']}; isolated installed module; "
            "CLI JSON, both queue exports and all platform briefs match; eight-tool MCP console entry point "
            "matches the published transcript. No model inference."
        )


if __name__ == "__main__":
    main()
