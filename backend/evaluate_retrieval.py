import sys
import os


sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


from retriever import retriever
from bm25_retriever import bm25_search
from hybrid_retriever import reciprocal_rank_fusion
from reranker import rerank_documents


# ============================================================
# TEST DATASET
# ============================================================

TEST_CASES = [

    # ========================================================
    # REDIS
    # ========================================================

    {
        "question": "Redis is reporting MISCONF. What is the likely reason?",
        "expected_source": "redis_troubleshooting.md",
        "expected_text": "Redis MISCONF Error"
    },
    {
        "question": "Why would Redis fail while creating an RDB snapshot?",
        "expected_source": "redis_troubleshooting.md",
        "expected_text": "Redis MISCONF Error"
    },
    {
        "question": "What could prevent Redis from writing its database snapshot to disk?",
        "expected_source": "redis_troubleshooting.md",
        "expected_text": "Redis MISCONF Error"
    },
    {
        "question": "What should I investigate if Redis cannot write its RDB file?",
        "expected_source": "redis_troubleshooting.md",
        "expected_text": "Redis MISCONF Error"
    },
    {
        "question": "Redis cannot write data to disk. What are the possible causes?",
        "expected_source": "redis_troubleshooting.md",
        "expected_text": "Redis MISCONF Error"
    },
    {
        "question": "Why is Redis unable to create a background database snapshot?",
        "expected_source": "redis_troubleshooting.md",
        "expected_text": "Redis MISCONF Error"
    },
    {
        "question": "What might cause Redis to fail when saving its database?",
        "expected_source": "redis_troubleshooting.md",
        "expected_text": "Redis MISCONF Error"
    },
    {
        "question": "Redis cannot save its database to disk. What should I check?",
        "expected_source": "redis_troubleshooting.md",
        "expected_text": "Redis MISCONF Error"
    },

    # ========================================================
    # DOCKER
    # ========================================================

    {
        "question": "Why does a Docker container repeatedly start and stop?",
        "expected_source": "docker_notes.md",
        "expected_text": "Container keeps restarting"
    },
    {
        "question": "What could cause a Docker container to restart continuously?",
        "expected_source": "docker_notes.md",
        "expected_text": "Container keeps restarting"
    },
    {
        "question": "My Docker application crashes during startup. What should I check?",
        "expected_source": "docker_notes.md",
        "expected_text": "Application Error"
    },
    {
        "question": "What can cause an application inside a Docker container to fail?",
        "expected_source": "docker_notes.md",
        "expected_text": "Application Error"
    },
    {
        "question": "How can I investigate why a Docker container keeps restarting?",
        "expected_source": "docker_notes.md",
        "expected_text": "Container keeps restarting"
    },
    {
        "question": "My container launches and then immediately dies. What could be wrong?",
        "expected_source": "docker_notes.md",
        "expected_text": "Container keeps restarting"
    },
    {
        "question": "What command should I use to see Docker container logs?",
        "expected_source": "docker_notes.md",
        "expected_text": "docker logs"
    },
    {
        "question": "How can I inspect the logs from a Docker container?",
        "expected_source": "docker_notes.md",
        "expected_text": "docker logs"
    },
    {
        "question": "What happens when required environment variables are missing?",
        "expected_source": "docker_notes.md",
        "expected_text": "Missing Environment Variables"
    },
    {
        "question": "Why might a Docker application fail during startup because of configuration?",
        "expected_source": "docker_notes.md",
        "expected_text": "Missing Environment Variables"
    },
    {
        "question": "How can I inspect the environment and details of a container?",
        "expected_source": "docker_notes.md",
        "expected_text": "docker inspect"
    },
    {
        "question": "What command can I use to inspect a Docker container?",
        "expected_source": "docker_notes.md",
        "expected_text": "docker inspect"
    },
    {
        "question": "What happens when the application's port differs from the Docker port?",
        "expected_source": "docker_notes.md",
        "expected_text": "Incorrect Port Configuration"
    },
    {
        "question": "Why would a Docker application's port mapping cause problems?",
        "expected_source": "docker_notes.md",
        "expected_text": "Incorrect Port Configuration"
    },
    {
        "question": "How do I restart a Docker container?",
        "expected_source": "docker_notes.md",
        "expected_text": "docker restart"
    },
    {
        "question": "What command restarts an existing Docker container?",
        "expected_source": "docker_notes.md",
        "expected_text": "docker restart"
    },

    # ========================================================
    # KUBERNETES
    # ========================================================

    {
        "question": "Why does a Kubernetes pod enter CrashLoopBackOff?",
        "expected_source": "kubernetes_notes.md",
        "expected_text": "CrashLoopBackOff"
    },
    {
        "question": "What are common reasons for a Kubernetes pod to repeatedly crash?",
        "expected_source": "kubernetes_notes.md",
        "expected_text": "CrashLoopBackOff"
    },
    {
        "question": "My Kubernetes container starts and then crashes repeatedly. What should I investigate?",
        "expected_source": "kubernetes_notes.md",
        "expected_text": "CrashLoopBackOff"
    },
    {
        "question": "What Kubernetes command can I use to inspect pod logs?",
        "expected_source": "kubernetes_notes.md",
        "expected_text": "kubectl logs"
    },
    {
        "question": "How can I view logs from a crashing Kubernetes pod?",
        "expected_source": "kubernetes_notes.md",
        "expected_text": "kubectl logs"
    },
    {
        "question": "What configuration problems can cause a Kubernetes pod to fail?",
        "expected_source": "kubernetes_notes.md",
        "expected_text": "Missing Environment Variables"
    },
    {
        "question": "What should I check if a Kubernetes application is missing configuration?",
        "expected_source": "kubernetes_notes.md",
        "expected_text": "Missing Environment Variables"
    },
    {
        "question": "Why might a Kubernetes pod fail because of application errors?",
        "expected_source": "kubernetes_notes.md",
        "expected_text": "Application Failure"
    },
    {
        "question": "What should I investigate when a pod keeps crashing?",
        "expected_source": "kubernetes_notes.md",
        "expected_text": "Application Failure"
    },
    {
        "question": "Why is my Kubernetes pod not accessible?",
        "expected_source": "kubernetes_notes.md",
        "expected_text": "not accessible"
    },
    {
        "question": "What could prevent traffic from reaching a Kubernetes pod?",
        "expected_source": "kubernetes_notes.md",
        "expected_text": "network policy"
    },
    {
        "question": "What should I investigate if Kubernetes traffic cannot reach the application?",
        "expected_source": "kubernetes_notes.md",
        "expected_text": "network policy"
    },

    # ========================================================
    # LINUX
    # ========================================================

    {
        "question": "How do I troubleshoot a permission denied error on Linux?",
        "expected_source": "linux_errors.md",
        "expected_text": "Permission denied"
    },
    {
        "question": "What could cause a Linux user to receive permission denied?",
        "expected_source": "linux_errors.md",
        "expected_text": "Permission denied"
    },
    {
        "question": "How can I check file permissions on Linux?",
        "expected_source": "linux_errors.md",
        "expected_text": "Incorrect File Permissions"
    },
    {
        "question": "What should I check if a Linux application cannot access a file?",
        "expected_source": "linux_errors.md",
        "expected_text": "Incorrect File Permissions"
    },
    {
        "question": "How can I investigate file access problems on Linux?",
        "expected_source": "linux_errors.md",
        "expected_text": "Incorrect File Permissions"
    },
    {
        "question": "How can I check whether a Linux system is running out of disk space?",
        "expected_source": "linux_errors.md",
        "expected_text": "Disk space problem"
    },
    {
        "question": "What should I investigate when applications fail because the disk is full?",
        "expected_source": "linux_errors.md",
        "expected_text": "Disk space problem"
    },
    {
        "question": "How can I determine whether disk usage is causing an application problem?",
        "expected_source": "linux_errors.md",
        "expected_text": "Disk space problem"
    },
    {
        "question": "What command checks Linux disk usage?",
        "expected_source": "linux_errors.md",
        "expected_text": "df -h"
    },
    {
        "question": "How can I find large files when the Linux disk is full?",
        "expected_source": "linux_errors.md",
        "expected_text": "du -sh"
    }
]


