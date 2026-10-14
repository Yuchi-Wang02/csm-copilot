const { test } = require("node:test");
const assert = require("node:assert/strict");
const api = require("../demo/case-review.js");

test("copyable Harbor handoff retains supplied facts, focused requests and review boundaries", () => {
  const workflow = structuredClone(require("../evidence/workflow.json"));
  const data = workflow.packets.find((p) => p.context.account.id === "acc_006");
  const before = JSON.stringify(data);
  const record = api.issuesFor(data, "harbor_android")[0];
  const text = api.handoffText(record, workflow.as_of);
  assert.match(text, /Snapshot: 2026-10-14T09:00:00\+00:00/);
  assert.match(text, /Issue: issue_callback · Draft: ticket-issue_callback/);
  assert.match(text, /Missing intake fields: reproduction_steps, redacted_logs/);
  assert.match(text, /Share the steps to reproduce/);
  assert.match(text, /credentials, tokens, personal data and other secrets removed/);
  assert.match(text, /HTTP 405 makes an endpoint method mismatch worth checking; it is not a confirmed cause/);
  assert.match(text, /Source reference: integration_record \/ harbor_android/);
  assert.match(text, /Source reference: issue_evidence \/ msg_issue_callback/);
  assert.match(text, /Root cause: unconfirmed/);
  assert.match(text, /No ticket was submitted and contact history is unchanged/);
  assert.doesNotMatch(text, /lantern_android|meadow_ios|Share the SDK version|Share the observation start/);
  for (const value of Object.values(record.ticket.fields)) assert.ok(text.includes(String(value)));
  assert.equal(JSON.stringify(data), before);
});

test("each copy stays with its own issue and unavailable sources are not reconstructed", () => {
  const data = packet();
  const records = api.issuesFor(data, "android");
  const first = api.handoffText(records[0], "snapshot"), second = api.handoffText(records[1], "snapshot");
  assert.match(first, /Original 1/);
  assert.doesNotMatch(first, /Original 2|Original 3|ticket-second|ticket-other/);
  assert.match(second, /Original 2/);
  assert.doesNotMatch(second, /Original 1|Original 3|ticket-first|ticket-other/);
  data.context.evidence[0].integration_id = "ios";
  const unavailable = api.handoffText(api.issuesFor(data, "android")[0], "snapshot");
  assert.match(unavailable, /One scoped source was not available/);
  assert.doesNotMatch(unavailable, /Original 1/);
  assert.equal(api.handoffText({...records[0], ticket: null}, "snapshot"), null);
});

test("scope-first copied handoff does not turn populated or missing fields into technical intake", () => {
  for (const missing of [[], ["redacted_logs"]]) {
    const data = packet(), t = data.tickets[0];
    t.handoff_state = "needs_scope";
    t.missing_fields = missing;
    t.collection_requests = [{field:"redacted_logs",request:"TECHNICAL REQUEST MUST NOT APPEAR"}];
    t.triage.candidates = [{category:"unknown",questions:["Which account does the invoice concern?"],source_url:null}];
    const text = api.handoffText(api.issuesFor(data, "android")[0], "snapshot");
    assert.match(text, /Clarify the request first/);
    assert.match(text, /Which account does the invoice concern/);
    assert.doesNotMatch(text, /Missing intake fields|TECHNICAL REQUEST MUST NOT APPEAR/);
  }
});

test("ambiguous drafts cannot be copied by choosing whichever occurs first", () => {
  for (const reverse of [false, true]) {
    const data = packet();
    data.tickets.push({...structuredClone(data.tickets[0]), title:"CONFLICTING DRAFT"});
    if (reverse) data.tickets.reverse();
    const records = api.issuesFor(data, "android");
    assert.equal(records[0].ticket, null);
    assert.equal(api.handoffText(records[0], "snapshot"), null);
    const html = api.handoffHTML(records, "unused", "snapshot");
    assert.match(html, /missing or duplicate drafts require review/);
    assert.doesNotMatch(html, /CONFLICTING DRAFT|Copy handoff · first/);
    assert.match(html, /Copy handoff · second/);
  }
});

