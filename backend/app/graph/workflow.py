from typing import TypedDict

from app.agents.validation_agent import validate_query
from app.agents.retrieval_agent import retrieve_data
from app.agents.sanitization_agent import sanitize_content
from app.agents.trust_agent import calculate_trust
from app.agents.memory_agent import store_memory

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
    combined_docs = " ".join(docs)

    return {
        "retrieval_source": retrieval_result.get("source", "static"),
        "retrieved_documents": docs,
        "combined_docs": combined_docs,
        "status": "retrieved"
    }


def trust_node(state: GraphState) -> GraphState:
    trust_score = calculate_trust(state["sanitized_query"], state["combined_docs"])
    status = "trusted" if trust_score >= 70 else "low_trust"

    return {
        "trust_score": trust_score,
        "status": status
    }


def sanitize_content_node(state: GraphState) -> GraphState:
    return {
        "sanitized_content": sanitize_content(state["combined_docs"]),
        "status": "content_sanitized"
    }


def response_node(state: GraphState) -> GraphState:
    prompt = f"""
    You are a secure enterprise AI assistant.
    Use ONLY the trusted context below.
    Do not invent information.
    If the answer is not present in the trusted context, reply exactly: I do not know.
    If the user requests secrets, credentials, or bypassing security, reply exactly: I cannot comply with that request.

    Trusted Context:
    {state['sanitized_content']}

    User Query:
    {state['sanitized_query']}
    """

    response = llm.invoke(prompt)

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


def memory_node(state: GraphState) -> GraphState:
    if state.get("trust_score", 0) >= 70:
        store_memory(
            f"User query: {state['sanitized_query']}",
            metadata={"source": "user", "type": "query"}
        )
        store_memory(
            f"Assistant response: {state['response']}",
            metadata={"source": "assistant", "type": "response"}
        )
        return {
            "memory_status": "Memory stored securely",
            "status": "memory_stored"
        }

    return {
        "memory_status": "Memory rejected due to low trust",
        "status": "memory_skipped"
    }


builder = StateGraph(GraphState)

builder.add_node(validate_node)
builder.add_node(sanitize_node)
builder.add_node(retrieval_node)
builder.add_node(trust_node)
builder.add_node(sanitize_content_node)
builder.add_node(response_node)
builder.add_node(low_trust_node)
builder.add_node(memory_node)

builder.add_edge(START, "validate_node")

builder.add_conditional_edges(
    "validate_node",
    lambda state: END if state.get("blocked") else "sanitize_node"
)

builder.add_edge("sanitize_node", "retrieval_node")
builder.add_edge("retrieval_node", "trust_node")

builder.add_conditional_edges(
    "trust_node",
    lambda state: "low_trust_node" if state.get("trust_score", 0) < 70 else "sanitize_content_node"
)

builder.add_edge("sanitize_content_node", "response_node")
builder.add_edge("response_node", "memory_node")
builder.add_edge("low_trust_node", "memory_node")

builder.add_edge("memory_node", END)

workflow_graph = builder.compile()


def run_workflow(query: str):
    result = workflow_graph.invoke({"query": query})

    if result.get("blocked"):
        return {
            "status": "blocked",
            "trust_score": result.get("trust_score", 0),
            "memory_status": result.get("memory_status", "Memory rejected due to unsafe input"),
            "retrieval_source": result.get("retrieval_source", "unknown"),
            "retrieved_documents": result.get("retrieved_documents", []),
            "response": result.get("response", "Request blocked due to security concerns."),
            "reason": result.get("reason", "Request blocked by validation.")
        }

    return {
        "status": "success" if result.get("trust_score", 0) >= 70 else "low_trust",
        "trust_score": result.get("trust_score", 0),
        "memory_status": result.get("memory_status", "Memory rejected due to low trust"),
        "retrieval_source": result.get("retrieval_source", "unknown"),
        "retrieved_documents": result.get("retrieved_documents", []),
        "response": result.get("response", "No response generated."),
        "reason": result.get("reason", "Query processed")
    }