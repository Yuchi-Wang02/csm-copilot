# Verification record

Verified through the v0.8 shareable reviews and portable PDF brief on 2026-10-14. For the latest commit, use the live [CI results](https://github.com/Yuchi-Wang02/csm-copilot/actions/workflows/ci.yml) and [Pages deployment](https://github.com/Yuchi-Wang02/csm-copilot/actions/workflows/pages.yml).

| Check | Observed result | Scope |
|---|---|---|
| JavaScript browser-logic tests | 10 passed locally | Five practice checks plus five routing checks; not learning outcomes |
| Portfolio PDF | Two pages, seven public links; repeated builds match | Built from checked-in evidence; both rendered pages visually reviewed |
| Python behavior tests | 109 passed locally | Workflow, source scope, next-action selection, readable exports and UTF-8 output |
| Evidence-integrity replay | 8/8 expected acceptance states | Developer-authored probes; no semantic truth verification |
| Ruff lint and format | Passed | Python source checks |
| Package build | Source distribution and wheel built | Includes packaged JSON fixtures |
| Real MCP stdio client | Eight tools, three follow-up intents, both prompts and invalid-ID error passed | Scripted client, no model inference |
| Local model attempts | Six recordings retained; latest structured fields match after two corrections | One task, changed configurations and feedback supplying expected values; free prose remains unverified |
| Portable morning review | English and Chinese-draft Markdown generated and checked for consistency | Same workflow packet as the browser; draft-only |
| Product feedback digest | Ten targeted tests cover counts, applicability, deduplication, empty cohorts, sources, ordering and export | Fixed synthetic snapshot; no measured Product outcome |
| Synthetic diagnostics | 12/12 dev; 14/18 family-separated cases | Same-session authored, not independently validated |
| Initial GitHub Actions verification | Windows / Python 3.13 and Ubuntu / Python 3.11 passed | Clean runner installation and regenerated-artifact consistency |
| GitHub Pages deployment | Published successfully | Public static replay |

## Browser interactions inspected

- Android evidence remains blocked; switching to iOS displays its own complete scoped checklist.
- English and Chinese follow-ups render from the generated engine outputs.
- Harbor's handoff retains HTTP 405 as a hypothesis and exposes missing reproduction steps and logs.
- The customer-update toggle confirms two settings while retaining the failed device check.
- Arrow-key navigation moves between review tabs.
- The copy button reports completion; operating-system clipboard contents were not independently validated.
- At a mobile viewport, document width and scroll width both measured 375 CSS pixels: no horizontal page overflow.
- Browser error logs were empty in the inspected local session.
- The v0.2 evidence selector displays rejected cross-platform and identity-overwrite probes, and accepts an explicitly unknown state with contradictory reports. Its mobile layout also measured 375 CSS pixels for both document and scroll width, without horizontal overflow.
- The v0.3 iOS follow-up requests a launch-plan review in both languages; Android requests its missing evidence. The English brief was downloaded through the browser and its SHA-256 matched the generated file. The download row had no horizontal overflow at the inspected mobile viewport, and the local browser error log was empty.
- The v0.4 feedback selector shows device checks at two affected / five applicable integrations, callbacks at two / three, and approval at one account with no cross-account recurrence claim. Expanding source panels distinguishes a recorded failure from no applicable record. The feedback download matched the generated file's SHA-256. At the inspected mobile viewport, document and scroll widths were both 375 CSS pixels; the selector worked and no browser errors were recorded.

Screenshots: [desktop introduction](assets/demo-desktop.png), [case review](assets/demo-case.png), [Chinese follow-up](assets/demo-followup.png), [mobile evidence view](assets/demo-mobile.png), [v0.2 evidence-boundary replay](assets/demo-integrity.png), [v0.3 follow-up and brief export](assets/demo-review-brief.png), [v0.4 Product feedback](assets/demo-product-feedback.png).

The v0.5 browser check exercised all three recorded-attempt selections, opened rejected raw output, and confirmed that the four-call run remains labeled as needing revision. Mobile document and scroll widths were both 375 CSS pixels, the selector worked, and no browser errors were recorded. [Model trace screenshot](assets/demo-model-trace.png).

The v0.6 browser check opened the system-rendered summary, selected the correction-budget failure, and inspected raw feedback. At the inspected mobile viewport, document and scroll widths both measured 360 CSS pixels, including expanded raw output. No browser errors were recorded. [Structured-response screenshot](assets/demo-response-review.png).

The v0.7 browser check exercised all three decisions, both matching and differing options, preserved notes on return, reset, and a downloaded reflection. The actual downloaded file retained the original choice and note separately from later reflection. Revealing guidance focused the feedback panel. Mobile document and scroll widths both measured 360 CSS pixels, including the longer AI case; no browser errors were recorded. [Practice screenshot](assets/demo-practice.png). Test notes were created only for verification and do not represent Yuchi's work.

The v0.8 browser check opened a Chinese iOS follow-up and Harbor handoff directly, verified the exact public URL in the clipboard, restored the previous view with Back, and confirmed invalid-setting fallback notices. Practice evidence links retained a test note while opening the appropriate iOS follow-up or Android comparison. The original Android panel stayed unchanged when the comparison toggle was active. The complete iOS empty-handoff view now proposes launch-plan review. Mobile document and scroll widths both measured 360 CSS pixels with the share-link controls expanded, and no browser errors were recorded. [Review-link screenshot](assets/demo-review-link.png).

The portable brief was rendered and visually reviewed on both pages. Its seven link annotations were extracted and checked, repeated builds produced identical bytes, and the browser-downloaded PDF matched the reviewed file's SHA-256. The new download link fit the inspected mobile layout (360 CSS pixels for both document and scroll width), with no browser errors. Rebuild instructions and metadata conventions are in [the brief guide](PROJECT_BRIEF.md).

## Reproduction

```sh
python -m pip install -e ".[dev,brief]"
python -m pytest -q
node --test tests-js/practice.test.cjs tests-js/review-links.test.cjs
python -m ruff check .
python -m ruff format --check .
python scripts/mcp_smoke.py --output evidence/mcp-transcript.json
python scripts/build_demo.py
python scripts/build_model_replay.py
python scripts/build_project_brief.py
git diff --exit-code -- demo/project-brief.pdf demo/data.js demo/model-runs.js demo/morning-review-en.md demo/morning-review-zh.md demo/product-feedback.md evidence
python -m build
```

Generated outputs are deterministic. The diagnostic case hash uses UTF-8 text with normalized line endings, so Windows and Linux yield the same identifier. Browser screenshots are observational artifacts and are not regenerated by CI.
