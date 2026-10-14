# Build a portable interview demo

The [v0.23.0 prerelease](https://github.com/Yuchi-Wang02/csm-copilot/releases/tag/v0.23.0) provides the five-decision demo, text/action-boundary probes, preserved callback failure and current repair, and two-page PDF brief. It is pinned to commit `34d436cbba31efcd892c60f599026c35f7aca070`.

The hosted portfolio and current source have advanced to v0.24 with focused handoff intake requests. That addition is not included in the fixed v0.23.0 download below. Use the hosted version to inspect the latest workflow, or rebuild a bundle from the desired committed revision.

## Choose the right take-away

| Item | Use it for |
|---|---|
| [Hosted portfolio](https://yuchi-wang02.github.io/csm-copilot/) | Open the interactive review with no setup; it may advance after this release |
| `csm-copilot-demo-v0.23.0.zip` under release Assets | Keep a fixed copy of the static demo, PDF, review briefs and recorded results |
| GitHub's Source code archives | Inspect the full repository, Python implementation, tests and documentation at the tag |

Extract the entire demo ZIP, read `START_HERE.txt`, and begin with `project-brief.pdf` or the three-minute route in `index.html`. Local browser restrictions may affect the interactive files; the application was browser-tested over HTTP, and direct file opening remains unverified. The hosted portfolio provides the browser-tested route. Write your own practice reasoning and download it before closing or reloading the page; the package does not include personal notes.

## Verify the fixed package

The published ZIP is **788,331 bytes**. Its SHA-256 is:

```text
ed06c791ebeb9e0dab5cef5582bb5415ff215c462dcfd2455801c18f57a8a3df
```

In PowerShell, from the folder containing the download:

```powershell
Get-FileHash -LiteralPath .\csm-copilot-demo-v0.23.0.zip -Algorithm SHA256
```

The release also provides a `.zip.sha256` file. All 22 demo files were checked byte-for-byte against the pinned Git tree, the guide matched its manifest hash, and ZIP integrity passed. The local, Windows and Ubuntu builds produced the same inner ZIP checksum in [the source commit's CI run](https://github.com/Yuchi-Wang02/csm-copilot/actions/runs/38605503423). This is file-identity evidence, not independent validation of the underlying customer scenarios.

## Rebuild from source

From a checkout containing the builder, run with Python 3.11 or newer and Git:

```sh
python scripts/build_interview_demo.py --output dist/interview-demo.zip
```

The command prints the selected commit, project version, archive size and SHA-256. It reads the committed `demo/` tree directly. Uncommitted changes and untracked notes are excluded, even when they are inside `demo/`. Commit an intended demo change before packaging it. `--ref <commit-or-tag>` selects another locally available revision; the current builder is still used.

To reproduce an archive byte-for-byte, use the same builder revision and selected source commit. The `csm-interview-bundle-v1` format uses sorted entries, fixed ZIP timestamps and permissions, and uncompressed bytes to avoid compression-library differences. File hashes and source identity are recorded in `SHA256SUMS.json`. These establish file identity, not authenticity, safety or correctness of the synthetic evidence.

The package contains the committed demo files plus two generated additions: `START_HERE.txt` and `SHA256SUMS.json`. The builder rejects committed symlinks, collisions with those reserved names, and missing local HTML script/link targets. It does not crawl external documentation or analyze every dynamically constructed URL. The application's existing behavior checks remain separate.

Both Windows and Ubuntu CI build a bundle from the checked-out commit and upload it as `interview-demo-<runner>-<attempt>`. Compare the inner `interview-demo.zip` hashes to check agreement across environments; the surrounding GitHub artifact archives are separate transport containers. Build success alone does not establish matching bytes between runners.

Six focused checks cover identical output despite dirty worktree edits and CRLF settings, original Git bytes and manifest hashes, missing local assets, pinned older commits, committed symlinks, reserved filenames, and query/fragment/external-link handling.

The earlier [v0.20.1 ZIP](https://github.com/Yuchi-Wang02/csm-copilot/releases/tag/v0.20.1) was packaged manually, with demo files checked against its tagged source. The reproducible archive format does not reproduce that historical ZIP's bytes or replace its assets. The v0.21.0 and v0.23.0 releases remain separate fixed snapshots.

The static application has been browser-tested over HTTP. Direct file opening was not browser-verified because the automated browser policy disallows `file://` navigation. Local script and clipboard behavior can vary; use the included PDF or hosted demo if local-file restrictions prevent the interactive walkthrough. Practice notes are not part of the package and are not uploaded by the builder.
