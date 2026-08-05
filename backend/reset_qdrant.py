from qdrant_client import QdrantClient

client = QdrantClient(
    host="localhost",
    port=6333
)

collection_name = "opsmind"

if client.collection_exists(collection_name):
    client.delete_collection(collection_name)
    print(f"Deleted collection: {collection_name}")
else:
    print("Collection does not exist")