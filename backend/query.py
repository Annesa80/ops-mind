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


    docs = retriever.invoke(search_query)


    context = "\n\n".join(
        f"Source: {doc.metadata['source']}\n{doc.page_content}"
        for doc in docs
    )


    for chunk in ask_llm_stream(
        context,
        messages
    ):
        yield chunk