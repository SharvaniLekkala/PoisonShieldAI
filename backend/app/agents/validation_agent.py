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

# Only block explicit credential extraction attempts
sensitive_patterns = [
    "show password",
    "reveal password",
    "give me password",
    "give me passwords",
    "dump passwords",
    "dump credentials",
    "show credentials",
    "reveal credentials",
    "show api key",
    "reveal api key",
    "give me api key",
    "show private key",
    "reveal private key",
]


def validate_query(query: str):

    lower_query = query.lower().strip()

    # Prompt injection detection
    for pattern in blocked_patterns:

        if pattern in lower_query:

            return {
                "safe": False,
                "reason":
                    f"Blocked prompt-injection pattern detected: {pattern}"
            }

    # Sensitive information extraction detection
    for pattern in sensitive_patterns:

        if pattern in lower_query:

            return {
                "safe": False,
                "reason":
                    f"Sensitive information request detected: {pattern}"
            }

    # Excessively long query protection
    if len(lower_query) > 2000:

        return {
            "safe": False,
            "reason":
                "Query rejected because it is too long for secure processing."
        }

    return {
        "safe": True,
        "reason": "Query validated successfully"
    }