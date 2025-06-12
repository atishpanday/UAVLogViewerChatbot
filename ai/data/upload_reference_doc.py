from dotenv import load_dotenv
from vector_store import vector_store, index
from langchain_core.documents import Document


load_dotenv(".env")

def parse_and_embed_html():
    # Fetch and parse HTML
    with open("data/reference_doc.html", "r") as f:
        html = f.read()
    
    # Split text into chunks with overlap
    words = html.split()
    chunk_size = 500
    overlap = 50
    chunks = []

    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)

    # Clear previous data in index
    # index.delete(delete_all=True)
    
    # Prepare documents for storage
    docs = []
    for i, chunk in enumerate(chunks):
        doc = Document(
            id=f"chunk_{i}",
            page_content=chunk,
            metadata={"chunk_index": i}
        )
        docs.append(doc)
    
    # Upload to Pinecone vector store
    vector_store.add_documents(docs)


parse_and_embed_html()