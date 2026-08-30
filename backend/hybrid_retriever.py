from backend.retriever import retriever
from backend.bm25_retriever import bm25_search


# ============================================================
# CHUNK-LEVEL RRF
# ============================================================

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

        # Chunk-level identity
        doc_id = (
            source,
            doc.page_content
        )

        scores[doc_id] = (
            scores.get(doc_id, 0)
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

        # Chunk-level identity
        doc_id = (
            source,
            doc["text"]
        )

        scores[doc_id] = (
            scores.get(doc_id, 0)
            +
            1 / (k + rank)
        )

        documents[doc_id] = {
            "text": doc["text"],
            "metadata": doc["metadata"]
        }

    # ----------------------------------------
    # Sort chunks by RRF score
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


# ============================================================
# DOCUMENT-LEVEL RANKING
# ============================================================

def rank_documents_by_first_occurrence(
    rrf_results
):

    document_ranking = {}
    document_first_chunks = {}

    # ----------------------------------------
    # First occurrence of each source
    # ----------------------------------------

    for rank, result in enumerate(
        rrf_results,
        start=1
    ):

        source = result["metadata"]["source"]

        # Only keep the first/highest-ranked chunk
        if source not in document_ranking:

            document_ranking[source] = rank

            document_first_chunks[source] = result

    # ----------------------------------------
    # Sort documents by first chunk rank
    # ----------------------------------------

    ranked_documents = sorted(
        document_ranking.items(),
        key=lambda item: item[1]
    )

    return [
        {
            "source": source,
            "first_rank": first_rank,
            "first_chunk": document_first_chunks[source]
        }
        for source, first_rank in ranked_documents
    ]


# ============================================================
# SELECT CHUNKS FOR RERANKER
# ============================================================

def select_chunks_for_reranker(
    rrf_results,
    max_documents=10,
    max_chunks_per_document=2
):

    # ----------------------------------------
    # Get document-level ranking
    # ----------------------------------------

    ranked_documents = rank_documents_by_first_occurrence(
        rrf_results
    )

    # ----------------------------------------
    # Select top documents
    # ----------------------------------------

    selected_sources = {
        document["source"]
        for document in ranked_documents[:max_documents]
    }

    # ----------------------------------------
    # Select chunks from those documents
    #
    # Chunks remain ordered by RRF score.
    # ----------------------------------------

    selected_chunks = []
    source_counts = {}

    for result in rrf_results:

        source = result["metadata"]["source"]

        # Ignore documents outside document-level top N
        if source not in selected_sources:
            continue

        count = source_counts.get(source, 0)

        # Maximum 2 chunks from each source
        if count >= max_chunks_per_document:
            continue

        selected_chunks.append(result)

        source_counts[source] = count + 1

    return selected_chunks


# ============================================================
# HYBRID SEARCH
# ============================================================

def hybrid_search(
    query,
    dense_k=10,
    bm25_k=10,
    final_k=20,
    max_documents=10,
    max_chunks_per_document=2
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
    # Chunk-level RRF
    # ----------------------------------------

    rrf_results = reciprocal_rank_fusion(
        dense_results,
        bm25_results
    )

    # ----------------------------------------
    # Document-level ranking
    #
    # Each unique source is ranked according
    # to the first occurrence of that source
    # in the RRF ranking.
    # ----------------------------------------

    document_ranking = rank_documents_by_first_occurrence(
        rrf_results
    )

    # ----------------------------------------
    # Select chunks for reranker
    #
    # Top documents according to document rank
    # Maximum 2 chunks per document
    # ----------------------------------------

    reranker_candidates = select_chunks_for_reranker(
        rrf_results,
        max_documents=max_documents,
        max_chunks_per_document=max_chunks_per_document
    )

    # ----------------------------------------
    # Debug output
    # ----------------------------------------

    print("\n=== HYBRID RETRIEVAL ===")
    print("Query:", query)

    print("\nDense results:")
    for i, doc in enumerate(
        dense_results,
        start=1
    ):
        print(
            f"{i}. "
            f"{doc.metadata.get('source')}"
        )

    print("\nBM25 results:")
    for i, doc in enumerate(
        bm25_results,
        start=1
    ):
        print(
            f"{i}. "
            f"{doc['metadata'].get('source')}"
        )

    print("\nRRF chunk results:")
    for i, doc in enumerate(
        rrf_results[:final_k],
        start=1
    ):
        print(
            f"{i}. "
            f"{doc['metadata'].get('source')} "
            f"-> {doc['rrf_score']}"
        )

    print("\nDocument ranking:")
    for i, document in enumerate(
        document_ranking[:max_documents],
        start=1
    ):
        print(
            f"{i}. "
            f"{document['source']} "
            f"(first chunk rank: "
            f"{document['first_rank']})"
        )

    print("\nReranker candidates:")
    for i, doc in enumerate(
        reranker_candidates,
        start=1
    ):
        print(
            f"{i}. "
            f"{doc['metadata'].get('source')} "
            f"-> {doc['rrf_score']}"
        )

    print("========================\n")

    return reranker_candidates
