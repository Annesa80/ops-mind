from llm import ask_llm
from vectorstore import vectorstore
from retriever import retriever



def main():

    question = input("Ask OpsMind: ")

    # Retrieve documents
    docs = retriever.invoke(question)


    # Combine context
    context = "\n\n".join(
        f"""
        Source: {doc.metadata.get('source')}
    
        Content:
        {doc.page_content}
        """
            for doc in docs
        )


    # Ask Ollama
    answer = ask_llm(
        context,
        question
    )


    print("\nAnswer:")
    print(answer)


    print("\nSources:")

    for doc in docs:
        print(
            "-",
            doc.metadata["source"]
        )


if __name__ == "__main__":
    main()