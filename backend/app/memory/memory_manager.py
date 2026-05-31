# memory/memory_manager.py

from agents.memory_classifier_agent import classify_memory


def process_memory(message):

    result = classify_memory(message)

    memory_type = result["memory_type"]

    if memory_type == "DO_NOT_STORE":
        return

    return {
        "content": message,
        "memory_type": memory_type,
        "importance": result["importance"]
    }