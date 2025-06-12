from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
import os
from langchain_mistralai import MistralAIEmbeddings
from langchain_pinecone import PineconeVectorStore

load_dotenv(".env")

# initialize MongoDB python client

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

embeddings = MistralAIEmbeddings(api_key=os.getenv("MISTRAL_API_KEY"), model="mistral-embed")

vector_store = PineconeVectorStore(index=index, embedding=embeddings)
