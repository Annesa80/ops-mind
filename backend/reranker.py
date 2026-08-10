from sentence_transformers import CrossEncoder


# ============================================================
# MODEL
# ============================================================

reranker_model = CrossEncoder(
    "BAAI/bge-reranker-base"
)


# ============================================================
# NORMALIZATION
# ============================================================

def normalize_scores(scores):

    if not scores:
        return []

    minimum = min(scores)
    maximum = max(scores)

    if maximum == minimum:
        return [1.0] * len(scores)

    return [
        (score - minimum) / (maximum - minimum)
        for score in scores
    ]


# ============================================================
# CONSERVATIVE RERANKING
# ============================================================

def rerank_documents(
    query,
    documents,
    top_k=5,
    bge_weight=0.20,
    rrf_weight=0.80
):

    if not documents:
        return []

    # --------------------------------------------------------
    # BGE scores
    # --------------------------------------------------------

    pairs = [
        (
            query,
            document["text"]
        )
        for document in documents
    ]

    bge_scores = reranker_model.predict(
        pairs
    )

    # --------------------------------------------------------
    # Normalize BGE scores
    # --------------------------------------------------------

    normalized_bge = normalize_scores(
        [
            float(score)
            for score in bge_scores
        ]
    )

    # --------------------------------------------------------
    # Create reranked candidates
    # --------------------------------------------------------

    reranked = []

    for (
        index,
        (
            document,
            bge_score,
            norm_bge
        )
    ) in enumerate(
        zip(
            documents,
            bge_scores,
            normalized_bge
        )
    ):

        original_rrf_rank = index + 1

        # ----------------------------------------------------
        # Rank-based RRF score
        #
        # RRF rank 1 = 1.0
        # RRF rank 2 = 0.5
        # RRF rank 3 = 0.333
        # etc.
        # ----------------------------------------------------

        rrf_rank_score = 1 / original_rrf_rank

        # ----------------------------------------------------
        # Conservative combination
        #
        # RRF = primary signal
        # BGE = secondary signal
        # ----------------------------------------------------

        combined_score = (
            rrf_weight * rrf_rank_score
            +
            bge_weight * norm_bge
        )

        reranked.append({
            "text": document["text"],
            "metadata": document["metadata"],

            "rrf_score": float(
                document.get(
                    "rrf_score",
                    0
                )
            ),

            "rerank_score": float(
                bge_score
            ),

            "normalized_bge_score": float(
                norm_bge
            ),

            "rrf_rank_score": float(
                rrf_rank_score
            ),

            "combined_score": float(
                combined_score
            ),

            "original_rrf_rank": original_rrf_rank
        })

    # --------------------------------------------------------
    # Final ranking
    # --------------------------------------------------------

    reranked.sort(
        key=lambda x: x["combined_score"],
        reverse=True
    )

    return reranked[:top_k]