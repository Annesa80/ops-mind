from langchain_ollama.llms import OllamaLLM

model = OllamaLLM(
    model="llama3.2"
)


def ask_llm(context, question):

    prompt = f"""
    You are OpsMind, a DevOps assistant.

    Answer using only the provided context.
    Always mention the source file.

    Context:
    {context}

    Question:
    {question}

    Answer:
    """

    return model.invoke(prompt)