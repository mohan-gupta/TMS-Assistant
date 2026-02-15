import nest_asyncio
nest_asyncio.apply()

import json

from llm_stack import get_llm_response, vector_search

def generate_response(query: str, threshold = 0.7):
    context, scores = vector_search(query, threshold=threshold)
    
    rag_prompt = f"""
    Answer the user query, using the provided context.
    
    ## Rules to follow:
    - Respond to the user query only if you have the right context.
    - If you are not provided with any context or the context is empty,
    then simply respond to the user that "Relevant Inforamtion Not found in document".
    - If user is greeting you then greet them.
    
    query: {query}
    
    context: {context}
    """
    
    response = get_llm_response(rag_prompt)
    
    if context is not None:
        return {
            "answer": response,
            "context": context,
            "retrieval score": round(sum(scores)/len(scores), 2)
        }
    
    return {
        "answer": response,
        "context": None,
        "retrieval score": None
    }

def extract_strucutred_data(unstructured_text: str):
    prompt = f"""
    Convert the following the data in structured JSON data.
    
    unstructured data: {unstructured_text}
    
    Only respond with the json data, don't generate any other information
    """
    
    response = get_llm_response(prompt)
    
    response = response.removeprefix("```json")
    response = response.removesuffix("```")
    
    json_response = json.loads(response)
    
    return json_response