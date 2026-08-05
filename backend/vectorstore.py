from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore
from langchain_huggingface import HuggingFaceEmbeddings


client = QdrantClient(
    host="localhost",
    port=6333
)


# Check collection exists first
collections = client.get_collections()

names = [
    c.name
    for c in collections.collections
]

if "opsmind" not in names:
    raise Exception(
        "Vector database missing. Run ingestion first."
    )


# Load embedding model
embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# Connect LangChain to existing Qdrant collection
vectorstore = QdrantVectorStore(
    client=client,
    collection_name="opsmind",
    embedding=embedding,
    content_payload_key="text",
    metadata_payload_key="metadata",
)