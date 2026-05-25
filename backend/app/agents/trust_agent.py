suspicious_words = [
    "disable",
    "bypass",
    "override",
    "ignore",
    "reveal",
    "credentials",
    "remove security",
    "disable verification",
]


def calculate_trust(query: str, content: str):

    trust_score = 100

    combined = f"{query} {content}".lower()

    for word in suspicious_words:

        if word in combined:
            trust_score -= 25

    trust_score = max(trust_score, 0)

    return trust_score