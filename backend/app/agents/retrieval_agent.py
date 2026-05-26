from app.memory.chroma_store import vector_store


STATIC_DOCS = [
    "Deployment workflow uses secure HTTPS endpoints.",
    "Internal API keys are encrypted.",
    "Security validation is mandatory before deployment."
]


def get_memory_retriever():
    return vector_store.as_retriever(search_kwargs={"k": 3})


def retrieve_data(query: str):

    try:
        relevant_docs = vector_store.similarity_search(query, k=3)

        if relevant_docs:
            unique_documents = []
            seen = set()

            for doc in relevant_docs:
                content = doc.page_content.strip()
                if content and content not in seen:
                    seen.add(content)
                    unique_documents.append(content)

            if unique_documents:
                return {
                    "source": "memory",
                    "documents": unique_documents
                }

    except Exception:
        pass

    return {
        "source": "static",
        "documents": STATIC_DOCS
    }