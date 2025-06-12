from dotenv import load_dotenv
from vector_store import initialize_vector_store
from langchain_core.documents import Document


load_dotenv(".env")

def parse_and_embed_html():
    with open("data/reference_doc.html", "r") as f:
        html = f.read()
    
    words = html.split()
    chunk_size = 500
    overlap = 50
    chunks = []

    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)

    docs = []
    for i, chunk in enumerate(chunks):
        doc = Document(
            id=f"chunk_{i}",
            page_content=chunk,
            metadata={"chunk_index": i}
        )
        docs.append(doc)
    
    vector_store, _ = initialize_vector_store()
    vector_store.add_documents(docs)


parse_and_embed_html()