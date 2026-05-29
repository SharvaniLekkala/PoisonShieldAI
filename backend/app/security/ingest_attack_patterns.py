from langchain_core.documents import Document

from app.security.attack_patterns import ATTACK_PATTERNS
from app.security.attack_store import attack_store


def ingest_attack_patterns():

    docs = []

    for pattern in ATTACK_PATTERNS:

        docs.append(
            Document(
                page_content=pattern,
                metadata={"type": "attack"}
            )
        )

    attack_store.add_documents(docs)

    print(
        f"Stored {len(docs)} attack patterns."
    )


if __name__ == "__main__":
    ingest_attack_patterns()