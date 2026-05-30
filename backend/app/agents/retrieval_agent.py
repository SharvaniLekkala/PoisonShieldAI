from app.memory.chroma_store import vector_store


def get_memory_retriever():
    return vector_store.as_retriever(search_kwargs={"k": 5})


def retrieve_data(query: str):

    try:
        query_lower = query.lower()

        summary_keywords = [
            "all",
            "summary",
            "overview",
            "policies",
            "policy",
            "guidelines",
            "requirements",
            "rules",
            "procedures"
        ]

        if any(
            keyword in query_lower
            for keyword in summary_keywords
        ):
            top_k = 3
        else:
            top_k = 1

        results = vector_store.similarity_search_with_score(
            query,
            k=top_k
        )
        print(
    f"\nRETRIEVAL MODE: k={top_k}"
)
        for doc, score in results:
            print(f"\nSCORE={score:.4f}")
            print(doc.page_content[:100])

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

                if top_k == 1:
                    docs_to_return = unique_documents[:1]
                else:
                    docs_to_return = unique_documents

                return {
                        "source": "memory",
                        "documents": docs_to_return,
                        "retrieval_score": float(best_score)
                    }

    except Exception as e:
        print("Retrieval Error:", e)

    # No relevant documents found
    return {
        "source": "memory",
        "documents": []
    }