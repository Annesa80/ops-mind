from qdrant_client import QdrantClient

from langchain_qdrant import QdrantVectorStore
from langchain_huggingface import HuggingFaceEmbeddings


COLLECTION_NAME = "opsmind"


client = QdrantClient(
    host="localhost",
    port=6333
)


# Check collection exists
collections = client.get_collections()

names = [
    c.name
    for c in collections.collections
]


if COLLECTION_NAME not in names:
    raise Exception(
        "Vector database missing. Run ingestion first."
    )


embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


vectorstore = QdrantVectorStore(
    client=client,
    collection_name=COLLECTION_NAME,
    embedding=embedding,
    content_payload_key="text",
    metadata_payload_key="metadata",
)