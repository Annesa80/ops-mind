from backend.hybrid_retriever import hybrid_search
from backend.reranker import rerank_documents

from backend.llm import ask_llm
from backend.llm import ask_llm_stream


def ask_opsmind(question: str):

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


def ask_opsmind_stream(messages):

    latest_question = messages[-1].content


    history = "\n".join(

        f"{m.role}: {m.content}"
        for m in messages

    )


    search_query = f"""
        Conversation:
        {history}

        Current question:
        {latest_question}
        """


    documents = hybrid_search(
        search_query,
        dense_k=5,
        bm25_k=5,
        final_k=10
    )


    reranked_documents = rerank_documents(
        latest_question,
        documents,
        top_k=5
    )


    context = "\n\n".join(

        f"Source: {document['metadata']['source']}\n"
        f"{document['text']}"

        for document in reranked_documents

    )


    for chunk in ask_llm_stream(
        context,
        messages
    ):

        yield chunk