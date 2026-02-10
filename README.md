# TMS-Assistant

AI assistant for the Transportation Management System (TMS).  
This project leverages LLMs and custom pipelines to assist users and developers in interacting efficiently with the TMS through natural language.

<p align="center">
  <img src="./assets/demo.gif" alt="Demo" width="600"/>
</p>

---

## 📌 Features

✅ Natural language assistant for TMS queries  
✅ Filters context which is not relevant to the user query<br>
✅ Converts PDF to text using ```docling```, and adds it to the ```Qdrant VectorDB```


---

## 📁 Repository Structure

| File / Folder | Description |
|---------------|-------------|
| `app.py` | Main application entrypoint — runs the assistant service using Streamlit |
| `agent.py` | A simple agent to answer the user query using the relevant context |
| `cfg.py` | Configuration file for environment variablesAPI keys |
| `data_pipeline.py` | Pipeline to preprocess, ingest data to the VectorDB |
| `llm_stack.py` | Defines the LLM client, embedding model and VectorDB functions.|
| `requirements.txt` | Lists all Python dependencies needed to run the project |

---

## 🚀 Environment Setup

To get started locally, follow these steps:

### 🧠 Prerequisites

✔ Python 3.10 or above  
✔ `git` installed on your machine  

### 🛠️ Clone & Install

```bash
git clone https://github.com/mohan-gupta/TMS-Assistant.git
cd TMS-Assistant
```

### Create Python Environment
```bash
uv venv --python 3.12
```

### Activate the Python Environment
```bash
.venv\Scripts\activate # for windows

source .venv/bin/activate # for mac and linux
```
### Install the dependencies
```bash
uv pip install -r requirements.txt
```
### Create the .env file
```
GEMINI_API_KEY=<your api key>
QDRANT_API_KEY=<qdrant api key>
QDRANT_CLUSTER_URL=<cluster url>
```
### Finally run the app
```bash
streamlit run main.py
```