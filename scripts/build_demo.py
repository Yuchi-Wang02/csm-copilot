"""Rebuild the browser's exact replay data from the same Python workflow used by MCP."""

import json
import runpy
from pathlib import Path

from csm_copilot.brief import render_review_brief
from csm_copilot.demo import build_demo
from csm_copilot.engine import Copilot
from csm_copilot.friction import render_friction_brief
from csm_copilot.summary import render_summary

ROOT = Path(__file__).resolve().parents[1]
report = runpy.run_path(str(ROOT / "evaluation/run.py"))["evaluate"]()
integrity = runpy.run_path(str(ROOT / "evaluation/integrity.py"))["write_report"]()
friction = Copilot().friction_digest()
callback_denial = runpy.run_path(str(ROOT / "evaluation/callback_denial.py"))["evaluate"]()
payload = {
    "workflow": build_demo(),
    "evaluation": report,
    "integrity": integrity,
    "friction": friction,
    "callback_denial": callback_denial,
}
(ROOT / "demo/data.js").write_text(
    "window.CSM_DATA = " + json.dumps(payload, ensure_ascii=False, indent=2) + ";\n",
    encoding="utf-8",
)
(ROOT / "evidence/workflow.json").write_text(
    json.dumps(payload["workflow"], ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print("Built demo/data.js and evidence/workflow.json from engine outputs.")
(ROOT / "evidence/morning-summary.txt").write_text(
    render_summary(payload["workflow"]), encoding="utf-8", newline="\n"
)
for language in ("en", "zh"):
    brief = render_review_brief(payload["workflow"], language)
    for directory in ("demo", "evidence"):
        (ROOT / directory / f"morning-review-{language}.md").write_text(brief, encoding="utf-8")
print("Built English and Chinese review briefs from the same workflow packet.")
case_directory = ROOT / "demo/case-briefs"
case_directory.mkdir(exist_ok=True)
for packet in payload["workflow"]["packets"]:
    for item in packet["integrations"]:
        integration_id = item["readiness"]["integration_id"]
        for language in ("en", "zh"):
            (case_directory / f"{integration_id}-{language}.md").write_text(
                render_review_brief(payload["workflow"], language, integration_id),
                encoding="utf-8",
                newline="\n",
            )
print("Built separate English and Chinese briefs for each queued platform.")
(ROOT / "evidence/friction.json").write_text(
    json.dumps(friction, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
for directory in ("demo", "evidence"):
    (ROOT / directory / "product-feedback.md").write_text(
        render_friction_brief(friction), encoding="utf-8"
    )
print("Built the source-linked Product feedback review.")
