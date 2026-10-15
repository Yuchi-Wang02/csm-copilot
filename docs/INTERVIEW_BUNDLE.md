# Build a portable interview demo

The [v0.30.0 prerelease](https://github.com/Yuchi-Wang02/csm-copilot/releases/tag/v0.30.0) is a fixed interview package pinned to commit `d899e2625bb3aaf5cb9a8d8b3ee67a2794c338da`. It includes the interactive case explorer, bilingual review briefs, five practice decisions, seventeen recorded model attempts, the two-page project brief and the one-page publisher teaching handout.

Compared with v0.29.8, seven additional recordings follow a queue-first morning review. The replay exposes host planning assistance, saved requests, final-field rejections and an exact context-omission audit. The latest pair returned sooner with reduced input but retained the same citation error. These are inspectable development attempts, not a model ranking or general performance benchmark. The tagged Python source includes the optional host policies and request-preservation changes; Python does not execute inside the static ZIP.

## Choose the right take-away

| Item | Use it for |
|---|---|
| [Hosted portfolio](https://yuchi-wang02.github.io/csm-copilot/) | Open the interactive review with no setup; it may advance after this release |
| [csm-copilot-demo-v0.30.0.zip](https://github.com/Yuchi-Wang02/csm-copilot/releases/download/v0.30.0/csm-copilot-demo-v0.30.0.zip) | Keep a fixed static demo with both PDFs, review briefs and recorded results |
| GitHub's Source code archives on the release page | Inspect the Python implementation, tests and full documentation at the tag |

Extract the entire ZIP and read `START_HERE.txt`. Start with `project-brief.pdf` for the overview or `publisher-teaching-example.pdf` for a customer-education example. The guide provides a localhost HTTP command for the interactive review. Direct file opening remains unverified; use the PDFs or hosted site if local browser restrictions prevent the walkthrough.

Write your own practice reasoning before revealing guidance. Save a progress JSON file to resume later; readable Markdown notes are a separate download. The package includes no personal responses. See [practice-file compatibility and limits](PRACTICE.md#resume-without-rewriting-the-learning-record).

The full Markdown guides are not separate files inside the demo ZIP. For this exact release, use the pinned [learning guide](https://github.com/Yuchi-Wang02/csm-copilot/blob/d899e2625bb3aaf5cb9a8d8b3ee67a2794c338da/docs/LEARNING.md), [interview script](https://github.com/Yuchi-Wang02/csm-copilot/blob/d899e2625bb3aaf5cb9a8d8b3ee67a2794c338da/docs/INTERVIEW.md), [model experiment notes](https://github.com/Yuchi-Wang02/csm-copilot/blob/d899e2625bb3aaf5cb9a8d8b3ee67a2794c338da/docs/LOCAL_MODEL.md) and [local setup guide](https://github.com/Yuchi-Wang02/csm-copilot/blob/d899e2625bb3aaf5cb9a8d8b3ee67a2794c338da/docs/LOCAL_SETUP.md). External documentation requires internet access; application links may point to the evolving site or repository.

## Verify the fixed package

The published ZIP is **2,134,863 bytes**. Its SHA-256 is:

```text
85504841bc0557c12219047f63adc7bad921b8a48dc99131b5726153e88dbe10
```

In PowerShell, from the folder containing the download:

```powershell
Get-FileHash -LiteralPath .\csm-copilot-demo-v0.30.0.zip -Algorithm SHA256
```

The release also provides a `.zip.sha256` file. All 26 committed demo files were checked byte-for-byte against the pinned Git tree, the generated guide matched its manifest hash, and ZIP integrity passed. With `START_HERE.txt` and `SHA256SUMS.json`, the archive contains 28 entries. Downloaded Windows and Ubuntu CI archives match the local build exactly. The public ZIP and checksum downloads also match the local files. The [source verification run](https://github.com/Yuchi-Wang02/csm-copilot/actions/runs/38669105626) passed 514 Python tests, 111 JavaScript tests, generated-artifact checks and isolated installed CLI/MCP checks on both runners.

An earlier preparation commit failed the generated-artifact check because two diagnostic reports retained the old version. Those reports were regenerated before selecting the release's source commit. The published package uses the corrected, passing revision.

The extracted package was opened over localhost HTTP in Edge. Checks covered the v0.30.0 banner, seventeen recording choices, the final-turn rejection and omitted-message audit, Android's evidence-request follow-up, iOS's launch-plan review and the issue handoff's three missing intake fields. No browser errors were recorded during those interactions. The PDFs match the committed, previously rendered files; this packaging pass did not change their content or repeat every prior practice, clipboard or responsive-layout check. No personal practice response or new model inference was produced.

Eight ZIP entries differ from v0.29.8: manifest, start guide, app script, versioned data, index page, model recordings, turn renderer and project brief. The teaching PDF, customer review briefs and practice modules are unchanged. Every raw model recording and its review file remain unchanged from the previously published seventeen-run source.

These checks establish file identity and the observed behaviors. They do not establish independent model reliability, customer impact or personal mastery. Earlier clipboard payload read-back and native leave-page-prompt limitations remain; use the read-only text fields for manual copying and save progress JSON to retain practice work. The [v0.29.8 package](https://github.com/Yuchi-Wang02/csm-copilot/releases/tag/v0.29.8) and its [verification notes](https://github.com/Yuchi-Wang02/csm-copilot/blob/1320c312e655143b6114765b848ee41203cdf6f2/docs/INTERVIEW_BUNDLE.md) remain available as a separate historical snapshot.

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

The earlier [v0.20.1 ZIP](https://github.com/Yuchi-Wang02/csm-copilot/releases/tag/v0.20.1) was packaged manually, with demo files checked against its tagged source. The reproducible archive format does not reproduce that historical ZIP's bytes or replace its assets. The v0.21.0, v0.23.0, v0.25.0, v0.27.1, v0.28.0, v0.28.2, v0.29.1, v0.29.3, v0.29.4, v0.29.5, v0.29.6 and v0.29.7 releases remain separate fixed snapshots.

The static application has been browser-tested over HTTP. Direct file opening was not browser-verified because the automated browser policy disallows `file://` navigation. Local script and clipboard behavior can vary; use the included PDF or hosted demo if local-file restrictions prevent the interactive walkthrough. Practice notes are not part of the package and are not uploaded by the builder.
