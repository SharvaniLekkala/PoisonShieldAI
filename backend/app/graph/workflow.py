from typing import TypedDict

from app.agents.validation_agent import validate_query
from app.agents.retrieval_agent import retrieve_data
from app.agents.sanitization_agent import sanitize_content


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
    sanitized_content: str
    response: str
    memory_status: str
    status: str

    security_status: str
    retrieval_quality: str
    


# =========================
# VALIDATION NODE
# =========================

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


# =========================
# SANITIZE QUERY
# =========================

def sanitize_node(state: GraphState) -> GraphState:

    return {
        "sanitized_query": sanitize_content(
            state["query"]
        ),
        "status": "sanitized"
    }


# =========================
# RETRIEVAL NODE
# =========================

def retrieval_node(state: GraphState) -> GraphState:

    retrieval_result = retrieve_data(
        state["sanitized_query"]
    )

    docs = retrieval_result["documents"]

    docs = retrieval_result["documents"]

    combined_docs = "\n\n".join(docs)

    return {
        "retrieval_source": retrieval_result.get(
            "source",
            "memory"
        ),
        "retrieved_documents": docs,
        "combined_docs": combined_docs,
        "status": "retrieved"
    }


# =========================
# TRUST NODE
# =========================

def trust_node(state: GraphState) -> GraphState:

    docs_count = len(
        state.get(
            "retrieved_documents",
            []
        )
    )

    if docs_count >= 5:
        retrieval_quality = "HIGH"

    elif docs_count >= 1:
        retrieval_quality = "MEDIUM"

    else:
        retrieval_quality = "LOW"

    security_status = (
        "BLOCKED"
        if state.get("blocked")
        else "SAFE"
    )

    return {
        "security_status": security_status,
        "retrieval_quality": retrieval_quality,
        "status": "trusted"
    }


# =========================
# SANITIZE CONTENT
# =========================

def sanitize_content_node(
    state: GraphState
) -> GraphState:

    return {
        "sanitized_content": sanitize_content(
            state["combined_docs"]
        ),
        "status": "content_sanitized"
    }


# =========================
# RESPONSE NODE
# =========================

def response_node(state: GraphState) -> GraphState:

    context = (
        state["sanitized_content"]
        .strip()
    )

    question = (
        state["sanitized_query"]
        .strip()
    )

    # No context
    if not context:

        return {
            "response":
                "I do not know based on the provided context.",
            "status": "answered"
        }
    

    prompt = f"""
Context:
{context}

Question:
{question}

Answer ONLY using the context above.
Keep the answer short and accurate.
Do NOT explain extra information.
"""
    if not state.get("retrieved_documents"):
        return {
            "response":
            "The requested information was not found in the uploaded documents.",
            "status": "answered"
        }
    response = llm.invoke(prompt)

    response = response.strip()

    blocked_phrases = [
        "Context:",
        "Question:",
        "Use ONLY",
        "provided context"
    ]

    for phrase in blocked_phrases:

        if phrase.lower() in response.lower():

            response = (
                "I do not know based on the provided context."
            )

            break

    return {
        "response": response,
        "status": "answered"
    }




# =========================
# MEMORY NODE
# =========================

def memory_node(
    state: GraphState
) -> GraphState:

    return {
        "memory_status":
            "Memory storage disabled",

        "status":
            "memory_skipped"
    }


# =========================
# GRAPH SETUP
# =========================

builder = StateGraph(GraphState)

builder.add_node(
    "validate_node",
    validate_node
)

builder.add_node(
    "sanitize_node",
    sanitize_node
)

builder.add_node(
    "retrieval_node",
    retrieval_node
)

builder.add_node(
    "trust_node",
    trust_node
)

builder.add_node(
    "sanitize_content_node",
    sanitize_content_node
)

builder.add_node(
    "response_node",
    response_node
)


builder.add_node(
    "memory_node",
    memory_node
)


builder.add_edge(
    START,
    "validate_node"
)


builder.add_conditional_edges(
    "validate_node",

    lambda state:
        END
        if state.get("blocked")
        else "sanitize_node"
)


builder.add_edge(
    "sanitize_node",
    "retrieval_node"
)

builder.add_edge(
    "retrieval_node",
    "trust_node"
)


builder.add_edge(
    "trust_node",
    "sanitize_content_node"
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
    "memory_node",
    END
)


workflow_graph = builder.compile()


# =========================
# MAIN WORKFLOW
# =========================

def run_workflow(query: str):

    result = workflow_graph.invoke({
        "query": query
    })

    if result.get("blocked"):

        return {

            "status": "blocked",

            "security_status":
                result.get(
                    "security_status",
                    "BLOCKED"
                ),

            "retrieval_quality":
                result.get(
                    "retrieval_quality",
                    "LOW"
                ),

            "memory_status":
                result.get(
                    "memory_status",
                    "Memory rejected due to unsafe input"
                ),

            "retrieval_source":
                result.get(
                    "retrieval_source",
                    "unknown"
                ),

            "retrieved_documents":
                result.get(
                    "retrieved_documents",
                    []
                ),

            "response":
                result.get(
                    "response",
                    "Request blocked due to security concerns."
                ),

            "reason":
                result.get(
                    "reason",
                    "Request blocked by validation."
                )
        }

    return {

        "status": "success",

        "security_status":
            result.get(
                "security_status",
                "SAFE"
            ),

        "retrieval_quality":
            result.get(
                "retrieval_quality",
                "LOW"
            ),

        "memory_status":
            result.get(
                "memory_status",
                "Memory storage disabled"
            ),

        "retrieval_source":
            result.get(
                "retrieval_source",
                "unknown"
            ),

        "retrieved_documents":
            result.get(
                "retrieved_documents",
                []
            ),

        "response":
            result.get(
                "response",
                "No response generated."
            ),

        "reason":
            result.get(
                "reason",
                "Query processed"
            )
    }