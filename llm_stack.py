from uuid import uuid4

from typing import List

from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance, PointStruct

from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from google.genai.types import EmbedContentConfig
from llama_index.llms.google_genai import GoogleGenAI

from cfg import gemini_api_key, qdrant_api_key, qdrant_cluster_url

qdrant_client = QdrantClient(
    url=qdrant_cluster_url, 
    api_key=qdrant_api_key,
    check_compatibility=False
)

COLLECTION_NAME = "tms_vectorstore"
EMBEDDING_SIZE = 768

embedding_config = EmbedContentConfig(output_dimensionality=EMBEDDING_SIZE)
embed_model = GoogleGenAIEmbedding(
    model_name="models/gemini-embedding-001",
    embed_batch_size=100,
    embedding_config=embedding_config,
    api_key=gemini_api_key
)

llm = GoogleGenAI(model = "gemini-2.5-flash-lite", api_key=gemini_api_key, temperature=0)

def generate_chunk_embeddings(chunks: List[str]):
    chunk_embeddings = []
    for chunk_text in chunks:
        text_embedding = embed_model.get_text_embedding(chunk_text)
        chunk_embeddings.append(text_embedding)
    
    return chunk_embeddings

def get_llm_response(prompt):
    response = llm.complete(prompt)
    
    return response.text

def setup_vectordb():
    qdrant_client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=EMBEDDING_SIZE, distance=Distance.COSINE),
    )
    
def insert_document(doc):
    points = [
        PointStruct(
            id=str(uuid4()),
            vector=doc["embedding"],
            payload={"text":doc["text"]}
        )
    ]
    
    response = qdrant_client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )
    
    return response
    
def vector_search(query: str, top_k:int = 3, threshold=0.6):
    query_embedding = embed_model.get_text_embedding(query)
    
    search_results = qdrant_client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        limit=top_k
    )
    context = [(point.payload["text"], point.score) for point in search_results.points]
    
    filtered_context = [item[0] for item in context if item[1]>=threshold]
    
    return filtered_context

if __name__ == "__main__":
    setup_vectordb()