test("handoff preview keeps literal customer text inside a readonly, separately labeled field", () => {
  const data = packet();
  data.context.evidence[0].text = 'Line one\n</textarea><img src=x onerror="run()">';
  const records = api.issuesFor(data, "android");
  const text = api.handoffText(records[0], "snapshot");
  assert.match(text, /  \| Line one\n  \| <\/textarea><img/);
  const html = api.handoffHTML(records, "unused", "snapshot");
  assert.match(html, /data-handoff-copy="0"/);
  assert.match(html, /data-handoff-copy="1"/);
  assert.match(html, /id="handoff-text-0" rows="12" readonly/);
  assert.match(html, /Handoff text for first/);
  assert.match(html, /Handoff text for second/);
  assert.match(html, /&lt;\/textarea&gt;&lt;img/);
  assert.doesNotMatch(html, /<img/);
  assert.equal((html.match(/<textarea /g) || []).length, 2);
  assert.equal((html.match(/<\/textarea>/g) || []).length, 2);
});

function readinessFixture() {
  const workflow = require("../evidence/workflow.json");
  return structuredClone(workflow.packets[0]);
}

test("ambiguous check citations do not select a record by array order", () => {
  for (const sameText of [false, true]) {
    for (const reverse of [false, true]) {
      const data = readinessFixture(), item = data.integrations[0];
      const source = data.context.evidence.find((r) => r.id === "lantern_android_device_verified");
      source.text = "FIRST AMBIGUOUS DEVICE RECORD";
      const duplicate = structuredClone(source);
      if (!sameText) {
        duplicate.text = "SECOND AMBIGUOUS DEVICE RECORD";
        duplicate.claims.device_verified = "met";
      }
      data.context.evidence.push(duplicate);
      if (reverse) data.context.evidence.reverse();
      const before = JSON.stringify(data);
      for (const html of [
        api.readinessSourcesHTML(item.readiness, data.context),
        api.followupSourcesHTML(item.followup_en, item.readiness, data.context),
        api.followupSourcesHTML(item.followup_zh, item.readiness, data.context),
      ]) {
        assert.match(html, /Multiple matching records make this citation ambiguous/);
        assert.doesNotMatch(html, /FIRST AMBIGUOUS DEVICE RECORD|SECOND AMBIGUOUS DEVICE RECORD/);
        assert.match(html, /Non-test device verification · not met/);
        assert.match(html, /Requested evidence:/);
      }
      assert.equal(JSON.stringify(data), before);
    }
  }
});

test("ambiguous original messages stay unavailable in both issue views", () => {
  for (const reverse of [false, true]) {
    const data = readinessFixture();
    const source = data.context.evidence.find((r) => r.id === "msg_issue_blank");
    source.text = "FIRST AMBIGUOUS CUSTOMER MESSAGE";
    data.context.evidence.push({...structuredClone(source), text: "SECOND AMBIGUOUS CUSTOMER MESSAGE"});
    if (reverse) data.context.evidence.reverse();
    const before = JSON.stringify(data);
    const records = api.issuesFor(data, "lantern_android");
    const evidence = api.evidenceHTML(records), handoff = api.handoffHTML(records);
    assert.match(evidence, /missing or duplicate records require review/);
    assert.match(handoff, /missing or duplicate records require review/);
    assert.doesNotMatch(evidence + handoff, /FIRST AMBIGUOUS CUSTOMER MESSAGE|SECOND AMBIGUOUS CUSTOMER MESSAGE/);
    assert.match(handoff, /Scoped field source unavailable: msg_issue_blank/);
    assert.equal(JSON.stringify(data), before);
  }
});

test("one correctly scoped record remains usable beside an unrelated same-ID record", () => {
  const data = readinessFixture(), item = data.integrations[0];
  for (const id of ["lantern_android_device_verified", "msg_issue_blank"]) {
    const source = data.context.evidence.find((r) => r.id === id);
    data.context.evidence.unshift({...structuredClone(source), account_id: "another_account", text: "UNRELATED DUPLICATE ID"});
  }
  const html = api.readinessSourcesHTML(item.readiness, data.context) +
    api.followupSourcesHTML(item.followup_en, item.readiness, data.context) +
    api.evidenceHTML(api.issuesFor(data, "lantern_android"));
  assert.match(html, /Synthetic Android test record/);
  assert.match(html, /Read original customer message/);
  assert.doesNotMatch(html, /UNRELATED DUPLICATE ID|citation ambiguous/);
});

