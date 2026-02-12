from docling.document_converter import DocumentConverter

from llama_index.core.node_parser import TokenTextSplitter

from llm_stack import generate_chunk_embeddings, insert_document

def bytes_to_pdf(bytes_data):
    file_path = "upload_dir/temp_file.pdf"
    with open(file_path, "wb") as f:
        f.write(bytes_data)
        
    return file_path

def pdf_to_text(file_path: str):
    converter = DocumentConverter()
    result = converter.convert(file_path)
    
    return result.document.export_to_markdown()

def text_to_chunks(text: str) -> list[str]:
    text_parser = TokenTextSplitter(chunk_size=384, chunk_overlap=32)
    text_chunks = text_parser.split_text(text)
    
    return text_chunks
    

def add_doc_to_db(text):
    """
    Create embedding of chunks and add the chunks of the document to VectorDB
    """
    chunks = text_to_chunks(text)
    
    chunk_embeddings = generate_chunk_embeddings(chunks)
    
    for idx, text in enumerate(chunks):
        doc_obj = {
            "text": text,
            "embedding": chunk_embeddings[idx]
        }
        response = insert_document(doc_obj)
    
    return
