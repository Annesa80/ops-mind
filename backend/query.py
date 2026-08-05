from retriever import retriever

query = "Why is my Kubernetes pod stuck in CrashLoopBackOff?"

docs = retriever.invoke(query)

for doc in docs:
    print("SOURCE:", doc.metadata)
    print(doc.page_content)
    print("-"*50)