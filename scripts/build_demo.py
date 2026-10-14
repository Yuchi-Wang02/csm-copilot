"""Rebuild the browser's exact replay data from the same Python workflow used by MCP."""

import json
import runpy
from pathlib import Path

from csm_copilot.demo import build_demo

ROOT = Path(__file__).resolve().parents[1]
report = runpy.run_path(str(ROOT / "evaluation/run.py"))["evaluate"]()
integrity = runpy.run_path(str(ROOT / "evaluation/integrity.py"))["write_report"]()
payload = {"workflow": build_demo(), "evaluation": report, "integrity": integrity}
(ROOT / "demo/data.js").write_text(
    "window.CSM_DATA = " + json.dumps(payload, ensure_ascii=False, indent=2) + ";\n",
    encoding="utf-8",
)
(ROOT / "evidence/workflow.json").write_text(
    json.dumps(payload["workflow"], ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print("Built demo/data.js and evidence/workflow.json from engine outputs.")