test("follow-up requests expose only their check sources in the selected language", () => {
  const data = readinessFixture(), item = data.integrations[0];
  const before = JSON.stringify(data);
  for (const lang of ["en", "zh"]) {
    const html = api.followupSourcesHTML(item[`followup_${lang}`], item.readiness, data.context);
    assert.match(html, /Why this draft asks for evidence/);
    assert.match(html, /Non-test device verification · not met/);
    assert.match(html, /2026-10-09T09:00:00Z/);
    assert.match(html, /Recorded claim for this check:<\/strong> not met/);
    assert.match(html, /Platform currency approval · unknown/);
    assert.match(html, /No supporting record is cited/);
    assert.match(html, /does not verify source truth or every sentence/);
    assert.ok(html.includes(item[`followup_${lang}`].requests.find((r) => r.check_id === "device_verified").request));
    assert.doesNotMatch(html, /Placement and content|SDK connection sequence|lantern_ios|msg_issue_blank/);
  }
  assert.equal(JSON.stringify(data), before);
  const complete = data.integrations[1];
  assert.equal(api.followupSourcesHTML(complete.followup_en, complete.readiness, data.context), "");
});

test("follow-up source display refuses unmatched or differing request states", () => {
  for (const change of [
    (r, checks) => { r.check_id = "not_a_check"; },
    (r, checks) => { r.status = "met"; },
    (r, checks) => { checks.push(structuredClone(checks.find((c) => c.id === r.check_id))); },
  ]) {
    const data = readinessFixture(), item = data.integrations[0];
    const request = item.followup_en.requests.find((r) => r.check_id === "device_verified");
    item.followup_en.requests = [request];
    change(request, item.readiness.checks);
    const html = api.followupSourcesHTML(item.followup_en, item.readiness, data.context);
    assert.match(html, /Request needs review/);
    assert.match(html, /No unique matching open checklist state/);
    assert.doesNotMatch(html, /Synthetic Android test record|Recorded claim for this check/);
  }
});

test("follow-up source display keeps missing citations and wrong-scope records visible", () => {
  const data = readinessFixture(), item = data.integrations[0];
  item.followup_en.evidence_ids = [];
  const source = data.context.evidence.find((r) => r.id === "lantern_android_device_verified");
  source.account_id = "unrelated";
  source.text = "DO NOT ATTRIBUTE THIS RECORD";
  const html = api.followupSourcesHTML(item.followup_en, item.readiness, data.context);
  assert.match(html, /Checklist sources missing from draft citations: lantern_android_device_verified/);
  assert.match(html, /Scoped source unavailable: lantern_android_device_verified/);
  assert.doesNotMatch(html, /DO NOT ATTRIBUTE THIS RECORD/);
});

test("follow-up request text stays inert and does not alter the source records", () => {
  const data = readinessFixture(), item = data.integrations[0];
  item.followup_en.requests[0].request = '<script>rewrite()</script>';
  const before = JSON.stringify(data);
  const html = api.followupSourcesHTML(item.followup_en, item.readiness, data.context);
  assert.match(html, /&lt;script&gt;rewrite\(\)&lt;\/script&gt;/);
  assert.doesNotMatch(html, /<script>/);
  assert.equal(JSON.stringify(data), before);
});

