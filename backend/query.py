from backend.hybrid_retriever import hybrid_search
from backend.reranker import rerank_documents

from backend.llm import (
    ask_llm,
    ask_llm_stream,
    kb_can_answer,
    run_official_tool,
    ask_official_docs
)


# ============================================================
# NON-STREAMING
# ============================================================

def ask_opsmind(question: str):

    # ============================================================
    # STEP 1 — SEARCH OPSMIND KNOWLEDGE BASE
    # ============================================================

    documents = hybrid_search(
        question,
        dense_k=5,
        bm25_k=5,
        final_k=10
    )

    reranked_documents = rerank_documents(
        question,
        documents,
        top_k=5
    )

    context = "\n\n".join(

        f"Source: {document['metadata']['source']}\n"
        f"{document['text']}"

        for document in reranked_documents

    )

    # ============================================================
    # STEP 2 — ASK OPSMIND KNOWLEDGE BASE
    # ============================================================

    answer = ask_llm(
        context=context,
        question=question
    )

    # ============================================================
    # STEP 3 — KB CAN ANSWER
    # ============================================================

    if answer.strip() != "KB_INSUFFICIENT":

        sources = list({
            document["metadata"]["source"]
            for document in reranked_documents
        })

        return {
            "answer": answer,
            "sources": sources
        }

    # ============================================================
    # STEP 4 — KB CANNOT ANSWER
    # TRY OFFICIAL DOCUMENTATION
    # ============================================================

    official_result = run_official_tool(question)

    # ============================================================
    # STEP 5 — NO OFFICIAL DOCUMENTATION TOOL
    # ============================================================

    if not official_result:

        return {
            "answer": (
                "I don't know. "
                "I couldn't find enough information in the "
                "OpsMind knowledge base or the available "
                "official documentation."
            ),
            "sources": []
        }

    # ============================================================
    # STEP 6 — ASK LLM USING ONLY OFFICIAL DOCUMENTATION
    # ============================================================

    official_answer = ask_official_docs(
        question=question,
        context=official_result
    )

    # ============================================================
    # STEP 7 — OFFICIAL DOCUMENTATION IS ALSO INSUFFICIENT
    # ============================================================

    if official_answer.strip() == "OFFICIAL_DOCS_INSUFFICIENT":

        return {
            "answer": (
                "I don't know. "
                "I couldn't find enough information in the "
                "OpsMind knowledge base or the available "
                "official documentation."
            ),
            "sources": []
        }

    # ============================================================
    # STEP 8 — RETURN OFFICIAL DOCUMENTATION ANSWER
    # ============================================================

    return {
        "answer": official_answer,
        "sources": [
            "official_kubernetes_documentation"
        ]
    }


# ============================================================
# STREAMING
# ============================================================

def ask_opsmind_stream(messages):

    latest_question = messages[-1].content

    # ========================================================
    # HISTORY
    # ========================================================

    history = "\n".join(

        f"{m.role}: {m.content}"

        for m in messages

    )

    # ========================================================
    # SEARCH QUERY
    # ========================================================

    search_query = f"""
        Conversation:

        {history}

        Current question:

        {latest_question}
        """

    # ========================================================
    # LOCAL KB
    # ========================================================

    documents = hybrid_search(
        search_query,
        dense_k=5,
        bm25_k=5,
        final_k=10
    )

    # ========================================================
    # RERANK
    # ========================================================

    reranked_documents = rerank_documents(
        latest_question,
        documents,
        top_k=5
    )

    # ========================================================
    # CONTEXT
    # ========================================================

    context = "\n\n".join(

        f"Source: {document['metadata']['source']}\n"
        f"{document['text']}"

        for document in reranked_documents

    )

    # ========================================================
    # CHECK KB
    # ========================================================

    can_answer = kb_can_answer(
        context=context,
        question=latest_question
    )

    # ========================================================
    # KB ANSWER
    # ========================================================

    if can_answer:

        for chunk in ask_llm_stream(
            context,
            messages
        ):

            yield chunk

        return

    # ========================================================
    # OFFICIAL DOCUMENTATION FALLBACK
    # ========================================================

    official_answer = ask_official_docs(
        latest_question
    )

    if official_answer:

        yield official_answer

        return

    # ========================================================
    # NOTHING FOUND
    # ========================================================

    yield (
        "I don't have enough information in the "
        "OpsMind knowledge base or the official "
        "documentation to answer this question."
    )