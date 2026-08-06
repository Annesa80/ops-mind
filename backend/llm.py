from langchain_ollama.llms import OllamaLLM


model = OllamaLLM(
    model="llama3.2"
)


def create_prompt(context, question):

    return f"""
    You are OpsMind, a DevOps assistant.

    Answer using only the provided context.
    Always mention the source file.

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



def ask_llm_stream(context, question):

    prompt = create_prompt(
        context,
        question
    )

    for chunk in model.stream(prompt):
        yield chunk