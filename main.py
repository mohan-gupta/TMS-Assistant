from fastapi import FastAPI, UploadFile
from fastapi.exceptions import HTTPException

from pydantic import BaseModel

from data_pipeline import bytes_to_pdf, pdf_to_text, add_doc_to_db

from agent import generate_response, extract_strucutred_data

app = FastAPI()

class QueryInp(BaseModel):
    query: str

@app.post('/upload')
async def upload_file(file: UploadFile):
    if file.content_type != "application/pdf":
        raise HTTPException(422, detail="Upload a pdf file!!")

    bytes_data = await file.read()
    file_path = bytes_to_pdf(bytes_data)
    
    text = pdf_to_text(file_path)
    add_doc_to_db(text)
    
    return {
        "response": "Success"
    }

@app.post("/ask")
async def answer_query(inp: QueryInp):
    response = generate_response(inp.query)
    
    return {
        "response": response
    }

@app.post("/extract")
async def extract_data(file: UploadFile):
    if file.content_type != "application/pdf":
        raise HTTPException(422, detail="Upload a pdf file!!")

    bytes_data = await file.read()
    file_path = bytes_to_pdf(bytes_data)
    
    text = pdf_to_text(file_path)
    
    json_data = extract_strucutred_data(text)
    
    return {
        "response": json_data
    }
