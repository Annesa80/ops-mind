from backend.retriever import retriever

docs = retriever.invoke("How do I fix Kubernetes keep crashing?")

for i, doc in enumerate(docs, 1):
    print("=" * 50)
    print(i)
    print(doc.metadata)
    print(doc.page_content[:300])