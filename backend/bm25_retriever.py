from rank_bm25 import BM25Okapi

from qdrant_client import QdrantClient


COLLECTION_NAME = "opsmind"


client = QdrantClient(
    host="localhost",
    port=6333
)


def load_documents():

    points, _ = client.scroll(
        collection_name=COLLECTION_NAME,
        limit=10000,
        with_payload=True
    )

    documents = []

    for point in points:

        payload = point.payload

        documents.append({
            "text": payload["text"],
            "metadata": payload["metadata"]
        })

    return documents


documents = load_documents()


tokenized_documents = [
    document["text"].lower().split()
    for document in documents
]


bm25 = BM25Okapi(
    tokenized_documents
)


def bm25_search(
    query,
    k=5
):

    tokenized_query = query.lower().split()

    scores = bm25.get_scores(
        tokenized_query
    )

    ranked_indices = sorted(
        range(len(scores)),
        key=lambda i: scores[i],
        reverse=True
    )


    results = []

    for index in ranked_indices[:k]:

        document = documents[index]

        results.append({
            "text": document["text"],
            "metadata": document["metadata"],
            "score": float(scores[index])
        })


    return results