# Explain a blank Offerwall to a new publisher

An AI-assisted teaching example for the fictional Lantern Games case. All account details are synthetic. This is a proposed customer conversation, not a record of training delivered by Yuchi or an official Unity support procedure.

[Download the one-page teaching handout (PDF)](../demo/publisher-teaching-example.pdf) for a portable version of the explanation, case table and proposed next step. The PDF includes source links and a practice prompt; it can be read without opening GitHub.

**Customer question:** “It worked on iOS. Why is Android still blank, and what should we do next?”

## Explain the product checks

Review Android separately. Virtual currency approval is platform-specific. A registered test device can receive a test advertisement even when regional inventory is unavailable, so test-device success does not establish availability for other users. Test Only settings can also restrict who sees content. [Official Offerwall FAQ](https://docs.unity.com/en-us/grow/offerwall/monetization/other/faq).

For a blank Offerwall, also check that the placement is linked to content, its name matches between code and dashboard, and the SDK has reported a successful connection before requesting content. These are troubleshooting checks, not a diagnosis of this customer's cause. [Official Offerwall FAQ](https://docs.unity.com/en-us/grow/offerwall/monetization/other/faq).

## Apply that explanation to Lantern

Open [the Android evidence panel](https://yuchi-wang02.github.io/csm-copilot/?case=lantern_android&view=evidence&lang=en#workspace). The table below describes the fixed synthetic snapshot of October 14, 2026; it is not a live status update.

| What the record says | What to explain to the publisher |
|---|---|
| iOS has a complete scoped checklist. | That result belongs to iOS. We still need Android-specific evidence. |
| Android currency approval and Test Only status are unknown. | We are missing confirmation. We have not established that either setting is wrong. |
| Android's device check is recorded as `not_met`. | There is a recorded failed check. A new test result is needed to reassess it. |
| Android placement and SDK connection checks are recorded as met. | Retain those records in the handoff; avoid asking the customer to supply everything again. |
| Android callback verification is unknown. | Reward delivery remains a separate open checklist item; it does not establish why this screen is blank. |

These case statements come from the [synthetic account records](../src/csm_copilot/data/accounts.json), including `lantern_android` and `lantern_ios`. Expand **Trace checklist decisions to source records** in the demo to inspect the dated device observation and compare it with the unknown checks that have no supporting citation.

## Propose a focused next step

> Let's confirm the Android currency approval and Test Only settings first. Our record also shows a failed Android device check. Please share a fresh result from a non-test device, including the app/platform, region, test time and what appeared on screen. We can then compare that result with the existing placement and connection records and decide what needs technical review. We cannot confirm the cause or a launch date from the current information.

This wording illustrates the project's intake policy. Requiring a non-test-device record and a separate callback verification record are **project checklist choices**, not asserted Unity go-live requirements. See the [source and policy boundaries](SOURCES.md#official-documentation-versus-operating-choices).

If the new result is still blank, preserve it and prepare a handoff with the known context and remaining gaps. Ask for relevant redacted logs and reproduction steps when needed; do not fill missing fields with guesses. If the screen works, reassess the other open checks and ask whether the reported issue is resolved. One successful retest does not automatically close the case or approve launch. The [three-stage update example](https://yuchi-wang02.github.io/csm-copilot/?case=lantern_android&view=evidence&lang=en&update=2#customer-update) shows that project workflow.

## Practice the explanation yourself

Before adapting the sample, record your own answer to the customer's question. Then check:

- Can you explain why iOS and Android need separate evidence without using internal status names?
- Which sentence describes a known failure, and which asks about something unknown?
- What new observation would change your proposed next action?
- Can you give the same explanation in Chinese while preserving those distinctions?

Keep the first explanation and your later revision separately using the [learning reflection template](LEARNING.md#short-reflection-template). The example demonstrates the intended communication approach; your own explanation and revision provide evidence of learning.

Public documentation reviewed October 14, 2026. Product settings and documentation can change; recheck the linked guidance before adapting this example to a real account.
