from backend.retriever import retriever
from backend.bm25_retriever import bm25_search


def reciprocal_rank_fusion(
    dense_results,
    bm25_results,
    k=60
):

    scores = {}

    documents = {}


    # ----------------------------------------
    # Dense retrieval
    # ----------------------------------------

    for rank, doc in enumerate(
        dense_results,
        start=1
    ):

        source = doc.metadata["source"]

        doc_id = (
            source,
            doc.page_content
        )


        scores[doc_id] = (
            scores.get(
                doc_id,
                0
            )
            +
            1 / (k + rank)
        )


        documents[doc_id] = {

            "text": doc.page_content,

            "metadata": doc.metadata

        }


    # ----------------------------------------
    # BM25 retrieval
    # ----------------------------------------

    for rank, doc in enumerate(
        bm25_results,
        start=1
    ):

        source = doc["metadata"]["source"]

        doc_id = (
            source,
            doc["text"]
        )


        scores[doc_id] = (
            scores.get(
                doc_id,
                0
            )
            +
            1 / (k + rank)
        )


        documents[doc_id] = {

            "text": doc["text"],

            "metadata": doc["metadata"]

        }


    # ----------------------------------------
    # Sort by RRF score
    # ----------------------------------------

    ranked = sorted(
        scores.items(),
        key=lambda item: item[1],
        reverse=True
    )


    results = []


    for doc_id, score in ranked:

        document = documents[doc_id]


        results.append({

            "text": document["text"],

            "metadata": document["metadata"],

            "rrf_score": score

        })


    return results


def hybrid_search(
    query,
    dense_k=10,
    bm25_k=10,
    final_k=20
):

    # ----------------------------------------
    # Dense retrieval
    # ----------------------------------------

    dense_results = retriever.invoke(query)[:dense_k]


    # ----------------------------------------
    # BM25 retrieval
    # ----------------------------------------

    bm25_results = bm25_search(
        query,
        k=bm25_k
    )


    # ----------------------------------------
    # RRF
    # ----------------------------------------

    results = reciprocal_rank_fusion(
        dense_results,
        bm25_results
    )

    return results[:final_k]