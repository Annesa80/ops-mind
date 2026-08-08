from bm25_retriever import bm25_search


query = "Why does Redis MISCONF error happen?"


results = bm25_search(
    query,
    k=5
)


print("=" * 60)
print("QUERY:")
print(query)
print("=" * 60)


for i, result in enumerate(results, 1):

    print(f"\nRESULT {i}")
    print("-" * 60)

    print(
        "Source:",
        result["metadata"]["source"]
    )

    print(
        "Score:",
        result["score"]
    )

    print(
        result["text"][:500]
    )