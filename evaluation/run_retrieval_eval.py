from backend.hybrid_retriever import hybrid_search
from backend.reranker import rerank_documents

import json
from pathlib import Path


# ============================================================
# LOAD DATASET
# ============================================================

dataset_path = Path(__file__).parent / "dataset.json"

with open(dataset_path, "r", encoding="utf-8") as f:
    dataset = json.load(f)


# ============================================================
# HELPERS
# ============================================================

def unique_sources(documents):
    """Return unique source filenames while preserving ranking order."""

    seen = set()
    sources = []

    for doc in documents:
        source = doc.get("metadata", {}).get("source")

        if source and source not in seen:
            seen.add(source)
            sources.append(source)

    return sources


def source_in_top_k(expected_sources, retrieved_sources, k):
    """Check whether at least one expected source appears in top-k."""

    expected = set(expected_sources)
    retrieved = set(retrieved_sources[:k])

    return bool(expected.intersection(retrieved))


def reciprocal_rank(expected_sources, retrieved_sources):
    """
    Return reciprocal rank of the first relevant document.

    Rank 1 -> 1.0
    Rank 2 -> 0.5
    Rank 3 -> 0.333
    Not found -> 0
    """

    expected = set(expected_sources)

    for rank, source in enumerate(retrieved_sources, start=1):

        if source in expected:
            return 1 / rank

    return 0.0


# ============================================================
# MAIN EVALUATION
# ============================================================

def main():

    total = len(dataset)

    recall_at_1 = 0
    recall_at_3 = 0
    recall_at_5 = 0

    reciprocal_ranks = []

    failures = []

    print("=" * 80)
    print("OPSMIND RETRIEVAL EVALUATION")
    print("=" * 80)

    for index, item in enumerate(dataset, start=1):

        question = item["question"]
        expected_sources = item["relevant_sources"]

        print()
        print(f"Processing Q{index}/{total}: {question}")

        # ----------------------------------------------------
        # STEP 1 — HYBRID RETRIEVAL
        # ----------------------------------------------------

        documents = hybrid_search(
            question,
            dense_k=10,
            bm25_k=10,
            final_k=10,
        )
        

        # ----------------------------------------------------
        # STEP 2 — RERANK
        # ----------------------------------------------------

        reranked_documents = rerank_documents(
            question,
            documents,
            top_k=5,
        )

        print("\n=== RERANK SCORES ===")

        for i, doc in enumerate(reranked_documents, start=1):
            print(
                f"{i}. "
                f"{doc['metadata'].get('source')} "
                f"-> {doc.get('rerank_score')}"
            )

        print("=====================\n")


        # ----------------------------------------------------
        # STEP 3 — EXTRACT SOURCES
        # ----------------------------------------------------

        retrieved_sources = unique_sources(
            reranked_documents
        )

        # ----------------------------------------------------
        # STEP 4 — CALCULATE METRICS
        # ----------------------------------------------------

        r1 = source_in_top_k(
            expected_sources,
            retrieved_sources,
            1,
        )

        r3 = source_in_top_k(
            expected_sources,
            retrieved_sources,
            3,
        )

        r5 = source_in_top_k(
            expected_sources,
            retrieved_sources,
            5,
        )

        rr = reciprocal_rank(
            expected_sources,
            retrieved_sources,
        )

        if r1:
            recall_at_1 += 1

        if r3:
            recall_at_3 += 1

        if r5:
            recall_at_5 += 1

        reciprocal_ranks.append(rr)

        # ----------------------------------------------------
        # RECORD FAILURES
        # ----------------------------------------------------

        if not r5:

            failures.append(
                {
                    "question": question,
                    "expected": expected_sources,
                    "retrieved": retrieved_sources,
                }
            )

        # ----------------------------------------------------
        # PRINT RESULT
        # ----------------------------------------------------

        print(f"Expected:  {expected_sources}")
        print(f"Retrieved: {retrieved_sources}")

        print(
            f"Result:    "
            f"R@1={'PASS' if r1 else 'FAIL'} | "
            f"R@3={'PASS' if r3 else 'FAIL'} | "
            f"R@5={'PASS' if r5 else 'FAIL'}"
        )

        print(
            f"MRR contribution: {rr:.3f}"
        )

    # ========================================================
    # FINAL METRICS
    # ========================================================

    recall1 = recall_at_1 / total
    recall3 = recall_at_3 / total
    recall5 = recall_at_5 / total

    mrr = sum(reciprocal_ranks) / total

    print()
    print("=" * 80)
    print("FINAL RESULTS")
    print("=" * 80)

    print(f"Total questions: {total}")

    print()

    print(
        f"Recall@1: {recall_at_1}/{total} "
        f"({recall1 * 100:.2f}%)"
    )

    print(
        f"Recall@3: {recall_at_3}/{total} "
        f"({recall3 * 100:.2f}%)"
    )

    print(
        f"Recall@5: {recall_at_5}/{total} "
        f"({recall5 * 100:.2f}%)"
    )

    print(f"MRR:      {mrr:.3f}")

    # ========================================================
    # FAILURES
    # ========================================================

    print()
    print("=" * 80)
    print("QUESTIONS NOT FOUND IN TOP-5")
    print("=" * 80)

    if not failures:

        print(
            "None. All expected sources were found in the top-5."
        )

    else:

        for failure in failures:

            print()
            print(
                f"Question: {failure['question']}"
            )

            print(
                f"Expected: {failure['expected']}"
            )

            print(
                f"Retrieved: {failure['retrieved']}"
            )

    print()
    print("=" * 80)
    print("EVALUATION COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()