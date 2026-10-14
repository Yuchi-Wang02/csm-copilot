"""Build a one-page teaching handout from the existing guide and checked case data."""

import hashlib
import json
import re
from pathlib import Path
from xml.sax.saxutils import escape

from pypdf import PdfReader
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "demo/publisher-teaching-example.pdf"
REPO = "https://github.com/Yuchi-Wang02/csm-copilot"
SITE = "https://yuchi-wang02.github.io/csm-copilot/"
FAQ = "https://docs.unity.com/en-us/grow/offerwall/monetization/other/faq"
INK = colors.HexColor("#192c2b")
GREEN = colors.HexColor("#20564a")
MUTED = colors.HexColor("#5f706b")
LINE = colors.HexColor("#dce2d9")
SOFT = colors.HexColor("#eef2e9")


def build():
    guide = (ROOT / "docs/CLIENT_EDUCATION.md").read_text(encoding="utf-8")
    data = json.loads((ROOT / "src/csm_copilot/data/accounts.json").read_text(encoding="utf-8"))
    integrations = {i["id"]: i for i in data["integrations"]}
    # This editorial scenario must be reviewed if its facts change.
    assert {k: v["status"] for k, v in integrations["lantern_android"]["facts"].items()} == {
        "currency_approved": "unknown",
        "test_only_off": "unknown",
        "placement_linked": "met",
        "sdk_connected": "met",
        "device_verified": "not_met",
        "callback_verified": "unknown",
    }
    assert {
        k: v["status"] for k, v in integrations["lantern_ios"]["facts"].items()
    } == dict.fromkeys(integrations["lantern_android"]["facts"], "met")
    assert data["as_of"] == "2026-10-14T09:00:00+00:00"

    question = next(
        line for line in guide.splitlines() if line.startswith("**Customer question:**")
    )
    question = question.removeprefix("**Customer question:** ")
    explanation = guide.split("## Explain the product checks\n\n", 1)[1].split("\n\n", 1)[0]
    explanation = re.sub(r" \[Official Offerwall FAQ\]\([^\n]+\)\.", "", explanation)
    assert "[" not in explanation, "Review changed source markup before generating the handout"
    rows = [
        [cell.strip().replace("`", "") for cell in line.strip("|").split("|")]
        for line in guide.splitlines()
        if line.startswith("| ")
    ]
    assert len(rows) == 6 and all(len(row) == 2 for row in rows)
    requests = [line.removeprefix("> ") for line in guide.splitlines() if line.startswith("> ")]
    assert len(requests) == 1, "Review changed sample-message structure"
    fingerprint = hashlib.sha256(
        json.dumps({"guide": guide, "data": data}, ensure_ascii=False, sort_keys=True).encode(
            "utf-8"
        )
    ).hexdigest()[:12]

    styles = {
        "body": ParagraphStyle(
            "body", fontName="Helvetica", fontSize=9.3, leading=12.5, textColor=INK, spaceAfter=6
        ),
        "small": ParagraphStyle(
            "small", fontName="Helvetica", fontSize=7.6, leading=10, textColor=MUTED, spaceAfter=5
        ),
        "title": ParagraphStyle(
            "title", fontName="Helvetica-Bold", fontSize=25, leading=29, textColor=INK, spaceAfter=9
        ),
        "heading": ParagraphStyle(
            "heading",
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=14,
            textColor=GREEN,
            spaceBefore=10,
            spaceAfter=5,
            keepWithNext=True,
        ),
        "cell": ParagraphStyle(
            "cell", fontName="Helvetica", fontSize=8.6, leading=11.5, textColor=INK
        ),
    }

    def p(text, style="body"):
        return Paragraph(escape(text), styles[style])

    def link(label, url):
        return f'<link href="{escape(url, {chr(34): "&quot;"})}" color="#20564a"><u>{escape(label)}</u></link>'

    table = Table([[p(cell, "cell") for cell in row] for row in rows], colWidths=[222, 294])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), SOFT),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LINEBELOW", (0, 0), (-1, -1), 0.5, LINE),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    story = [
        p("CSM COPILOT / CUSTOMER EDUCATION", "small"),
        p("Explain a blank Offerwall", "title"),
        p(question),
        p(
            "Independent, AI-assisted teaching example. Lantern Games is fictional. "
            "Not affiliated with Unity; not a record of customer training delivered by Yuchi.",
            "small",
        ),
        p("1. Explain why the checks are separate", "heading"),
        p(explanation),
        p("2. Use the account's actual recorded state", "heading"),
        p(
            "Synthetic snapshot: 14 October 2026, 09:00 UTC. These are recorded facts, not a live status check.",
            "small",
        ),
        table,
        p("3. Give the publisher a focused next step", "heading"),
        p(requests[0]),
        p(
            "Project policy: requiring a non-test-device record and separate callback verification "
            "are this prototype's checklist choices, not asserted Unity go-live requirements. "
            "A passing retest alone does not close the issue or approve launch.",
            "small",
        ),
        p(
            "Practice: explain this in your own words, then in Chinese. Which new observation "
            "would change your next action? Keep your first answer and later revision separately.",
            "body",
        ),
        Spacer(1, 4),
        Paragraph(
            " | ".join(
                [
                    link("Official product FAQ", FAQ),
                    link(
                        "Synthetic source records",
                        REPO + "/blob/main/src/csm_copilot/data/accounts.json",
                    ),
                    link("Full teaching guide", REPO + "/blob/main/docs/CLIENT_EDUCATION.md"),
                    link(
                        "Inspect the Android case",
                        SITE + "?case=lantern_android&view=evidence&lang=en#workspace",
                    ),
                ]
            ),
            styles["small"],
        ),
        p(
            "Documentation reviewed 14 October 2026. Links require internet access and may change; "
            "recheck the official guidance before adapting the example to a real account.",
            "small",
        ),
    ]

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(LINE)
        canvas.line(48, 39, 564, 39)
        canvas.setFillColor(MUTED)
        canvas.setFont("Helvetica", 7)
        canvas.drawString(48, 27, f"Yuchi Wang | CSM Copilot | Source fingerprint {fingerprint}")
        canvas.drawRightString(564, 27, "Teaching example / 1")
        canvas.restoreState()

    document = SimpleDocTemplate(
        str(DEST),
        pagesize=letter,
        invariant=1,
        pageCompression=0,
        lang="en-US",
        leftMargin=48,
        rightMargin=48,
        topMargin=35,
        bottomMargin=52,
        title="CSM Copilot - Publisher Teaching Example",
        author="Yuchi Wang",
        subject="An AI-assisted teaching example with synthetic customer evidence",
    )
    document.build(story, onFirstPage=footer, onLaterPages=footer)
    reader = PdfReader(DEST)
    assert len(reader.pages) == 1, f"Expected one page, got {len(reader.pages)}"
    text = reader.pages[0].extract_text()
    assert "not a record of customer training" in text
    assert "We cannot confirm the cause or a launch date" in text
    urls = [ref.get_object()["/A"]["/URI"] for ref in reader.pages[0].get("/Annots", [])]
    assert len(urls) == 4 and FAQ in urls
    print(f"Built {DEST.name}: 1 page, 4 clickable links, source fingerprint {fingerprint}.")


if __name__ == "__main__":
    build()
