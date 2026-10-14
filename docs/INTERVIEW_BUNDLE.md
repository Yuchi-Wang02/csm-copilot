# Build a portable interview demo

The [v0.29.4 prerelease](https://github.com/Yuchi-Wang02/csm-copilot/releases/tag/v0.29.4) is a fixed interview package pinned to commit `33e83059d3f9ff2b6e5486407ae3bb449fbff664`. It includes the interactive case explorer, bilingual review briefs, five practice decisions, ten recorded model attempts, the two-page project brief and the one-page publisher teaching handout.

Compared with v0.29.3, the original batch attempt now pairs two model excerpts with fields extracted from the same historical trace. Evidence disclosures also have a consistent keyboard focus outline. The source interview guide describes both presentation improvements, and the generated start guide follows the current customer-decision, AI-mistake and learning-step route. The static demo does not execute the Python server or run model inference.

## Choose the right take-away

| Item | Use it for |
|---|---|
| [Hosted portfolio](https://yuchi-wang02.github.io/csm-copilot/) | Open the interactive review with no setup; it may advance after this release |
| [csm-copilot-demo-v0.29.4.zip](https://github.com/Yuchi-Wang02/csm-copilot/releases/download/v0.29.4/csm-copilot-demo-v0.29.4.zip) | Keep a fixed static demo with both PDFs, review briefs and recorded results |
| GitHub's Source code archives on the release page | Inspect the Python implementation, tests and full documentation at the tag |

Extract the entire demo ZIP and read `START_HERE.txt`. Start with `project-brief.pdf` for the overview or `publisher-teaching-example.pdf` for a customer-education example. The guide provides a localhost HTTP command for the interactive review. Direct file opening remains unverified; use the PDFs or hosted site if local browser restrictions prevent the walkthrough.

Write your own practice reasoning before revealing guidance. Save a progress JSON file to resume later; readable Markdown notes are a separate download. The package includes no personal responses. See [practice-file compatibility and limits](PRACTICE.md#resume-without-rewriting-the-learning-record).

The full Markdown guides are not separate files inside the demo ZIP. For this exact release, use the pinned [learning guide](https://github.com/Yuchi-Wang02/csm-copilot/blob/33e83059d3f9ff2b6e5486407ae3bb449fbff664/docs/LEARNING.md), [interview script](https://github.com/Yuchi-Wang02/csm-copilot/blob/33e83059d3f9ff2b6e5486407ae3bb449fbff664/docs/INTERVIEW.md), [teaching example](https://github.com/Yuchi-Wang02/csm-copilot/blob/33e83059d3f9ff2b6e5486407ae3bb449fbff664/docs/CLIENT_EDUCATION.md) and [local setup guide](https://github.com/Yuchi-Wang02/csm-copilot/blob/33e83059d3f9ff2b6e5486407ae3bb449fbff664/docs/LOCAL_SETUP.md). External documentation requires internet access; application links may point to the evolving site or repository.

## Verify the fixed package

The published ZIP is **843,028 bytes**. Its SHA-256 is:

```text
4c4dfc26adb1634ea7271f634bbf44f3e412e96dacae48e433cd88ecf05734aa
```

In PowerShell, from the folder containing the download:

```powershell
Get-FileHash -LiteralPath .\csm-copilot-demo-v0.29.4.zip -Algorithm SHA256
```

The release also provides a `.zip.sha256` file. All 26 committed demo files were checked byte-for-byte against the pinned Git tree, the generated guide matched its manifest hash, and ZIP integrity passed. With `START_HERE.txt` and `SHA256SUMS.json`, the archive contains 28 entries. The local, Windows and Ubuntu builds produced the same inner ZIP checksum in [the source commit's CI run](https://github.com/Yuchi-Wang02/csm-copilot/actions/runs/38636828232), which passed 317 Python tests, 82 JavaScript tests and installed CLI/MCP checks on both runners.

The extracted package was opened over localhost HTTP. The review route reached the original claim comparison with its recorded values. Both PDF download controls returned files matching the packaged/source bytes, with no browser errors recorded during those checks. Earlier workflow, reset and save/resume observations remain in [Verification](VERIFICATION.md); they were not all repeated for this packaging pass. No new model inference was performed. These checks establish specific behavior and file identity, not independent model reliability, customer impact or personal mastery.

## Rebuild from source

From a checkout containing the builder, run with Python 3.11 or newer and Git:

```sh
python scripts/build_interview_demo.py --output dist/interview-demo.zip
```

The command prints the selected commit, project version, archive size and SHA-256. It reads the committed `demo/` tree directly. Uncommitted changes and untracked notes are excluded, even when they are inside `demo/`. Commit an intended demo change before packaging it. `--ref <commit-or-tag>` selects another locally available revision; the current builder is still used.

To reproduce an archive byte-for-byte, use the same builder revision and selected source commit. The `csm-interview-bundle-v1` format uses sorted entries, fixed ZIP timestamps and permissions, and uncompressed bytes to avoid compression-library differences. File hashes and source identity are recorded in `SHA256SUMS.json`. These establish file identity, not authenticity, safety or correctness of the synthetic evidence.

The generated start guide includes a localhost preview command and detects whether the selected committed demo contains the practice-resume module, so older revisions do not receive unavailable-control instructions. The package contains the committed demo files plus two generated additions: `START_HERE.txt` and `SHA256SUMS.json`. The builder rejects committed symlinks, collisions with those reserved names, and missing local HTML script/link targets. It does not crawl external documentation or analyze every dynamically constructed URL. The application's existing behavior checks remain separate.

Both Windows and Ubuntu CI build a bundle from the checked-out commit and upload it as `interview-demo-<runner>-<attempt>`. Compare the inner `interview-demo.zip` hashes to check agreement across environments; the surrounding GitHub artifact archives are separate transport containers. Build success alone does not establish matching bytes between runners.

Six focused checks cover identical output despite dirty worktree edits and CRLF settings, original Git bytes and manifest hashes, missing local assets, pinned older commits and their appropriate practice instructions, committed symlinks, reserved filenames, and query/fragment/external-link handling.

The earlier [v0.20.1 ZIP](https://github.com/Yuchi-Wang02/csm-copilot/releases/tag/v0.20.1) was packaged manually, with demo files checked against its tagged source. The reproducible archive format does not reproduce that historical ZIP's bytes or replace its assets. The v0.21.0, v0.23.0, v0.25.0, v0.27.1, v0.28.0, v0.28.2, v0.29.1 and v0.29.3 releases remain separate fixed snapshots.

The static application has been browser-tested over HTTP. Direct file opening was not browser-verified because the automated browser policy disallows `file://` navigation. Local script and clipboard behavior can vary; use the included PDF or hosted demo if local-file restrictions prevent the interactive walkthrough. Practice notes are not part of the package and are not uploaded by the builder.
