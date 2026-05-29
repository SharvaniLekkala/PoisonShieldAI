import re

from app.security.attack_store import attack_store


# ==================================================
# REGEX ATTACK DETECTION
# ==================================================

REGEX_PATTERNS = [

    # Password extraction
    r"(show|reveal|display|provide|give).*(password)",

    # Credentials
    r"(show|reveal|display|provide|give).*(credential)",

    # API keys
    r"(show|reveal|display|provide|give).*(api\s*key)",

    # Private keys
    r"(show|reveal|display|provide|give).*(private\s*key)",

    # Secrets
    r"(show|reveal|display|provide|give).*(secret)",

    # Prompt injection
    r"(ignore|disregard|override).*(instruction)",

    # Safety bypass
    r"(disable|remove|bypass).*(safety|security|verification)",

    # Memory poisoning
    r"(remember|store).*(forever|permanently)",

]


def validate_query(query: str):

    lower_query = query.lower().strip()

    # =====================================
    # REGEX CHECK
    # =====================================

    for pattern in REGEX_PATTERNS:

        if re.search(pattern, lower_query):

            return {
                "safe": False,
                "reason":
                    f"Regex attack detected",
                "risk_score": 1.0
            }

    # =====================================
    # SEMANTIC ATTACK DETECTION
    # =====================================

    try:

        results = attack_store.similarity_search_with_score(
            query,
            k=3
        )

        if results:

            best_score = min(
                score
                for _, score in results
            )

            print(
                f"ATTACK SCORE: {best_score}"
            )

            # Tune later
            if best_score < 0.75:

                return {
                    "safe": False,
                    "reason":
                        "Semantic attack detected",
                    "risk_score":
                        float(best_score)
                }

    except Exception as e:

        print(
            "Attack Detection Error:",
            e
        )

    # =====================================
    # LENGTH CHECK
    # =====================================

    if len(query) > 2000:

        return {
            "safe": False,
            "reason":
                "Query too long",
            "risk_score": 1.0
        }

    return {
        "safe": True,
        "reason":
            "Query validated successfully",
        "risk_score": 0.0
    }