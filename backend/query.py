from backend.retriever import retriever
from backend.llm import ask_llm
from backend.llm import ask_llm_stream


def ask_opsmind(question: str):

    docs = retriever.invoke(question)

    context = "\n\n".join(
        f"Source: {doc.metadata['source']}\n{doc.page_content}"
        for doc in docs
    )

    answer = ask_llm(
        context=context,
        question=question
    )

    sources = list({
        doc.metadata["source"]
        for doc in docs
    })

    return {
        "answer": answer,
        "sources": sources
    }

def ask_opsmind_stream(question):

    docs = retriever.invoke(question)

    context = "\n\n".join(
        f"Source: {doc.metadata['source']}\n{doc.page_content}"
        for doc in docs
    )

    for chunk in ask_llm_stream(
        context,
        question
    ):
        yield chunk