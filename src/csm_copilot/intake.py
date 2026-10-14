"""Project intake wording; field presence does not establish evidence quality."""

REQUIRED_FIELDS = {
    "sdk_version": "Share the SDK version used in the affected app build.",
    "region": "Share the region where the issue was observed.",
    "time_window": "Share the observation start and end time, including date and timezone.",
    "reproduction_steps": (
        "Share the steps to reproduce the issue, including the expected and observed result."
    ),
    "redacted_logs": (
        "Share relevant logs with credentials, tokens, personal data and other secrets removed."
    ),
}

COLLECTION_BOUNDARY = (
    "Based on the five structured intake fields for this issue (project policy). "
    "Recorded values are not verified; review their content and the original report before asking. "
    "Details mentioned only in free text are not extracted automatically. "
    "Additional candidate-specific evidence may still be needed."
)
