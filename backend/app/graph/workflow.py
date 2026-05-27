from typing import TypedDict

from app.agents.validation_agent import validate_query
from app.agents.retrieval_agent import retrieve_data
from app.agents.sanitization_agent import sanitize_content
from app.agents.trust_agent import calculate_trust

from app.llm.ollama_llm import llm
from langgraph.graph import END, START, StateGraph


class GraphState(TypedDict, total=False):
    query: str
    blocked: bool
    reason: str
    validated: bool
    sanitized_query: str
    retrieval_source: str
    retrieved_documents: list[str]
    combined_docs: str
    trust_score: int
    sanitized_content: str
    response: str
    memory_status: str
    status: str


def validate_node(state: GraphState) -> GraphState:

    validation = validate_query(state["query"])

    if not validation["safe"]:
        return {
            "blocked": True,
            "status": "blocked",
            "reason": validation["reason"],
            "memory_status": "Memory rejected due to unsafe input"
        }

    return {
        "blocked": False,
        "validated": True,
        "status": "validated",
        "reason": validation["reason"]
    }


def sanitize_node(state: GraphState) -> GraphState:

    return {
        "sanitized_query": sanitize_content(state["query"]),
        "status": "sanitized"
    }


def retrieval_node(state: GraphState) -> GraphState:

    retrieval_result = retrieve_data(state["sanitized_query"])

    docs = retrieval_result["documents"]

    # Better document separation
    combined_docs = "\n\n".join(docs)

    return {
        "retrieval_source": retrieval_result.get("source", "static"),
        "retrieved_documents": docs,
        "combined_docs": combined_docs,
        "status": "retrieved"
    }


def trust_node(state: GraphState) -> GraphState:

    trust_score = calculate_trust(
        state["sanitized_query"],
        state["combined_docs"]
    )

    status = "trusted" if trust_score >= 70 else "low_trust"

    return {
        "trust_score": trust_score,
        "status": status
    }


def sanitize_content_node(state: GraphState) -> GraphState:

    return {
        "sanitized_content": sanitize_content(
            state["combined_docs"]
        ),
        "status": "content_sanitized"
    }


def response_node(state: GraphState) -> GraphState:

    context = state["sanitized_content"].strip()
    question = state["sanitized_query"].strip()

    # If no context exists
    if not context:
        return {
            "response": "I do not know based on the provided context.",
            "status": "answered"
        }

    # VERY IMPORTANT:
    # simple keyword relevance check BEFORE LLM

    query_words = question.lower().split()

    context_lower = context.lower()

    matches = sum(
        1 for word in query_words
        if word in context_lower
    )

    # If query unrelated to retrieved docs
    if matches <= 1:
        return {
            "response": "I do not know based on the provided context.",
            "status": "answered"
        }

    # SIMPLER PROMPT
    prompt = f"""
Context:
{context}

Question:
{question}

Answer ONLY using the context above.
If answer is not in context, say:
I do not know based on the provided context.
"""

    response = llm.invoke(prompt)

    # Extra cleanup
    response = response.strip()

    # Prevent prompt leakage
    blocked_phrases = [
        "RULES:",
        "Context:",
        "Question:",
        "Use ONLY",
        "Never use",
        "provided context"
    ]

    for phrase in blocked_phrases:

        if phrase.lower() in response.lower():

            response = "I do not know based on the provided context."
            break

    return {
        "response": response,
        "status": "answered"
    }

def low_trust_node(state: GraphState) -> GraphState:

    return {
        "response": "Unable to generate a trusted response because the request did not pass security trust thresholds.",
        "memory_status": "Memory rejected due to low trust",
        "status": "blocked"
    }


# MEMORY DISABLED
# Prevents vector DB pollution
def memory_node(state: GraphState) -> GraphState:

    return {
        "memory_status": "Memory storage disabled",
        "status": "memory_skipped"
    }


builder = StateGraph(GraphState)

builder.add_node("validate_node", validate_node)
builder.add_node("sanitize_node", sanitize_node)
builder.add_node("retrieval_node", retrieval_node)
builder.add_node("trust_node", trust_node)
builder.add_node("sanitize_content_node", sanitize_content_node)
builder.add_node("response_node", response_node)
builder.add_node("low_trust_node", low_trust_node)
builder.add_node("memory_node", memory_node)

builder.add_edge(START, "validate_node")

builder.add_conditional_edges(
    "validate_node",
    lambda state: END if state.get("blocked") else "sanitize_node"
)

builder.add_edge("sanitize_node", "retrieval_node")

builder.add_edge("retrieval_node", "trust_node")

builder.add_conditional_edges(
    "trust_node",
    lambda state:
        "low_trust_node"
        if state.get("trust_score", 0) < 70
        else "sanitize_content_node"
)

builder.add_edge(
    "sanitize_content_node",
    "response_node"
)

builder.add_edge(
    "response_node",
    "memory_node"
)

builder.add_edge(
    "low_trust_node",
    "memory_node"
)

builder.add_edge(
    "memory_node",
    END
)

workflow_graph = builder.compile()


def run_workflow(query: str):

    result = workflow_graph.invoke({
        "query": query
    })

    if result.get("blocked"):

        return {
            "status": "blocked",
            "trust_score": result.get("trust_score", 0),
            "memory_status": result.get(
                "memory_status",
                "Memory rejected due to unsafe input"
            ),
            "retrieval_source": result.get(
                "retrieval_source",
                "unknown"
            ),
            "retrieved_documents": result.get(
                "retrieved_documents",
                []
            ),
            "response": result.get(
                "response",
                "Request blocked due to security concerns."
            ),
            "reason": result.get(
                "reason",
                "Request blocked by validation."
            )
        }

    return {
        "status":
            "success"
            if result.get("trust_score", 0) >= 70
            else "low_trust",

        "trust_score": result.get("trust_score", 0),

        "memory_status": result.get(
            "memory_status",
            "Memory storage disabled"
        ),

        "retrieval_source": result.get(
            "retrieval_source",
            "unknown"
        ),

        "retrieved_documents": result.get(
            "retrieved_documents",
            []
        ),

        "response": result.get(
            "response",
            "No response generated."
        ),

        "reason": result.get(
            "reason",
            "Query processed"
        )
    }