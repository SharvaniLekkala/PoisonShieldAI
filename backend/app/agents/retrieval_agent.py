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
            if score < 1.65:
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

                best_score = min(
                    score
                    for _, score in results
                )

                return {
                    "source": "memory",
                    "documents": unique_documents,
                    "retrieval_score": float(best_score)
                }

    except Exception as e:
        print("Retrieval Error:", e)

    # No relevant documents found
    return {
        "source": "memory",
        "documents": []
    }