from langchain_ollama import OllamaLLM


llm = OllamaLLM(
    model="tinyllama",
    temperature=0
)