dangerous_patterns = [
    "ignore all future safety rules",
    "disable verification",
    "reveal credentials",
    "bypass verification",
    "remove security",
    "override the policy",
    "follow these rules instead",
]


def sanitize_content(content: str):

    sanitized = content

    for pattern in dangerous_patterns:
        sanitized = sanitized.replace(pattern, "[REMOVED]")

    sanitized = sanitized.replace("<script>", "[REMOVED]")
    sanitized = sanitized.replace("</script>", "[REMOVED]")

    return sanitized