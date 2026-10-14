const { test } = require("node:test");
const assert = require("node:assert/strict");
const api = require("../demo/case-review.js");

function packet() {
  return {
    context: {
      issues: [
        {
          id: "first",
          integration_id: "android",
          evidence_id: "source1",
          summary: "First issue",
        },
        {
          id: "second",
          integration_id: "android",
          evidence_id: "source2",
          summary: "Second issue",
        },
        {
          id: "other",
          integration_id: "ios",
          evidence_id: "source3",
          summary: "iOS issue",
        },
      ],
      evidence: [1, 2, 3].map((n) => ({
        id: `source${n}`,
        integration_id: n === 3 ? "ios" : "android",
        text: `Original ${n}`,
        at: "2026-10-14T09:00:00Z",
      })),
    },
    tickets: ["first", "second", "other"].map((id) => ({
      draft_id: `ticket-${id}`,
      title: `Ticket ${id}`,
      handoff_state: "needs_information",
      root_cause: "unconfirmed",
      fields: { platform: id === "other" ? "iOS" : "Android" },
      evidence_ids: [id],
      suggested_owner: "CSM",
      missing_fields: ["redacted_logs"],
      next_action: "Collect evidence",
      triage: { notes: [] },
      field_sources: {},
    })),
  };
}

test("both issues stay paired with their own source and ticket, excluding another platform", () => {
  const records = api.issuesFor(packet(), "android");
  assert.deepEqual(
    records.map((r) => [r.issue.id, r.evidence.id, r.ticket.draft_id]),
    [
      ["first", "source1", "ticket-first"],
      ["second", "source2", "ticket-second"],
    ],
  );
  const evidence = api.evidenceHTML(records),
    handoffs = api.handoffHTML(records, "unused");
  assert.match(evidence, /Original 1/);
  assert.match(evidence, /Original 2/);
  assert.match(handoffs, /Ticket first/);
  assert.match(handoffs, /Ticket second/);
  assert.doesNotMatch(evidence + handoffs, /Original 3|Ticket other/);
});

test("a missing draft is not described as an absent issue", () => {
  const data = packet();
  data.tickets.splice(1, 1);
  const html = api.handoffHTML(api.issuesFor(data, "android"), "unused");
  assert.match(html, /Handoff draft unavailable for second/);
  assert.match(html, /Ticket first/);
  assert.doesNotMatch(html, /No recorded issue to escalate/);
});

test("missing or mis-scoped sources do not erase the issue or borrow another platform's message", () => {
  const data = packet();
  data.context.evidence[1].integration_id = "ios";
  const html = api.evidenceHTML(api.issuesFor(data, "android"));
  assert.match(html, /Second issue/);
  assert.match(html, /Source record unavailable for second/);
  assert.doesNotMatch(html, /Original 2/);
  assert.match(api.evidenceHTML([]), /No issue message recorded/);
  assert.match(api.handoffHTML([], "Review launch plan"), /Review launch plan/);
});

test("customer content is escaped in issue summaries, sources and handoff fields", () => {
  const data = packet();
  data.context.issues[0].summary = '<img src=x onerror="run()">';
  data.context.evidence[0].text = "<script>run()</script>";
  data.tickets[0].fields.platform = '<iframe src="x">';
  const records = api.issuesFor(data, "android");
  const html = api.evidenceHTML(records) + api.handoffHTML(records, "unused");
  assert.doesNotMatch(html, /<img|<script|<iframe/);
  assert.match(html, /&lt;img/);
  assert.match(html, /&lt;script/);
  assert.match(html, /&lt;iframe/);
});

test("unrecognized scope takes precedence over generic field completeness in each draft", () => {
  const data = packet();
  data.tickets[1].handoff_state = "needs_scope";
  for (const missing of [[], ["sdk_version"]]) {
    data.tickets[1].missing_fields = missing;
    const html = api.handoffHTML(
      api.issuesFor(data, "android").slice(1),
      "unused",
    );
    assert.match(html, /Clarify the request first/);
    assert.match(html, /request, desired outcome and relevant account or product/);
    assert.doesNotMatch(html, /Confirm what happened and what was expected/);
    assert.doesNotMatch(
      html,
      /Ready for handoff review|Request before technical review/,
    );
  }
});
