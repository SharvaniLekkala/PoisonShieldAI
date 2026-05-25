from langchain_community.vectorstores import Chroma

from app.memory.embeddings import embedding_model


vector_store = Chroma(
    collection_name="secure_memory",
    embedding_function=embedding_model,
    persist_directory="./chroma_db"
)