from app.agents.validation_agent import validate_query
from app.agents.retrieval_agent import retrieve_data
from app.agents.sanitization_agent import sanitize_content
from app.agents.trust_agent import calculate_trust


def run_workflow(query: str):

    validation = validate_query(query)

    if not validation["safe"]:

        return {
            "query": query,
            "status": "blocked",
            "reason": validation["reason"]
        }

    retrieved_docs = retrieve_data(query)

    combined_docs = " ".join(retrieved_docs)

    trust_score = calculate_trust(combined_docs)

    sanitized_content = sanitize_content(combined_docs)

    return {
        "query": query,
        "status": "success",
        "trust_score": trust_score,
        "sanitized_content": sanitized_content,
        "response": sanitized_content
    }