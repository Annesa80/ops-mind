from backend.vectorstore import vectorstore


retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={
        "k": 10
    }
)