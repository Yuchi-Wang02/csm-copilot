# Build a portable interview demo

The [v0.30.2 prerelease](https://github.com/Yuchi-Wang02/csm-copilot/releases/tag/v0.30.2) is a fixed interview package pinned to commit `322da4407bdbdae6308d3a4a959189fe6d0c681b`. It includes the interactive case explorer, bilingual review briefs, six practice decisions, nineteen recorded model attempts, two PDFs and an English presenter guide.

Compared with v0.30.1, this snapshot adds two morning recordings, the before/after citation correction, explicit explanation-guidance disclosure, and three model-excerpt comparisons with recorded next actions. The morning overview now contains nine attempts. `PRESENTATION.txt` adds an optional discussion of why an accurate status can still omit a useful next step. It supplies preparation prompts without claiming personal practice is complete. The prior [v0.30.1 release](https://github.com/Yuchi-Wang02/csm-copilot/releases/tag/v0.30.1) and its [verification notes](https://github.com/Yuchi-Wang02/csm-copilot/blob/09eacdf7e780649e8204b68ffc6396933fdb1c41/docs/INTERVIEW_BUNDLE.md) remain a separate fixed snapshot.

## Choose the right take-away

| Item | Use it for |
|---|---|
| [Hosted portfolio](https://yuchi-wang02.github.io/csm-copilot/) | Open the interactive review with no setup; it may advance after this release |
| [csm-copilot-demo-v0.30.2.zip](https://github.com/Yuchi-Wang02/csm-copilot/releases/download/v0.30.2/csm-copilot-demo-v0.30.2.zip) | Keep a fixed static demo with PDFs, review briefs, recorded results and presenter instructions |
| `PRESENTATION.txt` inside the ZIP | Rehearse one customer decision, one recorded AI mistake and a learning step you can explain |
| GitHub's Source code archives on the release page | Inspect the Python implementation, tests and full documentation at the tag |

Extract the entire ZIP and read `START_HERE.txt`. Open `PRESENTATION.txt` for the speaking route, `project-brief.pdf` for the overview or `publisher-teaching-example.pdf` for a customer-education example. The start guide provides a localhost HTTP command for the interactive review. Direct file opening remains unverified; use the PDFs or hosted site if local browser restrictions prevent the walkthrough.

Write your own practice reasoning before revealing guidance. Save a progress JSON file to resume later; readable Markdown notes are a separate download. The package includes no personal responses. Compatible five-decision files retain their saved responses and add the sixth decision blank, after a preview and explicit replacement. A six-decision file cannot resume in the older v0.30.0 application. See [practice-file compatibility and limits](PRACTICE.md#resume-without-rewriting-the-learning-record).

The full Markdown guides are not separate files inside the demo ZIP. For this exact source, use the pinned [learning guide](https://github.com/Yuchi-Wang02/csm-copilot/blob/322da4407bdbdae6308d3a4a959189fe6d0c681b/docs/LEARNING.md), [interview script](https://github.com/Yuchi-Wang02/csm-copilot/blob/322da4407bdbdae6308d3a4a959189fe6d0c681b/docs/INTERVIEW.md) and [local setup guide](https://github.com/Yuchi-Wang02/csm-copilot/blob/322da4407bdbdae6308d3a4a959189fe6d0c681b/docs/LOCAL_SETUP.md). Those source guides may refer to the prior release as current; this page records the new package identity. External documentation and application sharing links require internet access and may lead to the evolving site or repository. Python and model inference do not execute inside the static ZIP.

## Verify the fixed package

The published ZIP is **3,078,260 bytes**. Its SHA-256 is:

```text
575477b27cca21439aa3d9bb166a59a55be7ac8fb529e29801fcbebc704bc9ad
```

In PowerShell, from the folder containing the download:

```powershell
Get-FileHash -LiteralPath .\csm-copilot-demo-v0.30.2.zip -Algorithm SHA256
```

The release also provides a `.zip.sha256` file. All 27 committed demo files were checked byte-for-byte against the pinned Git tree; the generated guide matched its manifest hash and ZIP integrity passed. With `START_HERE.txt` and `SHA256SUMS.json`, the archive contains 29 entries. Downloaded Windows and Ubuntu CI archives match the local build exactly. The public ZIP and checksum downloads also match the local files. The [source verification run](https://github.com/Yuchi-Wang02/csm-copilot/actions/runs/38678144787) passed 543 Python tests, 124 JavaScript tests, generated-artifact checks and isolated installed CLI/MCP checks on both runners.

The extracted package was opened over localhost HTTP in Edge. Checks covered the v0.30.2 banner, presenter-download target, nineteen recording choices, nine-attempt comparison, blank six-decision practice, and three excerpt-to-action comparisons including the handoff's raw source locations. The opening layout was visually inspected and no browser errors were recorded in those interactions. This packaging pass did not repeat every earlier practice-import, clipboard, keyboard or responsive-layout check. Those checks remain version-specific observations in the [development notes](DEVELOPMENT.md).

Both PDFs, every raw model recording and their review findings retain their prior content. No personal practice response or new model inference was produced. The comparison presents changing development attempts, not a controlled benchmark. File identity and these observed behaviors do not establish independent model reliability, customer impact or personal mastery. Earlier clipboard payload read-back and native leave-page-prompt limitations remain; use the read-only text fields for manual copying and save progress JSON to retain work.

## Rebuild from source

From a checkout containing the builder, run with Python 3.11 or newer and Git:

```sh
python scripts/build_interview_demo.py --output dist/interview-demo.zip
```

The command prints the selected commit, project version, archive size and SHA-256. It reads the committed `demo/` tree directly. Uncommitted changes and untracked notes are excluded, even when they are inside `demo/`. Commit an intended demo change before packaging it. `--ref <commit-or-tag>` selects another locally available revision; the current builder is still used.

To reproduce an archive byte-for-byte, use the same builder revision and selected source commit. The `csm-interview-bundle-v1` format uses sorted entries, fixed ZIP timestamps and permissions, and uncompressed bytes to avoid compression-library differences. File hashes and source identity are recorded in `SHA256SUMS.json`. These establish file identity, not authenticity, safety or correctness of the synthetic evidence.

The generated start guide includes a localhost preview command and detects whether the selected committed demo contains the practice-resume module and presenter guide, so older revisions do not receive unavailable-control instructions. The package contains the committed demo files plus two generated additions: `START_HERE.txt` and `SHA256SUMS.json`. The builder rejects committed symlinks, collisions with those reserved names, and missing local HTML script/link targets. It does not crawl external documentation or analyze every dynamically constructed URL. The application's existing behavior checks remain separate.

Both Windows and Ubuntu CI build a bundle from the checked-out commit and upload it as `interview-demo-<runner>-<attempt>`. Compare the inner `interview-demo.zip` hashes to check agreement across environments; the surrounding GitHub artifact archives are separate transport containers. Build success alone does not establish matching bytes between runners.

Six focused checks cover identical output despite dirty worktree edits and CRLF settings, original Git bytes and manifest hashes, missing local assets, pinned older commits and their appropriate practice and presenter instructions, committed symlinks, reserved filenames, and query/fragment/external-link handling.

The earlier [v0.20.1 ZIP](https://github.com/Yuchi-Wang02/csm-copilot/releases/tag/v0.20.1) was packaged manually, with demo files checked against its tagged source. The reproducible archive format does not reproduce that historical ZIP's bytes or replace its assets. The v0.21.0, v0.23.0, v0.25.0, v0.27.1, v0.28.0, v0.28.2, v0.29.1, v0.29.3, v0.29.4, v0.29.5, v0.29.6 and v0.29.7 releases remain separate fixed snapshots.

The static application has been browser-tested over HTTP. Direct file opening was not browser-verified because the automated browser policy disallows `file://` navigation. Local script and clipboard behavior can vary; use the included PDF or hosted demo if local-file restrictions prevent the interactive walkthrough. Practice notes are not part of the package and are not uploaded by the builder.
