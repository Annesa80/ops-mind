from hybrid_retriever import hybrid_search
from reranker import rerank_documents


query = "Why does Redis MISCONF error happen?"


print("=" * 70)
print("HYBRID RETRIEVAL")
print("=" * 70)


documents = hybrid_search(
    query,
    dense_k=5,
    bm25_k=5,
    final_k=10
)


for i, document in enumerate(
    documents,
    start=1
):

    print()
    print(f"RESULT {i}")
    print("-" * 70)

    print(
        "Source:",
        document["metadata"]["source"]
    )

    print(
        "RRF score:",
        document["rrf_score"]
    )

    print(
        document["text"][:500]
    )


print()
print("=" * 70)
print("AFTER RERANKING")
print("=" * 70)


reranked = rerank_documents(
    query,
    documents,
    top_k=5
)


for i, document in enumerate(
    reranked,
    start=1
):

    print()
    print(f"RESULT {i}")
    print("-" * 70)

    print(
        "Source:",
        document["metadata"]["source"]
    )

    print(
        "RRF score:",
        document["rrf_score"]
    )

    print(
        "Rerank score:",
        document["rerank_score"]
    )

    print(
        document["text"][:500]
    )