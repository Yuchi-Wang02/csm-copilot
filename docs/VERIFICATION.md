# Verification record

## Reviewed source snapshot

This summary describes the v0.30.0 release source, commit [`d899e26`](https://github.com/Yuchi-Wang02/csm-copilot/commit/d899e2625bb3aaf5cb9a8d8b3ee67a2794c338da), reviewed on **14 October 2026 (America/New_York)**. Both jobs in its [verification run](https://github.com/Yuchi-Wang02/csm-copilot/actions/runs/38669105626) passed: Windows / Python 3.13 and Ubuntu / Python 3.11. The [portable-package guide](INTERVIEW_BUNDLE.md) records its reproducible archive and observed browser behavior. The [earlier reviewed snapshot](https://github.com/Yuchi-Wang02/csm-copilot/blob/1320c312e655143b6114765b848ee41203cdf6f2/docs/VERIFICATION.md) remains available for comparison.

For newer commits, inspect the live [verification workflow](https://github.com/Yuchi-Wang02/csm-copilot/actions/workflows/ci.yml) and [deployment workflow](https://github.com/Yuchi-Wang02/csm-copilot/actions/workflows/pages.yml). The table below is tied to the reviewed source, rather than an automatically updated claim about `main`.

| Evidence | Verified observation | What it establishes |
|---|---|---|
| Python behavior checks | 514 passed in each CI job | The authored workflow, export, evidence-scope, host policy, request lifecycle, field review, recording integrity and packaging cases behaved as expected |
| JavaScript checks | 111 passed in each CI job | Practice, local progress files, routing, source rendering, triage replay, recorded conversations and copy-feedback logic passed their authored cases |
| Real MCP transport | Scripted stdio calls, eight tools, both prompts and invalid-ID behavior passed | The client and server exchanged the expected protocol results; this is separate from model orchestration |
| Installed package | Source distribution/wheel builds and isolated installed CLI/MCP checks passed on both runners | The checked package works outside the editable checkout in those environments |
| Generated artifacts | CI regenerated the demo, briefs, diagnostic reports, model replay and both PDFs without a Git diff | The committed outputs agree with the builders at this source revision |
| Portable PDFs | Project brief: two pages and seven links. Teaching handout: one page and four links. The committed PDFs match their previously rendered and visually inspected versions | Page counts, links and inspected layout; not audience comprehension or completed customer training |
| Synthetic triage diagnostic | 12/12 development cases; 16/18 reused family-separated cases after adaptation; earlier 14/18 preserved | Performance on inspected synthetic examples, not a fresh holdout or independent accuracy estimate |
| Model recordings | Seventeen preserved local attempts across four prescribed tasks | Observable tool choices, outputs, assistance and failures in those attempts; no new inference in the browser |
| Interview package | Local, downloaded Windows/Ubuntu CI archives and public release download are byte-identical | Reproducible static package from the pinned source, with each included file checked against that tree |

The counts are different kinds of evidence and should not be added into one reliability score. Passing tests does not establish source truth, production readiness, customer impact, general model reliability or Yuchi's personal mastery. The [evaluation report](../evidence/EVALUATION.md), [model-run review](../evidence/MODEL_RUNS.md) and [limitations](LIMITATIONS.md) describe those boundaries.

## Browser interactions inspected

Browser checks are recorded observations, not a cross-browser automated acceptance suite. This package pass opened the extracted v0.30.0 archive over localhost HTTP in Edge. It confirmed the version banner, seventeen recording choices, the latest final-turn rejection and omitted-message audit, Android's evidence request, iOS's launch-plan review and the handoff's missing SDK version, time window and redacted logs. No browser errors were recorded during those interactions. The public ZIP and checksum downloads match the checked local files.

Earlier checks covered keyboard focus, direct links, browser history, practice save/resume, reset confirmation, downloads, readable evidence sources and selected mobile layouts. They were performed at their recorded versions; they were not all repeated for this source snapshot. Screen-reader behavior and other browser engines remain unverified. Read the [version-specific history](VERIFICATION_HISTORY.md) and [development notes](DEVELOPMENT.md) for what was observed and what was not.

QA notes, generated examples and passing checks are not personal learning responses. The project keeps those separate from the user's own explanations and reflections.

## Reproduction

From a checkout of the source revision you intend to inspect, use Python 3.11-3.13, Node.js and Git. CI uses Node.js 24. Dependency installation requires package-index access. The sequence below includes all seven JavaScript suites and the current generated-artifact checks; execute it in order and stop if a command fails.

```sh
python -m pip install -e ".[dev,brief]"
node --test tests-js/practice.test.cjs tests-js/practice-session.test.cjs tests-js/review-links.test.cjs tests-js/case-review.test.cjs tests-js/triage-review.test.cjs tests-js/model-turns.test.cjs tests-js/copy-feedback.test.cjs
python -m ruff check .
python -m ruff format --check .
python -m pytest -q
python scripts/mcp_smoke.py --output evidence/mcp-transcript.json
python scripts/build_demo.py
python -m pytest tests/test_review_brief.py -k generated_morning_briefs -q
python evaluation/triage_boundaries.py
python evaluation/negation.py
python scripts/build_model_replay.py
python scripts/build_project_brief.py
python scripts/build_client_education.py
git diff --exit-code -- demo/project-brief.pdf demo/publisher-teaching-example.pdf demo/data.js demo/model-runs.js demo/morning-review-en.md demo/morning-review-zh.md demo/case-briefs demo/product-feedback.md evidence
python -m build
python scripts/verify_wheel.py
python scripts/build_interview_demo.py --output dist/interview-demo.zip
```

Builders overwrite their named generated artifacts. The final bundle command reads committed Git files and excludes worktree edits; commit intended source changes before packaging them. See the [bundle guide](INTERVIEW_BUNDLE.md) for fixed-release checksums and rebuild details. This sequence reproduces executable checks; it does not repeat historical browser observations or run a model.

On the development Windows machine, Application Control previously blocked local installed launchers. That restriction was not bypassed. Installed-command verification is supported by the clean Windows and Ubuntu CI runs, rather than a claim of successful local launcher execution. Do not treat a blocked local launcher as permission to change system policy.

## Installed package check

`scripts/verify_wheel.py` defaults to the wheel matching the version in `pyproject.toml`; an explicit wheel path can also be supplied. It creates a fresh virtual environment without shared site packages, clears `PYTHONPATH` and `PYTHONHOME`, and runs from a temporary directory outside the checkout. The imported module must reside in that new environment, and its package and module versions must agree.

The installed `csm-demo` command must reproduce the published workflow and review exports. A standalone MCP client launches the installed `csm-copilot` command, exercises all eight tools and both prompts, and compares its transcript with the published result. Temporary environments and exports are removed when the check exits. This check needs package-index access; it is not an offline installation claim.

A historical negative probe removed `accounts.json` from a disposable wheel. Installation succeeded, but the workflow command failed and the verifier rejected the wheel. That probe shows that an editable source tree could not mask that particular missing packaged file. It does not establish that all packaging failures or installation environments are covered. The [history](VERIFICATION_HISTORY.md#installed-package-check) retains the original observation and later checks.
