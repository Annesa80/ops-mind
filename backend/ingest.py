from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from sentence_transformers import SentenceTransformer

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct


# Load documents
loader = DirectoryLoader(
    "./knowledge_base",
    glob="**/*.md",
    loader_cls=TextLoader
)

documents = loader.load()


# Split
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks = splitter.split_documents(documents)


# Embed
embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

texts = [
    chunk.page_content
    for chunk in chunks
]

embeddings = embedding_model.encode(texts)


from qdrant_client.models import VectorParams, Distance


# Connect Qdrant
client = QdrantClient(
    host="localhost",
    port=6333
)


# Create collection if missing
collections = client.get_collections()

existing_collections = [
    c.name for c in collections.collections
]

if "opsmind" not in existing_collections:
    client.create_collection(
        collection_name="opsmind",
        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE
        )
    )


# Store
points = []

for i, (chunk, vector) in enumerate(zip(chunks, embeddings)):
    points.append(
        PointStruct(
            id=i,
            vector=vector.tolist(),
            payload={
                "text": chunk.page_content,
                "metadata": {
                    "source": chunk.metadata["source"]
                }
            }
        )
    )


client.upsert(
    collection_name="opsmind",
    points=points
)


print(client.count(
    collection_name="opsmind"
))