test("handoff provenance separates integration values from dated issue details", () => {
  const data = structuredClone(require("../evidence/workflow.json").packets.find((p) => p.context.account.id === "acc_006"));
  const before = JSON.stringify(data);
  const html = api.handoffHTML(api.issuesFor(data, "harbor_android"));
  const sources = html.split('class="handoff-sources"')[1];
  assert.match(sources, /app · Integration record/);
  assert.match(sources, /Recorded value:<\/strong> Pocket Harbor/);
  assert.match(sources, /No per-field observation date is recorded/);
  assert.match(sources, /sdk version · Issue evidence/);
  assert.match(sources, /Recorded value:<\/strong> synthetic-version-1/);
  assert.match(sources, /Customer report · msg_issue_callback · 2026-10-10T09:00:00Z/);
  assert.match(sources, /not automatic extraction/);
  assert.match(sources, /Inspect raw field-source map/);
  assert.doesNotMatch(sources, /handoff-field"><summary>redacted logs/);
  assert.equal(JSON.stringify(data), before);
});

test("handoff provenance rejects missing, cross-scope and misattributed sources", () => {
  for (const change of [
    (p) => { p.context.evidence.find((r) => r.id === "msg_issue_blank").account_id = "other"; },
    (p) => { p.context.evidence.find((r) => r.id === "msg_issue_blank").integration_id = "lantern_ios"; },
    (p) => { p.context.evidence = p.context.evidence.filter((r) => r.id !== "msg_issue_blank"); },
    (p) => { p.tickets[0].field_sources.region.source_id = "another_issue"; },
    (p) => { p.context.integrations.find((i) => i.id === "lantern_android").account_id = "other"; },
    (p) => { p.context.issues[0].details.region = null; },
  ]) {
    const p = readinessFixture();
    change(p);
    const sources = api.handoffHTML(api.issuesFor(p, "lantern_android")).split('class="handoff-sources"')[1];
    const region = sources.split('<summary>region · Issue evidence</summary>')[1].split('</details>')[0];
    assert.match(region, /Scoped field source unavailable/);
    assert.doesNotMatch(region, /Recorded value:/);
  }
});

test("handoff provenance exposes differing values and escapes copied source content", () => {
  const p = readinessFixture();
  p.tickets[0].fields.region = '<img src=x onerror="run()">';
  p.context.issues[0].details.region = '<script>source()</script>';
  const before = JSON.stringify(p);
  const sources = api.handoffHTML(api.issuesFor(p, "lantern_android")).split('class="handoff-sources"')[1];
  assert.match(sources, /Handoff value:<\/strong> &lt;img/);
  assert.match(sources, /Recorded value:<\/strong> &lt;script&gt;/);
  assert.match(sources, /handoff value differs from the recorded value/);
  assert.doesNotMatch(sources, /<img|<script/);
  assert.equal(JSON.stringify(p), before);
});

test("original issue text is not borrowed from another account", () => {
  const p = readinessFixture();
  const source = p.context.evidence.find((r) => r.id === "msg_issue_blank");
  source.account_id = "another_account";
  source.text = "DO NOT ATTRIBUTE THIS MESSAGE";
  const records = api.issuesFor(p, "lantern_android");
  const html = api.evidenceHTML(records) + api.handoffHTML(records);
  assert.match(html, /Source record unavailable/);
  assert.doesNotMatch(html, /DO NOT ATTRIBUTE THIS MESSAGE/);
});

test("readable readiness records retain check claims, full dates and platform scope", () => {
  const data = readinessFixture();
  const readiness = data.integrations[0].readiness;
  const original = JSON.stringify(data);
  const html = api.readinessSourcesHTML(readiness, data.context);
  assert.match(html, /Non-test device verification · not met/);
  assert.match(html, /Synthetic Android test record: Non-test device verification = not_met\./);
  assert.match(html, /2026-10-09T09:00:00Z/);
  assert.match(html, /Recorded claim for this check:<\/strong> not met/);
  assert.match(html, /Requested evidence:<\/strong> Share a fresh non-test-device check/);
  assert.match(html, /No supporting record is cited/);
  assert.doesNotMatch(html, /lantern_ios|contact_acc_014|msg_issue_blank/);
  assert.equal(JSON.stringify(data), original);
});

test("missing, wrong-account and wrong-platform readiness sources are not substituted", () => {
  for (const change of [
    (r) => { r.account_id = "other"; },
    (r) => { r.integration_id = "lantern_ios"; },
    (r) => { r.id = "different"; },
  ]) {
    const data = readinessFixture();
    const source = data.context.evidence.find((r) => r.id === "lantern_android_device_verified");
    source.text = "THIS SOURCE MUST NOT APPEAR";
    change(source);
    const html = api.readinessSourcesHTML(data.integrations[0].readiness, data.context);
    assert.match(html, /Scoped source unavailable: lantern_android_device_verified/);
    assert.doesNotMatch(html, /THIS SOURCE MUST NOT APPEAR/);
  }
});

test("readable sources expose missing and conflicting claims without rewriting decisions", () => {
  const data = readinessFixture();
  const source = data.context.evidence.find((r) => r.id === "lantern_android_device_verified");
  source.claims = {};
  let html = api.readinessSourcesHTML(data.integrations[0].readiness, data.context);
  assert.match(html, /No structured claim recorded/);
  source.claims.device_verified = "met";
  html = api.readinessSourcesHTML(data.integrations[0].readiness, data.context);
  assert.match(html, /recorded claim differs from the displayed state/);
  assert.match(html, /Non-test device verification · not met/);
});

test("readable readiness text is inert and not-applicable checks do not imply a passed test", () => {
  const data = readinessFixture();
  const r = data.integrations[0].readiness;
  data.context.evidence.find((e) => e.id === "lantern_android_device_verified").text = '<img src=x onerror="run()">';
  r.checks[0].status = "not_applicable";
  r.checks[1].request = "<script>run()</script>";
  const html = api.readinessSourcesHTML(r, data.context);
  assert.match(html, /&lt;img src=x/);
  assert.match(html, /&lt;script&gt;/);
  assert.match(html, /absent citation does not establish a passed test/);
  assert.doesNotMatch(html, /<img|<script/);
});

test("focused requests precede optional broader questions and escape all text", () => {
  const data = packet();
  const ticket = data.tickets[0];
  ticket.collection_requests = [{field: "redacted_logs", request: "Share logs <script>run()</script>"}];
  ticket.collection_boundary = "Recorded <values> are not verified.";
  ticket.triage.candidates = [{category: "reward_callback", questions: ["Share the time window."], source_url: null}];
  const original = JSON.stringify(data);
  const html = api.handoffHTML(api.issuesFor(data, "android").slice(0, 1));
  assert.match(html, /Request missing intake details/);
  assert.match(html, /Share logs &lt;script&gt;/);
  assert.match(html, /Recorded &lt;values&gt; are not verified/);
  assert.doesNotMatch(html, /<script>/);
  assert.match(html, /<details class="handoff-questions"><summary>/);
  assert.ok(html.indexOf("Request missing intake details") < html.indexOf("Share the time window."));
  assert.equal(JSON.stringify(data), original);
});

test("scope questions stay expanded without an empty technical request section", () => {
  const data = packet();
  const ticket = data.tickets[0];
  ticket.handoff_state = "needs_scope";
  ticket.collection_requests = [];
  ticket.triage.candidates = [{category: "unknown", questions: ["What outcome do you need?"], source_url: null}];
  const html = api.handoffHTML(api.issuesFor(data, "android").slice(0, 1));
  assert.match(html, /<details class="handoff-questions" open>/);
  assert.match(html, /What outcome do you need/);
  assert.doesNotMatch(html, /Request missing intake details/);
});

test("issue displays preserve whether the original source is a customer report or a test", () => {
  const data = packet();
  for (const [kind, label, disclosure] of [
    ["customer_report", "Customer report", "Read original customer message"],
    ["test_record", "Test record", "Read original test record"],
  ]) {
    data.context.evidence[0].kind = kind;
    const records = api.issuesFor(data, "android").slice(0, 1);
    const evidence = api.evidenceHTML(records), handoff = api.handoffHTML(records, "unused");
    assert.ok(evidence.includes(`${disclosure} · first`));
    assert.ok(evidence.includes(`${label} · source1`));
    assert.ok(handoff.includes(`${label} · 2026-10-14`));
    if (kind === "test_record") assert.doesNotMatch(evidence + handoff, /CUSTOMER REPORT|Read original customer message/);
  }
});

test("missing source type is not silently labeled a customer report", () => {
  const records = api.issuesFor(packet(), "android").slice(0, 1);
  const html = api.evidenceHTML(records) + api.handoffHTML(records, "unused");
  assert.match(html, /Source type unavailable/);
  assert.doesNotMatch(html, /CUSTOMER REPORT|Read original customer message/);
});

test("handoff questions are readable per candidate, with the scoped original record", () => {
  const data = packet();
  data.tickets[0].triage.candidates = [
    {category: "reward_callback", questions: ["Which currency mode?", "Share redacted logs."], source_url: "https://docs.unity.com/example"},
    {category: "no_offers", questions: ["Compare the devices."], source_url: null},
  ];
  const original = JSON.stringify(data);
  const html = api.handoffHTML(api.issuesFor(data, "android").slice(0, 1), "unused");
  assert.match(html, /<h4>Candidate: reward callback<\/h4>/);
  assert.match(html, /<li>Which currency mode\?<\/li>/);
  assert.match(html, /<li>Compare the devices\.<\/li>/);
  assert.match(html, /href="https:\/\/docs.unity.com\/example"/);
  assert.match(html, /Original issue record · source1/);
  assert.match(html, /Original 1/);
  assert.doesNotMatch(html, /Original 2|Original 3/);
  assert.match(html, /do not establish a root cause/);
  assert.equal(JSON.stringify(data), original);
});

test("unknown-scope questions do not invent technical candidates or documentation", () => {
  const data = packet();
  data.tickets[0].triage.candidates = [{category: "unknown", questions: ["What outcome do you need?"], source_url: null}];
  const html = api.handoffHTML(api.issuesFor(data, "android").slice(0, 1), "unused");
  assert.match(html, /<h4>Clarify the request<\/h4>/);
  assert.match(html, /<li>What outcome do you need\?<\/li>/);
  assert.doesNotMatch(html, /Candidate: unknown|Related documentation/);
});

test("handoff questions escape source text and do not activate non-HTTPS URLs", () => {
  const data = packet();
  data.context.evidence[0].integration_id = "ios";
  data.tickets[0].triage.candidates = [{category: "<img>", questions: ['<script>run()</script>'], source_url: 'javascript:run()'}];
  const html = api.handoffHTML(api.issuesFor(data, "android").slice(0, 1), "unused");
  assert.match(html, /&lt;img&gt;/);
  assert.match(html, /<li>&lt;script&gt;/);
  assert.match(html, /Original issue record unavailable for this platform/);
  assert.doesNotMatch(html, /<script>|<img>|href="javascript:|Original 1/);
});

test("timing view shows supplied dates and preserves one shared source across checks", () => {
  const timing = {
    as_of: "2026-10-14T09:00:00Z", unavailable_ids: [], boundary: "No expiry policy.",
    records: [
      {id:"device-old", kind:"test_record", recorded_at:"2026-10-09T09:00:00Z", age_days:5, check_ids:["device_verified"]},
      {id:"settings-new", kind:"customer_report", recorded_at:"2026-10-14T09:00:00Z", age_days:0, check_ids:["currency_approved","test_only_off"]},
      {id:"sdk-other", kind:"test_record", recorded_at:"2026-10-08T09:00:00Z", age_days:6, check_ids:["sdk_connected"]},
    ],
  };
  const original = JSON.stringify(timing);
  const html = api.timingHTML(timing,["device_verified","currency_approved","test_only_off"],true);
  assert.match(html,/2 supporting records/);
  assert.match(html,/5.00 days before snapshot/);
  assert.match(html,/0.00 days before snapshot/);
  assert.match(html,/currency_approved, test_only_off/);
  assert.match(html,/<time datetime="2026-10-09T09:00:00Z">/);
  assert.ok(!html.includes("sdk-other"));
  assert.equal(html.match(/<strong>settings-new<\/strong>/g).length,1);
  assert.equal(JSON.stringify(timing),original);
});
test("empty timing does not invent an age and unavailable source text is escaped", () => {
  const html = api.timingHTML({as_of:"2026-10-14T09:00:00Z",records:[],unavailable_ids:['<img src=x onerror=alert(1)>'],boundary:"Age does not expire evidence."});
  assert.match(html,/No available supporting records/);
  assert.match(html,/Unavailable scoped sources: &lt;img/);
  assert.ok(!html.includes("<img"));
  assert.ok(!html.includes("days before snapshot"));
});

function packet() {
  return {
    context: {
      account: { id: "account" },
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
        account_id: "account",
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
