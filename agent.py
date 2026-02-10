from llm_stack import get_llm_response, vector_search

def generate_response(query: str, threshold = 0.6):
    context = vector_search(query, threshold=threshold)
    
    rag_prompt = f"""
    Answer the user query, using the provided context.
    If you are not provided with any context or the context is empty,
    then simply respond to the user that you couldn't find any relevant inforamtion.
    
    query: {query}
    
    context: {context}
    """
    
    response = get_llm_response(rag_prompt)
    
    return response