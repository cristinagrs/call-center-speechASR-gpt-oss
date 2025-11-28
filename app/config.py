import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".config")

# config, compartments and endpoints
CONFIG_FILE_PATH = os.getenv("CONFIG_FILE_PATH")
COMPARTMENT_ID = os.getenv("COMPARTMENT_ID")
PROFILE_NAME= os.getenv("PROFILE_NAME")
ENDPOINT = os.getenv("ENDPOINT")

## Vision Bucket:
BUCKET_NAMESPACE = os.getenv("BUCKET_NAMESPACE")
BUCKET_NAME = os.getenv("BUCKET_NAME")
BUCKET_FILE_PREFIX = "uploads"
SPEECH_BUCKET_OUTPUT_PREFIX = "speech_output"

## Other config params
ORACLE_LOGO = "app_images/oracle_logo.png"
UPLOAD_PATH = "uploaded_files"
GENAI_MODELS = {
    #"Meta Llama 3.3": "meta.llama-3.3-70b-instruct", 
    #"Cohere Command-A": "cohere.command-a-03-2025", 
    #"Cohere Command-R": "cohere.command-r-08-2024",
    "OpenAI GPT-OSS 120b": "openai.gpt-oss-120b",
    "OpenAI GPT-OSS 20b": "openai.gpt-oss-20b",

}
LIST_GENAI_MODELS = list(GENAI_MODELS.keys())

SUMMARIZE_PROMPT = """
Summarize the following conversation from a call center:
{conversation}

Rules:
- DO NOT invent additional information, use only the information in the text
- Give only the summary, in the following specific format:
   {format}
"""

SUMMARY_FORMAT = """
- **Calling reason:** specify why the user called.
- **Issue was solved:** specify ONLY yes or no, whether the issue was solved.
- **Information asked by the agent:** list the information the agent asked to complete the task.
- **Small summary:** 2 line summary of the call.
"""