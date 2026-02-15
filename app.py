import json

import streamlit as st

from data_pipeline import pdf_to_text, add_doc_to_db, bytes_to_pdf
from agent import generate_response, extract_strucutred_data

def process_user_file():    
    uploaded_file = st.file_uploader(label="Upload you logistic document pdf.", type="pdf")
    text = None
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        
        file_path = bytes_to_pdf(bytes_data)
            
        with st.spinner("Loading", show_time=True):
            st.info("Analyzing your Data..")
            text = pdf_to_text(file_path)
            json_data = extract_strucutred_data(text)
            
            json_file_path = "upload_dir/temp_file.json"
            with open(json_file_path, "w") as f:
                json.dump(json_data, f, indent=2)
            
            st.info("Adding your data to VectorDB")
            add_doc_to_db(text)
        
        st.success("I am ready now, you may ask your queries.")
        
        st.session_state["file_uploaded"] = True

def get_strucutured_data():
    json_data = None
    if "file_uploaded" in st.session_state:
        json_file_path = "upload_dir/temp_file.json"
        with open(json_file_path) as f:
            json_data = json.load(f)
            
    return json_data

def chat_with_user():
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("Ask your Query!"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        response = generate_response(prompt)
        response = f"""```json 
        {json.dumps(response, indent=2)}"""
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

st.title('TMS Assistant')
st.html("<p>This Assistant, will help you with your logistic documents. You just need to upload your file and it will answer your queries.</p>")

if "file_uploaded" not in st.session_state:
    process_user_file()

json_data = get_strucutured_data()

if 'button_label' not in st.session_state:
    st.session_state.button_label = "Show Data"

def change_button_text():
    if st.session_state.button_label == "Show Data":
        st.markdown(f"```json {json.dumps(json_data, indent=2)}")
        st.session_state.button_label = "Hide Data"
    else:
        st.session_state.button_label = "Show Data"
        
st.button(
    label=st.session_state.button_label,
    on_click=change_button_text
)

chat_with_user()