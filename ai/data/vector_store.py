from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
import os
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

load_dotenv(".env")

def initialize_vector_store():
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

    index_name = "ardupilot-reference-docs"

    if not pc.has_index(index_name):
        pc.create_index(
            name=index_name,
            dimension=1024,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1",
            )
        )

    index = pc.Index(index_name)

    embeddings = OpenAIEmbeddings(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="text-embedding-3-large",
        dimensions=1024
    )

    vector_store = PineconeVectorStore(index=index, embedding=embeddings)
    return vector_store, index
