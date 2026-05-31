# memory/episodic.py

from app.memory.chroma_store import get_collection

collection = get_collection("episodic_memory")


def add_memory(memory):

    collection.add(
        documents=[memory["content"]],
        metadatas=[{
            "importance": memory["importance"]
        }],
        ids=[str(hash(memory["content"]))]
    )