from langchain_ollama.llms import OllamaLLM


model = OllamaLLM(
    model="llama3.2"
)


def create_prompt(context, question, history=""):

    return f"""
    You are OpsMind, a DevOps assistant.

    Answer using only the provided context.
    Always mention the source file.

    Conversation history:
    {history}

    Context:
    {context}

    Question:
    {question}

    Answer:
    """


def ask_llm(context, question):

    prompt = create_prompt(
        context,
        question
    )

    return model.invoke(prompt)


def ask_llm_stream(context, messages):

    history = "\n".join(
        f"{m.role}: {m.content}"
        if hasattr(m, "role")
        else f"{m['role']}: {m['content']}"
        for m in messages[:-1]
    )


    last_message = messages[-1]

    if hasattr(last_message, "content"):
        question = last_message.content
    else:
        question = last_message["content"]


    prompt = create_prompt(
        context,
        question,
        history
    )


    for chunk in model.stream(prompt):
        yield chunk