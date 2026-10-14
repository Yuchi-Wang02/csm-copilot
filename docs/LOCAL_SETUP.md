# Run CSM Copilot locally

Install the Python workflow, export a review, or connect an MCP host. The bundled synthetic workflow needs no model or API key. For the browser portfolio, [open the hosted demo](https://yuchi-wang02.github.io/csm-copilot/).

[Back to the project overview](../README.md)

Python **3.11–3.13**; verified locally on Windows / Python 3.13. GitHub Actions tests Windows and Ubuntu.

```sh
git clone https://github.com/Yuchi-Wang02/csm-copilot.git
cd csm-copilot
python -m venv .venv
```

Activate the environment:

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

```sh
# macOS / Linux
source .venv/bin/activate
```

Then install and verify:

```sh
python -m pip install -e ".[dev]"
csm-demo --format summary
python -m pytest -q
python scripts/mcp_smoke.py --output evidence/mcp-transcript.json
python scripts/build_demo.py
python -m http.server 8000 --directory demo
```

Open `http://localhost:8000`. Browser verification uses HTTP; direct-file opening of `demo/index.html` remains unverified in this environment. The optional Google Fonts request falls back to local system fonts when offline. No account data leaves the page.

To check the distributable package as well as the editable checkout:

```sh
python -m build
python scripts/verify_wheel.py
```

This creates a temporary clean environment, installs the built wheel and its dependencies, and runs both installed commands outside the repository. It checks the JSON workflow, English and Chinese exports, and real MCP results against the published artifacts. Dependency installation requires package-index access; no model or API key is needed. Both CI operating systems run this check. See [verification details](VERIFICATION.md#installed-package-check).

For a first terminal walkthrough, run `csm-demo --format summary`. It prints the original queue, each platform's decision, unknown/failed check IDs, next actions and handoff missing fields in English. [Preview the generated summary](../evidence/morning-summary.txt). No model or API key is required; the snapshot is fixed and nothing is sent. Use `--output morning-summary.txt` to save it. Summary format covers the full queue; platform selection and Chinese customer drafts use Markdown.

To print the full review packet without a browser:

```sh
csm-demo --output review-packet.json
csm-demo --format markdown --lang en --output morning-review.md
csm-demo --format markdown --lang zh --output morning-review-zh.md
```

For a focused leave-behind, use the **selected platform brief** links inside the case panel. Each contains only that platform's findings, follow-up, handoffs and source records, plus its account's contact evidence. Choose English or Chinese customer drafts independently of the displayed review step. The brief preserves the original snapshot; the separate synthetic-update comparison is excluded.

The same export is available from the CLI:

```sh
csm-demo --format markdown --integration harbor_android --lang en --output harbor-handoff.md
csm-demo --format markdown --integration lantern_ios --lang zh --output ios-review-zh.md
```

An unknown or unqueued integration produces an error before writing the output. `--integration` requires Markdown format; JSON continues to export the complete workflow. See [export scope and examples](REVIEW_BRIEF.md#export-one-platform).

### Connect an MCP host

After installation, configure a stdio server with the **absolute Python path inside the environment**:

```json
{
  "mcpServers": {
    "csm-copilot": {
      "command": "/absolute/path/to/csm-copilot/.venv/bin/python",
      "args": ["-m", "csm_copilot.server"]
    }
  }
}
```

Windows example: `"command": "C:\\projects\\csm-copilot\\.venv\\Scripts\\python.exe"`. No working directory is required because fixtures are packaged with the module. Host configuration formats vary; see [MCP setup and demo prompts](MCP.md).

Use the [current morning-review prompt](MCP.md#suggested-live-prompt) to include stale contacts and unknown-contact entries, preserve platform scope, and prepare follow-ups and handoffs with citations.

For the complete reproduction sequence, including JavaScript checks and PDF generation, follow [Verification](VERIFICATION.md#reproduction). PDF builders require the optional `brief` dependencies: `python -m pip install -e ".[dev,brief]"`.
