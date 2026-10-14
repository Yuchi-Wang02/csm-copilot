# Build a portable interview demo

The [v0.29.6 prerelease](https://github.com/Yuchi-Wang02/csm-copilot/releases/tag/v0.29.6) is a fixed interview package pinned to commit `02a8b30a018f54d607b0e9e6aca83258538caf10`. It includes the interactive case explorer, bilingual review briefs, five practice decisions, ten recorded model attempts, the two-page project brief and the one-page publisher teaching handout.

Compared with v0.29.5, the queue exposes dated contact evidence and preserves unknown contact, overdue planned dates and recorded live stages. Copied handoffs and downloadable review briefs carry field-source comparisons, including explicit disagreement and unavailable-source warnings. Missing field-source entries no longer stop Markdown exports. The static demo does not execute the Python server or run model inference.

## Choose the right take-away

| Item | Use it for |
|---|---|
| [Hosted portfolio](https://yuchi-wang02.github.io/csm-copilot/) | Open the interactive review with no setup; it may advance after this release |
| [csm-copilot-demo-v0.29.6.zip](https://github.com/Yuchi-Wang02/csm-copilot/releases/download/v0.29.6/csm-copilot-demo-v0.29.6.zip) | Keep a fixed static demo with both PDFs, review briefs and recorded results |
| GitHub's Source code archives on the release page | Inspect the Python implementation, tests and full documentation at the tag |

Extract the entire demo ZIP and read `START_HERE.txt`. Start with `project-brief.pdf` for the overview or `publisher-teaching-example.pdf` for a customer-education example. The guide provides a localhost HTTP command for the interactive review. Direct file opening remains unverified; use the PDFs or hosted site if local browser restrictions prevent the walkthrough.

Write your own practice reasoning before revealing guidance. Save a progress JSON file to resume later; readable Markdown notes are a separate download. The package includes no personal responses. See [practice-file compatibility and limits](PRACTICE.md#resume-without-rewriting-the-learning-record).

The full Markdown guides are not separate files inside the demo ZIP. For this exact release, use the pinned [learning guide](https://github.com/Yuchi-Wang02/csm-copilot/blob/02a8b30a018f54d607b0e9e6aca83258538caf10/docs/LEARNING.md), [interview script](https://github.com/Yuchi-Wang02/csm-copilot/blob/02a8b30a018f54d607b0e9e6aca83258538caf10/docs/INTERVIEW.md), [teaching example](https://github.com/Yuchi-Wang02/csm-copilot/blob/02a8b30a018f54d607b0e9e6aca83258538caf10/docs/CLIENT_EDUCATION.md) and [local setup guide](https://github.com/Yuchi-Wang02/csm-copilot/blob/02a8b30a018f54d607b0e9e6aca83258538caf10/docs/LOCAL_SETUP.md). External documentation requires internet access; application links may point to the evolving site or repository.

## Verify the fixed package

The published ZIP is **860,678 bytes**. Its SHA-256 is:

```text
9698803fe7d68c79c099f3326137ef13c75b83301d5c5af6d62033f314cc305e
```

In PowerShell, from the folder containing the download:

```powershell
Get-FileHash -LiteralPath .\csm-copilot-demo-v0.29.6.zip -Algorithm SHA256
```

The release also provides a `.zip.sha256` file. All 26 committed demo files were checked byte-for-byte against the pinned Git tree, the generated guide matched its manifest hash, and ZIP integrity passed. With `START_HERE.txt` and `SHA256SUMS.json`, the archive contains 28 entries. The local, Windows and Ubuntu builds produced the same inner ZIP checksum in [the source commit's CI run](https://github.com/Yuchi-Wang02/csm-copilot/actions/runs/38645412310), which passed 321 Python tests, 100 JavaScript tests and installed CLI/MCP checks on both runners.

The extracted package was opened over localhost HTTP. Harbor's queue disclosure showed its contact record and fixed review time; its readonly handoff preview included source comparisons and the snapshot boundary. Both language variants of the packaged Harbor brief contain the comparison table. The recordings and both PDFs are byte-identical to v0.29.5. Earlier workflow, reset, save/resume and PDF-download observations remain in [Verification](VERIFICATION.md); they were not all repeated for this packaging pass. No new model inference was performed. These checks establish specific behavior and file identity, not independent model reliability, customer impact or personal mastery.

The preceding handoff check observed successful-copy feedback, but the browser-control tool's separate virtual clipboard prevented independent payload read-back. The controlled session also did not expose a native leave-page prompt. These remain explicit verification limits; the preview supports manual copying and progress JSON is the reliable way to retain practice work.

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

The earlier [v0.20.1 ZIP](https://github.com/Yuchi-Wang02/csm-copilot/releases/tag/v0.20.1) was packaged manually, with demo files checked against its tagged source. The reproducible archive format does not reproduce that historical ZIP's bytes or replace its assets. The v0.21.0, v0.23.0, v0.25.0, v0.27.1, v0.28.0, v0.28.2, v0.29.1, v0.29.3, v0.29.4 and v0.29.5 releases remain separate fixed snapshots.

The static application has been browser-tested over HTTP. Direct file opening was not browser-verified because the automated browser policy disallows `file://` navigation. Local script and clipboard behavior can vary; use the included PDF or hosted demo if local-file restrictions prevent the interactive walkthrough. Practice notes are not part of the package and are not uploaded by the builder.
