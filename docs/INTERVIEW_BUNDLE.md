# Build a portable interview demo

The [v0.21.0 prerelease](https://github.com/Yuchi-Wang02/csm-copilot/releases/tag/v0.21.0) provides the five-decision demo and PDF brief using the repository builder below. The earlier [v0.20.1 ZIP](https://github.com/Yuchi-Wang02/csm-copilot/releases/tag/v0.20.1) was packaged manually, with demo files checked against its tagged source. The reproducible archive format does not reproduce that historical ZIP's bytes or replace its assets.

From a checkout containing the builder, run with Python 3.11 or newer and Git:

```sh
python scripts/build_interview_demo.py --output dist/interview-demo.zip
```

The command prints the selected commit, project version, archive size and SHA-256. It reads the committed `demo/` tree directly. Uncommitted changes and untracked notes are excluded, even when they are inside `demo/`. Commit an intended demo change before packaging it. `--ref <commit-or-tag>` selects another locally available revision; the current builder is still used.

To reproduce an archive byte-for-byte, use the same builder revision and selected source commit. The `csm-interview-bundle-v1` format uses sorted entries, fixed ZIP timestamps and permissions, and uncompressed bytes to avoid compression-library differences. File hashes and source identity are recorded in `SHA256SUMS.json`. These establish file identity, not authenticity, safety or correctness of the synthetic evidence.

The package contains the committed demo files plus two generated additions: `START_HERE.txt` and `SHA256SUMS.json`. The builder rejects committed symlinks, collisions with those reserved names, and missing local HTML script/link targets. It does not crawl external documentation or analyze every dynamically constructed URL. The application's existing behavior checks remain separate.

Both Windows and Ubuntu CI build a bundle from the checked-out commit and upload it as `interview-demo-<runner>-<attempt>`. Compare the inner `interview-demo.zip` hashes to check agreement across environments; the surrounding GitHub artifact archives are separate transport containers. Build success alone does not establish matching bytes between runners.

Six focused checks cover identical output despite dirty worktree edits and CRLF settings, original Git bytes and manifest hashes, missing local assets, pinned older commits, committed symlinks, reserved filenames, and query/fragment/external-link handling.

The static application has been browser-tested over HTTP. Direct file opening was not browser-verified because the automated browser policy disallows `file://` navigation. Local script and clipboard behavior can vary; use the included PDF or hosted demo if local-file restrictions prevent the interactive walkthrough. Practice notes are not part of the package and are not uploaded by the builder.
