from backend.retriever import retriever
from backend.llm import ask_llm


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