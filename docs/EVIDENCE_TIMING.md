# Read the date as well as the source

The case explorer and exported review briefs show a timing view for records that support the selected platform's checklist. Dates are already present in the source records; this view makes them easier to compare without changing their meaning.

Each entry identifies the source, its type, recorded timestamp, elapsed days at the fixed snapshot, and the checks it supports. Sources appear oldest first. One record supporting two settings appears once with both check IDs. Account contact records and issue-only messages are excluded unless they actually support a checklist check.

## Demonstrate the difference

Open [the Android customer-update comparison](https://yuchi-wang02.github.io/csm-copilot/?case=lantern_android&view=evidence&lang=en&update=1#customer-update). The new settings confirmation is recorded at the snapshot (0.00 days old). The earlier failed non-test-device record remains unchanged. This makes the next action concrete: ask for a new device result rather than treating the new settings message as proof of a passed test.

The original case view and its downloadable brief keep the original snapshot. The timing view in the comparison uses only the separate synthetic-update branch. Resetting the comparison removes that new source; it does not alter stored records or contact history.

## Interpretation boundary

Age is elapsed time between the source timestamp and the fixed snapshot, rounded to two decimal days. The browser's current clock is not used. Timezone offsets are included in the calculation, and exact timestamps remain visible.

There is no invented vendor expiry threshold, automatic stale flag or newest-record-wins rule. An older record can still support a historical observation; a newer message does not necessarily retest it. The CSM must decide whether the customer needs to reconfirm a setting or provide a fresh test. Source age does not establish source truth or current product behavior.

Missing or mis-scoped referenced records appear as unavailable, with no invented date. Future and timezone-naive timestamps are rejected by the timing helper, as they are by the dataset boundary. Timing does not modify readiness, resolve conflicting claims, approve launch or send anything.

## Reproduction

`python scripts/build_demo.py` builds the browser timing data and both language versions of the Markdown briefs from the same scoped records. The eight MCP tools retain their existing responses; `get_account_context` already returns the underlying timestamps. No new model inference is needed for this descriptive view.

The Python checks cover timezone arithmetic, non-mutation, old records without automatic expiry, missing/mis-scoped sources, invalid dates, shared-source deduplication and the settings-versus-device comparison. Browser-logic checks cover rendering, scope filtering, unavailable sources and text escaping. These are software checks, not a freshness policy or independent evidence validation.
