import re

suspicious_words = [
    "disable",
    "bypass",
    "override",
    "ignore",
    "reveal",
    "credentials",
    "remove security",
    "disable verification",
    "secret",
    "password",
    "api key",
    "private key",
]


def calculate_trust(query: str, content: str):

    trust_score = 100

    combined = f"{query} {content}".lower()

    for word in suspicious_words:
        if re.search(rf"\b{re.escape(word)}\b", combined):
            trust_score -= 20

    if re.search(r"\bresearch\b", combined) and re.search(r"\bmalicious\b", combined):
        trust_score -= 15

    if len(combined) > 1500:
        trust_score -= 10

    trust_score = max(trust_score, 0)

    return trust_score