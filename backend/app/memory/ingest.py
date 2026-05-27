from pathlib import Path

from langchain_core.documents import Document

from app.memory.chroma_store import vector_store


# IMPORTANT
# Go from app/memory -> backend/data
DATA_PATH = Path(__file__).resolve().parents[2] / "data"


def ingest_documents():

    print("\n=== INGEST STARTED ===")
    print("Looking inside:", DATA_PATH)

    documents = []

    txt_files = list(DATA_PATH.glob("*.txt"))

    print("TXT FILES FOUND:", len(txt_files))

    for file_path in txt_files:

        print("\nReading:", file_path.name)

        try:

            with open(file_path, "r", encoding="utf-8") as file:

                content = file.read()

                print("Characters:", len(content))

                documents.append(
                    Document(
                        page_content=content,
                        metadata={
                            "source": file_path.name
                        }
                    )
                )

        except Exception as e:
            print("ERROR READING FILE:", e)

    if documents:

        print("\nAdding documents to ChromaDB...")

        vector_store.add_documents(documents)

        print(f"\nSUCCESS: Ingested {len(documents)} documents.")

    else:
        print("\nNO DOCUMENTS FOUND TO INGEST")


if __name__ == "__main__":
    ingest_documents()