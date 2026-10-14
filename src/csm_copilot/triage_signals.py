"""Bounded lexical matching. Explicit local denials are not general semantic parsing."""

import re

OFFERWALL_SIGNAL = re.compile(
    r"(?<![a-z])(?:blank(?:s|ed|ing|ness)?|no offers|no ads|empty offerwalls?)(?![a-z])"
    r"|空白|没广告|没有广告|无广告|不展示"
)
NEGATIVE_COPULA = r"(?:(?:is|are|was|were)\s+not|(?:isn|aren|wasn|weren)['’]t)"
EXPLICIT_DENIAL = re.compile(
    r"(?<![a-z])(?:no offers|no ads|empty offerwalls?|blank(?: screen)?)(?![a-z])"
    rf"\s+{NEGATIVE_COPULA}\s+(?:our|my|the|a|an|this)\s+(?:problem|issue)(?![a-z])"
    rf"|(?<![a-z]){NEGATIVE_COPULA}\s+blank(?![a-z])"
    r"|(?:不是|并非)(?:没有广告|没广告|无广告|不展示|空白)(?:的)?(?:问题|故障)"
    r"|(?:并不|不再)(?:是)?空白"
)


def offerwall_signal(text: str) -> tuple[bool, bool]:
    """Return active/denied mention flags; another occurrence remains eligible."""
    text = text.casefold()
    denials = [match.span() for match in EXPLICIT_DENIAL.finditer(text)]
    active = denied = False
    for match in OFFERWALL_SIGNAL.finditer(text):
        excluded = any(start <= match.start() and match.end() <= end for start, end in denials)
        denied |= excluded
        active |= not excluded
    return active, denied
