blocked_patterns = [
    "ignore previous instructions",
    "reveal api keys",
    "disable safety",
    "bypass verification",
    "reveal credentials",
]


def validate_query(query: str):

    lower_query = query.lower()

    for pattern in blocked_patterns:

        if pattern in lower_query:

            return {
                "safe": False,
                "reason": f"Blocked pattern detected: {pattern}"
            }

    return {
        "safe": True,
        "reason": "Query validated successfully"
    }