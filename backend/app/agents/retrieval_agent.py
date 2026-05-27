from app.memory.chroma_store import vector_store


def get_memory_retriever():
    return vector_store.as_retriever(search_kwargs={"k": 5})


def retrieve_data(query: str):

    try:

        results = vector_store.similarity_search_with_score(
            query,
            k=5
        )

        filtered_docs = []

        for doc, score in results:

            # Lower score = better match
            if score < 2:
                filtered_docs.append(doc)

        if filtered_docs:

            unique_documents = []
            seen = set()

            for doc in filtered_docs:

                content = doc.page_content.strip()

                if content and content not in seen:

                    seen.add(content)
                    unique_documents.append(content)

            if unique_documents:

                return {
                    "source": "memory",
                    "documents": unique_documents
                }

    except Exception as e:
        print("Retrieval Error:", e)

    # No relevant documents found
    return {
        "source": "memory",
        "documents": []
    }