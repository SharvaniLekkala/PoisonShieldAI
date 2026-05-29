from langchain_chroma import Chroma

from app.memory.embeddings import embedding_model

attack_store = Chroma(
    collection_name="attack_patterns",
    embedding_function=embedding_model,
    persist_directory="./attack_db"
)