import os

from dotenv import load_dotenv

load_dotenv()

# Check directories
directory_path = "./upload_dir/"

if not os.path.exists(directory_path):
    os.mkdir("./upload_dir/")

gemini_api_key = os.getenv("GEMINI_API_KEY")
qdrant_api_key = os.getenv("QDRANT_API_KEY")
qdrant_cluster_url = os.getenv("QDRANT_CLUSTER_URL")