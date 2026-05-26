blocked_patterns = [
    "ignore previous instructions",
    "reveal api keys",
    "disable safety",
    "bypass verification",
    "reveal credentials",
    "ignore all future safety rules",
    "remove security",
    "override the policy",
    "follow these rules instead",
]

suspicious_tokens = [
    "password",
    "secret",
    "ssn",
    "credit card",
    "private key",
    "api key",
]


def validate_query(query: str):

    lower_query = query.lower()

    for pattern in blocked_patterns:
        if pattern in lower_query:
            return {
                "safe": False,
                "reason": f"Blocked prompt-injection pattern detected: {pattern}"
            }

    for token in suspicious_tokens:
        if token in lower_query:
            return {
                "safe": False,
                "reason": f"Sensitive information request detected: {token}"
            }

    if len(lower_query) > 2000:
        return {
            "safe": False,
            "reason": "Query rejected because it is too long for secure processing."
        }

    return {
        "safe": True,
        "reason": "Query validated successfully"
    }