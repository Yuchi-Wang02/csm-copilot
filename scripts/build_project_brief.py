"""Build a deterministic two-page portfolio PDF from the checked-in evidence."""

import hashlib
import json
from functools import partial
from pathlib import Path
from xml.sax.saxutils import escape

from pypdf import PdfReader
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "demo/project-brief.pdf"
SITE = "https://yuchi-wang02.github.io/csm-copilot/"
REPO = "https://github.com/Yuchi-Wang02/csm-copilot"
INK = colors.HexColor("#192c2b")
GREEN = colors.HexColor("#20564a")
SOFT = colors.HexColor("#eef2e9")
LINE = colors.HexColor("#dce2d9")
MUTED = colors.HexColor("#5f706b")
AMBER = colors.HexColor("#f4e8dc")
WIDTH = 516


def load(relative):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


STYLES = {
    "body": ParagraphStyle(
        "body", fontName="Helvetica", fontSize=10, leading=14, textColor=INK, spaceAfter=7
    ),
    "small": ParagraphStyle(
        "small", fontName="Helvetica", fontSize=8.1, leading=11, textColor=MUTED, spaceAfter=5
    ),
    "heading": ParagraphStyle(
        "heading",
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=GREEN,
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True,
    ),
    "title": ParagraphStyle(
        "title", fontName="Helvetica-Bold", fontSize=31, leading=35, textColor=INK, spaceAfter=10
    ),
    "subtitle": ParagraphStyle(
        "subtitle", fontName="Helvetica", fontSize=16, leading=21, textColor=GREEN, spaceAfter=13
    ),
    "eyebrow": ParagraphStyle(
        "eyebrow", fontName="Helvetica-Bold", fontSize=8, leading=11, textColor=GREEN, spaceAfter=10
    ),
    "cell": ParagraphStyle(
        "cell", fontName="Helvetica", fontSize=9, leading=12, textColor=INK, alignment=TA_LEFT
    ),
}


def para(text, style="body"):
    return Paragraph(text, STYLES[style])


def link(label, url):
    return f'<link href="{escape(url, {chr(34): "&quot;"})}" color="#20564a"><u>{escape(label)}</u></link>'


def box(contents, background=SOFT):
    table = Table([[contents]], colWidths=[WIDTH])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), background),
                ("LEFTPADDING", (0, 0), (-1, -1), 13),
                ("RIGHTPADDING", (0, 0), (-1, -1), 13),
                ("TOPPADDING", (0, 0), (-1, -1), 11),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    return table


def comparison(rows, widths):
    table = Table([[para(cell, "cell") for cell in row] for row in rows], colWidths=widths)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), SOFT),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LINEBELOW", (0, 0), (-1, -1), 0.5, LINE),
                ("LEFTPADDING", (0, 0), (-1, -1), 9),
                ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                ("TOPPADDING", (0, 0), (-1, -1), 9),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
            ]
        )
    )
    return table


def footer(canvas, doc, fingerprint):
    canvas.saveState()
    canvas.setStrokeColor(LINE)
    canvas.line(48, 42, 564, 42)
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(48, 29, f"Yuchi Wang | CSM Copilot | Evidence {fingerprint}")
    canvas.drawRightString(564, 29, f"{doc.page} / 2")
    canvas.restoreState()


