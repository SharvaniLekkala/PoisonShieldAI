# memory/long_term.py

from app.memory.chroma_store import get_collection

collection = get_collection("long_term_memory")


def add_memory(memory):

    collection.add(
        documents=[memory["content"]],
        metadatas=[{
            "importance": memory["importance"]
        }],
        ids=[str(hash(memory["content"]))]
    )