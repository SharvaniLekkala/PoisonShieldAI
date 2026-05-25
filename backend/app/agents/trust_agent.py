suspicious_words = [
    "disable",
    "bypass",
    "override",
    "ignore",
]


def calculate_trust(content: str):

    trust_score = 100

    lower_content = content.lower()

    for word in suspicious_words:

        if word in lower_content:
            trust_score -= 25

    trust_score = max(trust_score, 0)

    return trust_score