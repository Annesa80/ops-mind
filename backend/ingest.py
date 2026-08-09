import os
import uuid

from langchain_community.document_loaders import (
    DirectoryLoader,
    TextLoader,
    PyPDFLoader,
    Docx2txtLoader,
)

from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)

from sentence_transformers import SentenceTransformer

from qdrant_client import QdrantClient
from qdrant_client.models import (
    PointStruct,
    VectorParams,
    Distance,
)


COLLECTION_NAME = "opsmind"


client = QdrantClient(
    host="localhost",
    port=6333
)


embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

def clean_filename(path: str) -> str:
    filename = os.path.basename(path)

    parts = filename.split("_", 1)

    if len(parts) == 2 and len(parts[0]) == 36:
        return parts[1]

    return filename

def create_collection():

    collections = client.get_collections()

    existing = [
        c.name
        for c in collections.collections
    ]

    if COLLECTION_NAME not in existing:

        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE
            )
        )


def add_documents(documents):

    create_collection()

    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[
            ("#", "h1"),
            ("##", "h2"),
            ("###", "h3"),
        ],
        strip_headers=False
    )

    recursive_splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=100
    )

    chunks = []

    for document in documents:

        source = clean_filename(
            document.metadata.get(
                "source",
                "unknown"
            )
        )

        markdown_chunks = markdown_splitter.split_text(
            document.page_content
        )

        for chunk in markdown_chunks:

            chunk.metadata["source"] = source

            if len(chunk.page_content) > 700:

                smaller_chunks = recursive_splitter.split_documents(
                    [chunk]
                )

                chunks.extend(
                    smaller_chunks
                )

            else:

                chunks.append(
                    chunk
                )

    texts = [
        chunk.page_content
        for chunk in chunks
    ]

    embeddings = embedding_model.encode(
        texts
    )

    points = []

    for chunk, vector in zip(
        chunks,
        embeddings
    ):

        points.append(

            PointStruct(

                id=str(uuid.uuid4()),

                vector=vector.tolist(),

                payload={

                    "text": chunk.page_content,

                    "metadata": {

                        "source": clean_filename(
                            chunk.metadata.get(
                                "source",
                                "unknown"
                            )
                        ),

                        "h1": chunk.metadata.get(
                            "h1",
                            ""
                        ),

                        "h2": chunk.metadata.get(
                            "h2",
                            ""
                        ),

                        "h3": chunk.metadata.get(
                            "h3",
                            ""
                        )
                    }
                }
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

    return len(points)



def ingest_file(filepath):

    extension = os.path.splitext(
        filepath
    )[1].lower()


    if extension in [".md", ".txt"]:

        loader = TextLoader(
            filepath
        )


    elif extension == ".pdf":

        loader = PyPDFLoader(
            filepath
        )


    elif extension == ".docx":

        loader = Docx2txtLoader(
            filepath
        )


    else:

        raise ValueError(
            f"Unsupported file type: {extension}"
        )


    documents = loader.load()


    return add_documents(
        documents
    )



def ingest_directory(
    path="./knowledge_base"
):

    loader = DirectoryLoader(
        path,
        glob="**/*.md",
        loader_cls=TextLoader
    )


    documents = loader.load()


    return add_documents(
        documents
    )



if __name__ == "__main__":

    count = ingest_directory()

    print(
        f"Inserted {count} chunks"
    )