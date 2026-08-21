from sentence_transformers import CrossEncoder


reranker_model = CrossEncoder(
    "BAAI/bge-reranker-base"
)


def rerank_documents(
    query,
    documents,
    top_k=5
):

    if not documents:
        return []

    pairs = [
        (
            query,
            document["text"]
        )
        for document in documents
    ]

    bge_scores = reranker_model.predict(pairs)

    reranked = []

    for document, bge_score in zip(
        documents,
        bge_scores
    ):

        reranked.append({
            "text": document["text"],
            "metadata": document["metadata"],
            "rrf_score": document.get(
                "rrf_score",
                0
            ),
            "rerank_score": float(bge_score)
        })

    reranked.sort(
        key=lambda x: x["rerank_score"],
        reverse=True
    )

    return reranked[:top_k]