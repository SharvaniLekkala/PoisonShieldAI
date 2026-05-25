from app.agents.validation_agent import validate_query
from app.agents.retrieval_agent import retrieve_data
from app.agents.sanitization_agent import sanitize_content
from app.agents.trust_agent import calculate_trust
from app.agents.memory_agent import store_memory

from app.llm.ollama_llm import llm


def run_workflow(query: str):

    # =========================
    # STEP 1 — VALIDATION
    # =========================

    validation = validate_query(query)

    if not validation["safe"]:

        return {
            "status": "blocked",
            "reason": validation["reason"]
        }

    # =========================
    # STEP 2 — RETRIEVAL
    # =========================

    docs = retrieve_data(query)

    combined_docs = " ".join(docs)

    # =========================
    # STEP 3 — TRUST ANALYSIS
    # =========================

    trust_score = calculate_trust(
    query,
    combined_docs
)

    # =========================
    # STEP 4 — SANITIZATION
    # =========================

    sanitized_content = sanitize_content(combined_docs)

    # =========================
    # STEP 5 — MEMORY STORAGE
    # =========================

    if trust_score >= 70:

        memory_status = store_memory(sanitized_content)

    else:

        memory_status = "Memory rejected due to low trust"

    # =========================
    # STEP 6 — LLM PROMPT
    # =========================

    prompt = f"""
    You are a secure enterprise AI assistant.

    Answer ONLY using the trusted context provided below.

    If the information is not present in the context,
    say you do not know.

    Trusted Context:
    {sanitized_content}

    User Query:
    {query}
    """

    # =========================
    # STEP 7 — GENERATE RESPONSE
    # =========================

    response = llm.invoke(prompt)

    # =========================
    # STEP 8 — FINAL OUTPUT
    # =========================

    return {
        "status": "success",
        "trust_score": trust_score,
        "memory_status": memory_status,
        "retrieved_content": sanitized_content,
        "response": response
    }