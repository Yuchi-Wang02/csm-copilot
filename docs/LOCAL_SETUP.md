# Run CSM Copilot locally

Choose the path that matches what you want to inspect. All three use synthetic records; none requires a model or API key.

| Your goal | Start here | Requirements |
|---|---|---|
| Present or explore the case | [Hosted three-minute review](https://yuchi-wang02.github.io/csm-copilot/#start), or [local replay below](#view-the-browser-replay) | A browser; local replay also uses Git and Python's standard-library HTTP server |
| Run the workflow and export a brief | [Install the Python workflow](#install-the-python-workflow) | Git, Python 3.11–3.13 and package-index access |
| Change the code or reproduce verification | [Develop and verify](#develop-and-verify) | Workflow installation plus development dependencies; full reproduction also uses Node.js |

[Back to the project overview](../README.md)

## View the browser replay

The committed `demo/` directory already contains the generated case data, saved model recordings, scripts and PDFs. You can serve it without installing the Python package or rebuilding anything:

```sh
git clone https://github.com/Yuchi-Wang02/csm-copilot.git
cd csm-copilot
python -m http.server 8000 --bind 127.0.0.1 --directory demo
```

Open **http://127.0.0.1:8000/#start**. Leave the terminal running while presenting; press **Ctrl+C** there when finished. If port 8000 is already in use, choose another port such as 8001 in both the command and browser address. The server listens only on your computer's loopback address.

You should see **Follow a decision. Inspect a mistake. Explain the learning.** Start with the Android follow-up, then compare the recorded AI claim with its tool result. This path replays committed outputs; it does not start an MCP server or run inference. Practice notes remain in page memory unless you explicitly download a file.

Browser verification uses HTTP. Direct-file opening of `demo/index.html` remains unverified. The optional Google Fonts request falls back to system fonts when offline; external source links still require internet access. For a fixed release instead of the current checkout, use the [portable interview package](INTERVIEW_BUNDLE.md).

## Install the Python workflow

Python **3.11–3.13**. The installed commands are verified by GitHub Actions on Windows / Python 3.13 and Ubuntu / Python 3.11; local system policies can impose additional restrictions.

Clone the repository and enter `csm-copilot` using the first two commands above if you have not already done so. Stop the preview server with Ctrl+C or use a second terminal in the checkout. Then create an environment:

```sh
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

Install the workflow and print the first review:

```sh
python -m pip install -e .
csm-demo --format summary
```

At the bundled snapshot, the output starts with `CSM Copilot - morning review` and reports **3 accounts, 4 platforms**. Find `Moon Garden / Android: blocked`, then compare it with `Moon Garden / iOS: checklist_complete` and `Meadow Notes / iOS: needs_evidence`. The [committed summary](../evidence/morning-summary.txt) is the complete reference output. This confirms the deterministic workflow ran; it does not establish model reasoning or customer outcomes.

If activation or an installed command is blocked by a local security policy, keep that restriction intact. The hosted or local browser replay remains available without running the installed package. The [verification record](VERIFICATION.md#reproduction) distinguishes successful CI checks from the development machine's launcher restriction.

## Develop and verify

From the activated environment, add development dependencies and run the authored Python checks:

```sh
python -m pip install -e ".[dev]"
python -m pytest -q
```

To regenerate the scripted MCP transcript and browser workflow data after changing their source:

```sh
python scripts/mcp_smoke.py --output evidence/mcp-transcript.json
python scripts/build_demo.py
git diff --stat
```

These builders overwrite generated files. Inspect the diff before committing; regeneration is not required just to view the existing demo. For the complete sequence, including JavaScript checks, model-replay packaging and both PDF builders, follow [Verification](VERIFICATION.md#reproduction). PDF generation needs the optional `brief` dependencies.

## Check the installed package

To check the distributable package as well as the editable checkout:

```sh
python -m build
python scripts/verify_wheel.py
```

This creates a temporary clean environment, installs the built wheel and its dependencies, and runs both installed commands outside the repository. It checks the JSON workflow, English and Chinese exports, and real MCP results against the published artifacts. Dependency installation requires package-index access; no model or API key is needed. Both CI operating systems run this check. See [verification details](VERIFICATION.md#installed-package-check).

## Export review briefs

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

## Connect an MCP host

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
