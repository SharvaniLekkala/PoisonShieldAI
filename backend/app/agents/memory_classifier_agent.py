# agents/memory_classifier_agent.py

from langchain_ollama import OllamaLLM
import json

llm = OllamaLLM(model="llama3.2:3b")


def classify_memory(message: str):

    prompt = f"""
You are a memory classification agent.

Classify the message into EXACTLY ONE category.

SHORT_TERM
- Current project details
- Ongoing debugging information
- Current task context
- Session-specific information
- Information likely needed later in this conversation

EPISODIC
- Achievements
- Experiences
- Completed projects
- Completed internships
- Milestones
- Events

LONG_TERM
- Preferences
- Skills
- Career goals
- Stable personal information
- Long-lasting user facts

DO_NOT_STORE
- Greetings
- Small talk
- Standalone factual questions
- General knowledge questions
- Questions that do not describe the user

Examples:

"My project uses ChromaDB"
→ SHORT_TERM

"I'm debugging my memory classifier"
→ SHORT_TERM

"I completed my Parkinson internship"
→ EPISODIC

"I built PoisonShieldAI"
→ EPISODIC

"I prefer Python over Java"
→ LONG_TERM

"My goal is to become an AI Engineer"
→ LONG_TERM

"Explain transformers"
→ DO_NOT_STORE

"What is attention?"
→ DO_NOT_STORE

Return ONLY valid JSON:

{{
    "memory_type":"SHORT_TERM|EPISODIC|LONG_TERM|DO_NOT_STORE",
    "importance":0.0
}}

Message:
{message}
"""

    response = llm.invoke(prompt)

    try:
        return json.loads(response)

    except:
        return {
            "memory_type": "DO_NOT_STORE",
            "importance": 0.0
        }