def build():
    workflow = load("evidence/workflow.json")
    accounts = load("src/csm_copilot/data/accounts.json")
    transport = load("evidence/mcp-transcript.json")
    reviews = load("evidence/model-runs/review.json")
    batch = load("evidence/model-runs/qwen4-batch.json")
    constrained = load("evidence/model-runs/qwen4-constrained.json")
    diagnostic = load("evidence/evaluation.json")
    lantern = next(p for p in workflow["packets"] if p["selection"]["account_id"] == "acc_014")
    platforms = {i["readiness"]["platform"]: i for i in lantern["integrations"]}
    android = platforms["Android"]["readiness"]
    ios = platforms["iOS"]["readiness"]
    unknown = sum(c["status"] == "unknown" for c in android["checks"])
    failed = sum(c["status"] == "not_met" for c in android["checks"])
    ios_met = sum(c["status"] == "met" for c in ios["checks"])
    corrections = sum("correction_feedback" in s for s in constrained["steps"])
    # These editorial examples must be reconsidered if their underlying cases change.
    assert (unknown, failed, ios_met) == (3, 1, 6)
    assert "full compliance" in batch["final"]
    assert constrained["response_review"]["status"] == "structured_fields_match"
    assert constrained["response_review"]["free_text_verification"] == "not_performed"
    assert corrections == 2
    evidence = [workflow, accounts, transport, reviews, batch, constrained, diagnostic]
    fingerprint = hashlib.sha256(
        json.dumps(evidence, ensure_ascii=False, sort_keys=True).encode("utf-8")
    ).hexdigest()[:12]
    holdout = diagnostic["metrics"]["holdout"]

    story = [
        para("YUCHI WANG / CUSTOMER SUCCESS x APPLIED AI", "eyebrow"),
        para("CSM Copilot", "title"),
        para("Move onboarding forward.<br/>Keep the evidence intact.", "subtitle"),
        para(
            "Independent portfolio project. Not affiliated with Unity. All customer records are synthetic.",
            "small",
        ),
        box(
            [
                para(
                    f"<b>{len(accounts['accounts'])} synthetic accounts</b> &nbsp; / &nbsp; "
                    f"<b>{transport['tool_count']} MCP tools</b> &nbsp; / &nbsp; "
                    f"<b>{len(reviews['runs'])} recorded model attempts</b>"
                ),
                para(
                    "English and Chinese follow-ups | Public evidence snapshot: 14 October 2026",
                    "small",
                ),
            ]
        ),
        para("The customer problem", "heading"),
        para(
            "A publisher wants to launch on Friday. An iOS test passed, but a non-test Android "
            "device shows a blank Offerwall. The CSM needs a focused follow-up and a useful "
            "technical handoff without turning incomplete information into a promise."
        ),
        para("The working sequence", "heading"),
        box(
            [
                para(
                    "<b>Prioritize accounts &gt; inspect evidence &gt; draft &gt; prepare handoff &gt; review</b>"
                ),
                para(
                    "The MCP server supplies scoped findings and drafts. A model-enabled host can choose "
                    "tools. The website replays actual engine outputs and recorded model runs; it is not a live chat.",
                    "small",
                ),
            ]
        ),
        para("One account. Two different next actions.", "heading"),
        comparison(
            [
                ["<b>Integration</b>", "<b>Recorded evidence</b>", "<b>CSM next action</b>"],
                [
                    "Moon Garden<br/><b>Android</b>",
                    f"{unknown} unknown checks; {failed} failed device check. Separate settings evidence from a fresh test.",
                    "Request missing settings/callback evidence and a new non-test-device result. Keep launch unresolved.",
                ],
                [
                    "Moon Garden<br/><b>iOS</b>",
                    f"{ios_met} scoped checks met. The records belong to iOS, not Android.",
                    "Confirm changes and review the launch plan. Checklist completion is not launch approval.",
                ],
            ],
            [100, 196, 220],
        ),
        para(
            "Trace the Android failure to <b>lantern_android_device_verified</b>. "
            "Two new setting confirmations still do not replace that failed test.",
            "small",
        ),
        para("What a reviewer can inspect", "heading"),
        para(
            "Bilingual drafts, explicit missing handoff fields, platform-specific evidence, "
            "a Product feedback digest, and a practice exercise that preserves initial reasoning "
            "separately from reflection after guidance."
        ),
        box(
            [
                para("<b>Contribution and learning</b>", "small"),
                para(
                    "Yuchi selected the project direction and CSM workflow. Implementation, synthetic cases, "
                    "tests and documentation used substantial AI assistance. Personal mastery exercises and "
                    "independent human validation are not claimed as completed.",
                    "small",
                ),
            ]
        ),
        Spacer(1, 6),
        para(
            link("Open the interactive portfolio", SITE)
            + " &nbsp; | &nbsp; "
            + link("View code and evidence", REPO)
        ),
        PageBreak(),
        para("EXECUTION EVIDENCE / FAILURE / IMPROVEMENT", "eyebrow"),
        para("AI behavior you can inspect", "title"),
        para(
            "Correct tool use does not guarantee a faithful explanation. The project preserves "
            "the failed outputs as well as the changes made in response."
        ),
        comparison(
            [
                ["<b>Observed step</b>", "<b>What happened</b>", "<b>Design response</b>"],
                [
                    "1. Tool calls succeed",
                    f"Qwen3-4B executed {batch['coverage']['observed']}/{batch['coverage']['required']} requested calls, then described iOS as having 'full compliance' and omitted citations.",
                    "Separate tool coverage from answer fidelity. Preserve the raw output and compare claims with sources.",
                ],
                [
                    "2. Format is constrained",
                    "Parseable JSON still repeated platforms and included an issue-only source as readiness evidence.",
                    "Check scope, unknowns, failures and readiness IDs against actual tool results. Reject mismatches.",
                ],
                [
                    "3. Fields finally match",
                    f"After {corrections} recorded correction requests, the structured fields matched. The explanation still lacked inline source IDs and an explicit nothing-sent sentence.",
                    "Render a separate summary from checked tool fields. Keep free prose visibly unverified.",
                ],
            ],
            [105, 215, 196],
        ),
        Spacer(1, 12),
        box(
            [
                para("<b>Result: assisted recovery on one task, not a model accuracy score.</b>"),
                para(
                    "Prompts, response contracts and generation settings changed across attempts. Correction "
                    "feedback supplied expected values. Field agreement does not verify source truth or free prose. "
                    "The source comparison is AI-assisted, not independent human review.",
                    "small",
                ),
            ],
            AMBER,
        ),
        para("What the checks establish", "heading"),
        para(
            "Real MCP transport, repeatable workflow outputs and tested evidence boundaries. "
            f"The lexical triage diagnostic matched {holdout['correct']}/{holdout['total']} "
            "family-separated synthetic messages; the same development effort authored the cases. "
            "No production adoption, measured time savings or general reliability is claimed."
        ),
        para("How to demonstrate the learning", "heading"),
        para(
            "Explain one decision before opening the guidance. Trace it to a source. Identify what "
            "would change your conclusion. Then make and verify a small improvement you can explain yourself. "
            "The practice download keeps original reasoning and later reflection distinct; it does not grade them."
        ),
        para("Open the evidence", "heading"),
        KeepTogether(
            [
                para(
                    link(
                        "Android case",
                        SITE + "?case=lantern_android&view=evidence#workspace",
                    )
                    + " &nbsp; | &nbsp; "
                    + link(
                        "Chinese iOS follow-up",
                        SITE + "?case=lantern_ios&view=followup&lang=zh#workspace",
                    )
                    + " &nbsp; | &nbsp; "
                    + link("Practice", SITE + "#practice")
                ),
                para(
                    link(
                        "Six model recordings and review",
                        REPO + "/blob/main/evidence/MODEL_RUNS.md",
                    )
                    + " &nbsp; | &nbsp; "
                    + link("Verification record", REPO + "/blob/main/docs/VERIFICATION.md")
                ),
                para(
                    "Source basis: evidence/workflow.json; evidence/model-runs/qwen4-batch.json; "
                    "evidence/model-runs/qwen4-constrained.json; evidence/evaluation.json. Links open the current "
                    "public project. The evidence fingerprint in the footer identifies the source bundle used here.",
                    "small",
                ),
            ]
        ),
    ]
    document = SimpleDocTemplate(
        str(DEST),
        pagesize=letter,
        invariant=1,
        pageCompression=0,
        lang="en-US",
        rightMargin=48,
        leftMargin=48,
        topMargin=43,
        bottomMargin=55,
        title="CSM Copilot - Portfolio Brief",
        author="Yuchi Wang",
        subject="An AI-assisted customer-success workflow and inspectable model experiment",
    )
    document.build(
        story,
        onFirstPage=partial(footer, fingerprint=fingerprint),
        onLaterPages=partial(footer, fingerprint=fingerprint),
    )
    reader = PdfReader(DEST)
    assert len(reader.pages) == 2, f"Expected two pages, got {len(reader.pages)}"
    text = " ".join(" ".join(page.extract_text() for page in reader.pages).split())
    assert "lantern_android_device_verified" in text
    assert "substantial AI assistance" in text
    assert "assisted recovery on one task" in text
    links = [
        ref.get_object()["/A"]["/URI"]
        for page in reader.pages
        for ref in page.get("/Annots", [])
        if ref.get_object().get("/A", {}).get("/S") == "/URI"
    ]
    assert len(links) == 7, links
    assert all(url.startswith((SITE, REPO)) for url in links)
    print(f"Built {DEST.name}: 2 pages, {len(links)} clickable links, evidence {fingerprint}.")


if __name__ == "__main__":
    build()
