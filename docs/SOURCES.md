# Source register

Source review date: **2026-10-14**. Rules are concise paraphrases, not copied documentation. Product documentation may change; the pinned rule version is `2026-10-14.1`.

| Source | Used for | Scope |
|---|---|---|
| [Offerwall FAQ](https://docs.unity.com/en-us/grow/offerwall/monetization/other/faq) | Currency approval per platform; content/placement alignment; connection sequencing; test-device visibility; no-offers candidate checks | Offerwall publisher integration only |
| [Troubleshoot callback failures](https://docs.unity.com/en-us/grow/offerwall/monetization/virtual-currency/troubleshoot-callback-failures) | Reward callback questions and HTTP 405 method-mismatch hypothesis | Diagnostic checks, not proof of root cause |
| [Official MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) | Server/client protocol implementation | Installed SDK 1.30.0 |
| [MCP architecture](https://modelcontextprotocol.io/docs/learn/architecture) | Host/server separation | Protocol architecture |
| [Claude Code MCP setup](https://code.claude.com/docs/en/mcp) | Optional stdio client configuration | Host-specific setup |

The machine-readable register lives in `src/csm_copilot/data/rules.json`. It includes `source_url`, `source_section`, `reviewed_on`, `scope` and `authority` for each check.

## Official documentation versus operating choices

The official documentation motivates product checks. This project separately chooses to require a non-test-device evidence record and a callback verification record in its scoped checklist. It also chooses a three-day follow-up threshold, launch-date ordering and a CSM-to-technical-support handoff sequence. These are **project policies**, not claims about Unity's internal operating procedures or SLAs.

## Excluded from this version

Advertising campaign setup, advertiser creative moderation, Unity Ads payout/tax onboarding, app-ads.txt and direct-integration lifecycle rules are outside the Offerwall publisher workflow. They should not be added to every account merely because they belong to the same vendor ecosystem. No roadmap announcement is treated as an API integration this prototype possesses.

## Data provenance

Every account, company, app, issue, timestamp and customer message was invented for this project. Public product documentation supplies the source-backed checks; it does not supply the fictional customer evidence. The public repository contains no resume PDF, private job posting, real customer data, API credential or private contact information.
