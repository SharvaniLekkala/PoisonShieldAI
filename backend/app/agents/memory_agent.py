from langchain_core.documents import Document
from app.memory.chroma_store import vector_store


def store_memory(content: str, metadata: dict | None = None):

    doc = Document(
        page_content=content,
        metadata=metadata or {}
    )

    vector_store.add_documents([doc])

    if hasattr(vector_store, "persist"):
        vector_store.persist()

    return "Memory stored securely"