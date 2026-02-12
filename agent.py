import nest_asyncio
nest_asyncio.apply()

import json

from llm_stack import get_llm_response, vector_search

def generate_response(query: str, threshold = 0.65):
    context = vector_search(query, threshold=threshold)
    
    context_text = [item[0] for item in context]
    context_score = [item[1] for item in context]
    score = sum(context_score)/len(context_score)
    
    rag_prompt = f"""
    Answer the user query, using the provided context.
    If you are not provided with any context or the context is empty,
    then simply respond to the user that you couldn't find any relevant inforamtion.
    
    query: {query}
    
    context: {context_text}
    """
    
    response = get_llm_response(rag_prompt)
    
    response += f"\n\nConfidence score: {round(score, 3)*100}%"
    
    return response

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