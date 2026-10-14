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
CALLBACK_SIGNAL = re.compile(r"callback|reward|回调|奖励|到账|发币")
CALLBACK_DENIAL = re.compile(
    r"(?<![a-z])(?:(?:reward\s+)?callbacks?|rewards?)(?![a-z])"
    rf"\s+{NEGATIVE_COPULA}\s+(?:our|my|the|a|an|this)\s+(?:problem|issue)(?![a-z])"
    r"|(?:不是|并非)(?:奖励回调|回调|奖励|到账|发币)(?:的)?(?:问题|故障)"
    r"|(?<![a-z])(?:reward\s+)?callbacks?(?![a-z])"
    r"\s+(?:(?:is|are)\s+not|(?:isn|aren)['’]t)\s+failing(?=[ \t]*(?:[.!;]|\n|$))"
)


def offerwall_signal(text: str) -> tuple[bool, bool]:
    return _scoped_signal(text, OFFERWALL_SIGNAL, EXPLICIT_DENIAL)


def callback_signal(text: str) -> tuple[bool, bool]:
    return _scoped_signal(text, CALLBACK_SIGNAL, CALLBACK_DENIAL)


def _scoped_signal(text: str, signal: re.Pattern, denial: re.Pattern) -> tuple[bool, bool]:
    """Return active/denied mention flags; another occurrence remains eligible."""
    text = text.casefold()
    denials = [match.span() for match in denial.finditer(text)]
    active = denied = False
    for match in signal.finditer(text):
        excluded = any(start <= match.start() and match.end() <= end for start, end in denials)
        denied |= excluded
        active |= not excluded
    return active, denied
