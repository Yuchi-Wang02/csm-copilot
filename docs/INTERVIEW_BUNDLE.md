# Build a portable interview demo

The [v0.29.1 prerelease](https://github.com/Yuchi-Wang02/csm-copilot/releases/tag/v0.29.1) includes failure-aware English/Chinese follow-up wording, readable request sources, ambiguous-source handling, and links to a publisher teaching example. It retains focused handoff intake, local practice save/resume, five practice decisions, recorded AI attempts and the two-page PDF brief. It is pinned to commit `d85d816ed55a8eb413338bc37891d1fb3075ce38`.

This package also includes readable handoff-field provenance, checklist source records, recorded model conversations presented turn by turn, preserved keyboard focus, and selection-scoped clipboard feedback. Since v0.28.0, the portable review briefs include an integration-record index, full-queue exports use explicit LF line endings, and Reset asks before clearing practice work. The hosted site may advance later; this package remains pinned to its source commit.

The extracted v0.29.1 package was checked over localhost HTTP. The Android draft showed the recorded-failure sentence, and its source disclosure displayed the dated scoped record and requested retest. The downloaded Android English brief matched the packaged file byte-for-byte and contained the updated wording. No browser errors were recorded during those checks. The source commit passed 300 Python and 81 JavaScript tests. The reset confirmation's earlier browser verification remains recorded under v0.28.2 in [Verification](VERIFICATION.md); it was not repeated for this package.

The full learning guide, interview script and publisher teaching example are part of the repository/source archive. The demo ZIP links to external documents but does not include them as separate files. For stable references, read the [learning guide](https://github.com/Yuchi-Wang02/csm-copilot/blob/d85d816ed55a8eb413338bc37891d1fb3075ce38/docs/LEARNING.md), [interview script](https://github.com/Yuchi-Wang02/csm-copilot/blob/d85d816ed55a8eb413338bc37891d1fb3075ce38/docs/INTERVIEW.md) and [teaching example](https://github.com/Yuchi-Wang02/csm-copilot/blob/d85d816ed55a8eb413338bc37891d1fb3075ce38/docs/CLIENT_EDUCATION.md) at the release source. External links inside the application may point to the evolving repository or hosted site and require internet access. Use these pinned references when discussing the exact release.

## Choose the right take-away

| Item | Use it for |
|---|---|
| [Hosted portfolio](https://yuchi-wang02.github.io/csm-copilot/) | Open the interactive review with no setup; it may advance after this release |
| `csm-copilot-demo-v0.29.1.zip` under release Assets | Keep a fixed copy of the static demo, PDF, review briefs and recorded results |
| GitHub's Source code archives | Inspect the full repository, Python implementation, tests and documentation at the tag |

Extract the entire demo ZIP, read `START_HERE.txt`, and begin with `project-brief.pdf` or the three-minute route in `index.html`. Local browser restrictions may affect the interactive files; the application was browser-tested over HTTP, and direct file opening remains unverified. The hosted portfolio provides the browser-tested route. Write your own practice reasoning and save it before closing or reloading the page; the package does not include personal notes. Download Markdown for reading and a progress JSON file for resuming. Choosing a JSON file previews it locally; explicit confirmation is required before it replaces the current in-page work. See [practice-file compatibility and limits](PRACTICE.md#resume-without-rewriting-the-learning-record).

## Verify the fixed package

The published ZIP is **829,772 bytes**. Its SHA-256 is:

```text
3fd71634eb0ede44445720e9e943eacf78793e2270049c1a95ccfac0551dc065
```

In PowerShell, from the folder containing the download:

```powershell
Get-FileHash -LiteralPath .\csm-copilot-demo-v0.29.1.zip -Algorithm SHA256
```

The release also provides a `.zip.sha256` file. All 25 demo files were checked byte-for-byte against the pinned Git tree, the guide matched its manifest hash, and ZIP integrity passed. The local, Windows and Ubuntu builds produced the same inner ZIP checksum in [the source commit's CI run](https://github.com/Yuchi-Wang02/csm-copilot/actions/runs/38628285090). This is file-identity evidence, not independent validation of the underlying customer scenarios.

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

The earlier [v0.20.1 ZIP](https://github.com/Yuchi-Wang02/csm-copilot/releases/tag/v0.20.1) was packaged manually, with demo files checked against its tagged source. The reproducible archive format does not reproduce that historical ZIP's bytes or replace its assets. The v0.21.0, v0.23.0, v0.25.0, v0.27.1, v0.28.0 and v0.28.2 releases remain separate fixed snapshots.

The static application has been browser-tested over HTTP. Direct file opening was not browser-verified because the automated browser policy disallows `file://` navigation. Local script and clipboard behavior can vary; use the included PDF or hosted demo if local-file restrictions prevent the interactive walkthrough. Practice notes are not part of the package and are not uploaded by the builder.
