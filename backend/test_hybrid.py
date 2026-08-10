from hybrid_retriever import hybrid_search
from reranker import rerank_documents


queries = [

    "Why does Redis MISCONF error happen?",

    "Why is my Kubernetes pod crashing?",

    "How do I fix Nginx 502?"

]


for query in queries:

    print()
    print("=" * 70)
    print("QUERY:")
    print(query)
    print("=" * 70)


    # --------------------------------------------------
    # Hybrid retrieval
    # --------------------------------------------------

    hybrid_results = hybrid_search(
        query,
        dense_k=5,
        bm25_k=5,
        final_k=10
    )


    print()
    print("HYBRID RESULTS")
    print("-" * 70)


    for i, result in enumerate(
        hybrid_results,
        start=1
    ):

        print()
        print(f"RESULT {i}")
        print("-" * 70)

        print(
            "Source:",
            result["metadata"]["source"]
        )

        print(
            "RRF score:",
            result["rrf_score"]
        )

        print(
            result["text"][:500]
        )


    # --------------------------------------------------
    # BGE reranking
    # --------------------------------------------------

    reranked_results = rerank_documents(
        query,
        hybrid_results,
        top_k=5
    )


    print()
    print()
    print("AFTER RERANKING")
    print("-" * 70)


    for i, result in enumerate(
        reranked_results,
        start=1
    ):

        print()
        print(f"RESULT {i}")
        print("-" * 70)

        print(
            "Source:",
            result["metadata"]["source"]
        )

        print(
            "RRF score:",
            result["rrf_score"]
        )

        print(
            "Rerank score:",
            result["rerank_score"]
        )

        print(
            result["text"][:500]
        )


    print()
    print("=" * 70)