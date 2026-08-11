from backend.hybrid_retriever import hybrid_search
from backend.reranker import rerank_documents

from backend.llm import (
    ask_llm,
    ask_llm_stream,
    kb_can_answer,
    ask_web_llm,
    ask_web_llm_stream,
    web_can_answer,
    extract_web_sources
)

from backend.tools.web_search import web_search


# ============================================================
# NON-STREAMING
# ============================================================

def ask_opsmind(question: str):

    # ========================================================
    # STEP 1 — SEARCH OPSMIND KNOWLEDGE BASE
    # ========================================================

    documents = hybrid_search(
        question,
        dense_k=5,
        bm25_k=5,
        final_k=10
    )

    # ========================================================
    # STEP 2 — RERANK
    # ========================================================

    reranked_documents = rerank_documents(
        question,
        documents,
        top_k=5
    )

    # ========================================================
    # STEP 3 — BUILD KB CONTEXT
    # ========================================================

    context = "\n\n".join(
        f"Source: {document['metadata']['source']}\n"
        f"{document['text']}"
        for document in reranked_documents
    )

    # ========================================================
    # STEP 4 — CHECK KB
    # ========================================================

    can_answer = kb_can_answer(
        context=context,
        question=question
    )

    # ========================================================
    # STEP 5 — ANSWER FROM KB
    # ========================================================

    if can_answer:

        answer = ask_llm(
            context=context,
            question=question
        )

        sources = list({
            document["metadata"]["source"]
            for document in reranked_documents
        })

        return {
            "answer": answer,
            "sources": sources
        }

    # ========================================================
    # STEP 6 — KB INSUFFICIENT → WEB SEARCH
    # ========================================================

    web_result = web_search.invoke({
        "query": question
    })

    if not web_result:
        return {
            "answer": (
                "I don't know. "
                "I couldn't find enough information in the "
                "OpsMind knowledge base or the web."
            ),
            "sources": []
        }

    # CHECK WEB EVIDENCE

    can_answer_web = web_can_answer(
        context=web_result,
        question=question
    )

    if not can_answer_web:
        return {
            "answer": (
                "I don't know. "
                "I couldn't find enough information in the "
                "OpsMind knowledge base or the web."
            ),
            "sources": []
        }

    # ANSWER FROM WEB

    answer = ask_web_llm(
        context=web_result,
        question=question
    )

    sources = extract_web_sources(
        web_result
    )

    return {
        "answer": answer,
        "sources": sources
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
    # BUILD CONTEXT
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
    # KB INSUFFICIENT → WEB SEARCH
    # ========================================================

    web_result = web_search.invoke({
        "query": latest_question
    })

    # ========================================================
    # NO WEB RESULTS
    # ========================================================

    if not web_result:

        yield (
            "I don't know. "
            "I couldn't find enough information in the "
            "OpsMind knowledge base or the web."
        )

        return

    # ========================================================
    # ANSWER FROM WEB
    # ========================================================

    for chunk in ask_web_llm_stream(
        web_result,
        messages
    ):
        yield chunk