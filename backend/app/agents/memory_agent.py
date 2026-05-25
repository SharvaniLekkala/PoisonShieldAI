from langchain_core.documents import Document
from app.memory.chroma_store import vector_store


def store_memory(content: str):

    doc = Document(
        page_content=content
    )

    vector_store.add_documents([doc])

    return "Memory stored securely"