"""Bilingual wording for explicit follow-up intents; no inferred promises or deadlines."""

NEXT_ACTIONS = {
    "en": {
        "evidence_request": "Review and send the evidence request, then reassess when new records arrive.",
        "issue_status_review": "Confirm the recorded issue's current status before planning further action.",
        "launch_plan_review": "Review the launch plan and confirm any changes since the recorded checks.",
        "post_launch_checkin": "Check the live experience and ask about new issues or changed configuration.",
    },
    "zh": {
        "evidence_request": "复核并发送证据请求，收到新记录后重新评估。",
        "issue_status_review": "先确认已记录问题的当前状态，再讨论下一步。",
        "launch_plan_review": "复核上线计划，并确认上次检查后是否有变更。",
        "post_launch_checkin": "跟进线上体验，确认是否出现新问题或配置变更。",
    },
}


def compose_followup(*, name, app, platform, stage, intent, requests, lang):
    """Use a checklist result and known account stage to choose the customer's next question."""
    recorded_failure = (
        "Our records show this check was not met. "
        if lang == "en"
        else "现有记录显示该项检查未满足要求。"
    )
    request_lines = [
        f"- {recorded_failure if r['status'] == 'not_met' else ''}{r['request']}" for r in requests
    ]
    if lang == "en":
        lines = [f"Hi {name} team,"]
        if intent == "evidence_request":
            lines += [
                f"Following up on {app} ({platform}). Our current records still need the following evidence:"
            ]
            lines += request_lines
            lines += [
                "I can consolidate your updates for technical review. Please let us know when you expect to share them."
            ]
        else:
            lines += [
                f"Our scoped checklist for {app} ({platform}) is complete based on the recorded evidence."
            ]
            if intent == "issue_status_review":
                lines += [
                    "A previous issue is still recorded. Please confirm whether it still occurs and share any new observations; checklist completion does not establish that the issue is resolved."
                ]
            elif intent == "post_launch_checkin":
                lines += [
                    "How is the live experience? Please let us know about any new issues or configuration changes since the recorded checks so we can agree on the next review step."
                ]
            else:
                lines += [
                    "Please confirm whether anything has changed since those checks and whether the proposed launch plan is still current. We can then review the remaining launch decisions together."
                ]
        lines += [
            "This check-in does not confirm issue resolution or guarantee ad availability."
            if stage == "live"
            else "Launch timing remains subject to verification; this message does not confirm approval or ad availability."
        ]
    else:
        lines = [f"{name} 团队好，"]
        if intent == "evidence_request":
            lines += [f"跟进 {app}（{platform}）的接入进展，目前记录还需要以下证据："]
            lines += request_lines
            lines += ["收到后我可以汇总信息交给技术同事复核，请告知预计何时可以提供。"]
        else:
            lines += [f"根据现有记录，{app}（{platform}）已完成本项目范围内的检查清单。"]
            if intent == "issue_status_review":
                lines += [
                    "记录中仍有此前报告的问题。请确认目前是否仍然出现，并分享新的观察；清单完成并不代表该问题已解决。"
                ]
            elif intent == "post_launch_checkin":
                lines += [
                    "想了解目前的线上体验。请告知上次检查后是否出现新问题或配置变更，我们可以据此确认下一次复核的重点。"
                ]
            else:
                lines += [
                    "请确认上次检查后是否有变更，以及拟定的上线计划是否仍适用。之后我们可以一起复核其余上线决策。"
                ]
        lines += [
            "本次跟进不代表问题已解决，也不承诺广告供应。"
            if stage == "live"
            else "上线时间仍需核验；本消息不代表审核通过或广告供应承诺。"
        ]
    return {"body": "\n".join(lines), "next_action": NEXT_ACTIONS[lang][intent]}