# ============================================================
# HELPERS
# ============================================================

def get_source(result):

    if hasattr(result, "metadata"):
        return result.metadata.get(
            "source",
            ""
        )

    return result["metadata"].get(
        "source",
        ""
    )


def get_text(result):

    if hasattr(result, "page_content"):
        return result.page_content

    return result["text"]


def find_rank(
    results,
    expected_source,
    expected_text
):

    for rank, result in enumerate(
        results,
        start=1
    ):

        source = get_source(result)
        text = get_text(result)

        if (
            source == expected_source
            and
            expected_text.lower() in text.lower()
        ):
            return rank

    return None


def recall_at_k(
    rank,
    k
):

    if rank is not None and rank <= k:
        return 1

    return 0


def reciprocal_rank(rank):

    if rank is None:
        return 0

    return 1 / rank


def average(values):

    if not values:
        return 0

    return sum(values) / len(values)


# ============================================================
# EVALUATION
# ============================================================

def evaluate():

    # --------------------------------------------------------
    # Metric storage
    # --------------------------------------------------------

    dense_r1 = []
    dense_r3 = []
    dense_r5 = []
    dense_mrr = []

    bm25_r1 = []
    bm25_r3 = []
    bm25_r5 = []
    bm25_mrr = []

    rrf_r1 = []
    rrf_r3 = []
    rrf_r5 = []
    rrf_mrr = []

    bge_r1 = []
    bge_r3 = []
    bge_r5 = []
    bge_mrr = []

    # --------------------------------------------------------
    # Regression storage
    # --------------------------------------------------------

    bge_regressions = []

    # ========================================================
    # RUN TESTS
    # ========================================================

    for index, test in enumerate(
        TEST_CASES,
        start=1
    ):

        question = test["question"]
        expected_source = test["expected_source"]
        expected_text = test["expected_text"]

        print()
        print("=" * 80)

        print(
            f"TEST {index}/{len(TEST_CASES)}"
        )

        print()
        print("QUESTION:")
        print(question)

        print()
        print("EXPECTED:")
        print(
            f"{expected_source} -> {expected_text}"
        )

        print("=" * 80)

        # ====================================================
        # DENSE
        # ====================================================

        dense_results = retriever.invoke(
            question
        )

        dense_results = dense_results[:10]

        # ====================================================
        # BM25
        # ====================================================

        bm25_results = bm25_search(
            question,
            k=10
        )

        # ====================================================
        # RRF
        # ====================================================

        rrf_results = reciprocal_rank_fusion(
            dense_results,
            bm25_results
        )

        rrf_results = rrf_results[:10]

        # ====================================================
        # BGE
        # ====================================================

        bge_results = rerank_documents(
            question,
            rrf_results,
            top_k=5
        )

        # ====================================================
        # FIND RANKS
        # ====================================================

        dense_rank = find_rank(
            dense_results,
            expected_source,
            expected_text
        )

        bm25_rank = find_rank(
            bm25_results,
            expected_source,
            expected_text
        )

        rrf_rank = find_rank(
            rrf_results,
            expected_source,
            expected_text
        )

        bge_rank = find_rank(
            bge_results,
            expected_source,
            expected_text
        )

        # ====================================================
        # METRICS
        # ====================================================

        dense_r1.append(
            recall_at_k(
                dense_rank,
                1
            )
        )

        dense_r3.append(
            recall_at_k(
                dense_rank,
                3
            )
        )

        dense_r5.append(
            recall_at_k(
                dense_rank,
                5
            )
        )

        dense_mrr.append(
            reciprocal_rank(
                dense_rank
            )
        )

        bm25_r1.append(
            recall_at_k(
                bm25_rank,
                1
            )
        )

        bm25_r3.append(
            recall_at_k(
                bm25_rank,
                3
            )
        )

        bm25_r5.append(
            recall_at_k(
                bm25_rank,
                5
            )
        )

        bm25_mrr.append(
            reciprocal_rank(
                bm25_rank
            )
        )

        rrf_r1.append(
            recall_at_k(
                rrf_rank,
                1
            )
        )

        rrf_r3.append(
            recall_at_k(
                rrf_rank,
                3
            )
        )

        rrf_r5.append(
            recall_at_k(
                rrf_rank,
                5
            )
        )

        rrf_mrr.append(
            reciprocal_rank(
                rrf_rank
            )
        )

        bge_r1.append(
            recall_at_k(
                bge_rank,
                1
            )
        )

        bge_r3.append(
            recall_at_k(
                bge_rank,
                3
            )
        )

        bge_r5.append(
            recall_at_k(
                bge_rank,
                5
            )
        )

        bge_mrr.append(
            reciprocal_rank(
                bge_rank
            )
        )

        # ====================================================
        # PRINT RANKS
        # ====================================================

        print()
        print("RANKS")
        print("-" * 80)

        print(
            f"Dense:     {dense_rank}"
        )

        print(
            f"BM25:      {bm25_rank}"
        )

        print(
            f"RRF:       {rrf_rank}"
        )

        print(
            f"RRF + BGE: {bge_rank}"
        )

        # ====================================================
        # BGE REGRESSION
        # ====================================================

        if (
            rrf_rank is not None
            and
            bge_rank is not None
            and
            bge_rank > rrf_rank
        ):

            bge_regressions.append({
                "question": question,
                "expected_source": expected_source,
                "expected_text": expected_text,
                "rrf_rank": rrf_rank,
                "bge_rank": bge_rank
            })

    # ========================================================
    # FINAL RESULTS
    # ========================================================

    print()
    print()
    print("=" * 80)

    print(
        "OPSMIND RETRIEVAL EVALUATION"
    )

    print("=" * 80)

    print()

    print(
        f"Test questions: {len(TEST_CASES)}"
    )

    print()

    print(
        f"{'Pipeline':<20}"
        f"{'Recall@1':<12}"
        f"{'Recall@3':<12}"
        f"{'Recall@5':<12}"
        f"{'MRR':<12}"
    )

    print("-" * 80)

    print(
        f"{'Dense':<20}"
        f"{average(dense_r1):<12.3f}"
        f"{average(dense_r3):<12.3f}"
        f"{average(dense_r5):<12.3f}"
        f"{average(dense_mrr):<12.3f}"
    )

    print(
        f"{'BM25':<20}"
        f"{average(bm25_r1):<12.3f}"
        f"{average(bm25_r3):<12.3f}"
        f"{average(bm25_r5):<12.3f}"
        f"{average(bm25_mrr):<12.3f}"
    )

    print(
        f"{'RRF':<20}"
        f"{average(rrf_r1):<12.3f}"
        f"{average(rrf_r3):<12.3f}"
        f"{average(rrf_r5):<12.3f}"
        f"{average(rrf_mrr):<12.3f}"
    )

    print(
        f"{'RRF + BGE':<20}"
        f"{average(bge_r1):<12.3f}"
        f"{average(bge_r3):<12.3f}"
        f"{average(bge_r5):<12.3f}"
        f"{average(bge_mrr):<12.3f}"
    )

    print("=" * 80)

    # ========================================================
    # BGE REGRESSIONS
    # ========================================================

    print()
    print("=" * 80)

    print(
        "BGE REGRESSION ANALYSIS"
    )

    print("=" * 80)

    print()

    if not bge_regressions:

        print(
            "No BGE regressions found."
        )

    else:

        print(
            f"BGE made {len(bge_regressions)} "
            f"results worse than RRF."
        )

        for index, failure in enumerate(
            bge_regressions,
            start=1
        ):

            print()
            print("-" * 80)

            print(
                f"REGRESSION {index}"
            )

            print()

            print(
                "QUESTION:"
            )

            print(
                failure["question"]
            )

            print()

            print(
                "EXPECTED:"
            )

            print(
                f"{failure['expected_source']} -> "
                f"{failure['expected_text']}"
            )

            print()

            print(
                f"RRF rank: {failure['rrf_rank']}"
            )

            print(
                f"BGE rank: {failure['bge_rank']}"
            )

    # ========================================================
    # SUMMARY
    # ========================================================

    print()
    print()
    print("=" * 80)

    print(
        "SUMMARY"
    )

    print("=" * 80)

    print()

    print(
        f"RRF Recall@1:     {average(rrf_r1):.3f}"
    )

    print(
        f"BGE Recall@1:     {average(bge_r1):.3f}"
    )

    print()

    print(
        f"RRF Recall@3:     {average(rrf_r3):.3f}"
    )

    print(
        f"BGE Recall@3:     {average(bge_r3):.3f}"
    )

    print()

    print(
        f"RRF Recall@5:     {average(rrf_r5):.3f}"
    )

    print(
        f"BGE Recall@5:     {average(bge_r5):.3f}"
    )

    print()

    print(
        f"RRF MRR:          {average(rrf_mrr):.3f}"
    )

    print(
        f"BGE MRR:          {average(bge_mrr):.3f}"
    )

    print()

    if (
        average(bge_mrr)
        >
        average(rrf_mrr)
    ):

        print(
            "BGE improved MRR over RRF."
        )

    elif (
        average(bge_mrr)
        <
        average(rrf_mrr)
    ):

        print(
            "BGE reduced MRR compared with RRF."
        )

    else:

        print(
            "BGE and RRF have the same MRR."
        )

    print()

    if not bge_regressions:

        print(
            "BGE regression count: 0"
        )

    else:

        print(
            f"BGE regression count: "
            f"{len(bge_regressions)}"
        )

    print()
    print("=" * 80)

    print("DONE")

    print("=" * 80)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    evaluate()