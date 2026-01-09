import pdfplumber
from langchain_core.tools import tool
from langchain_community.document_loaders import WebBaseLoader

# This docstring is CRITICAL. It tells the LLM *when* to use this tool.
@tool
def read_resume_file(file_path: str) -> str:
    """
    Useful for extracting raw text from a candidate's resume PDF file.
    Input should be the valid local file path to the PDF.
    """
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text
    except Exception as e:
        return f"Error reading file: {e}"
    

@tool
def fetch_jd_from_url(url: str) -> str:
    """
    Docstring for fetch_jd_from_url
    Useful for reading a Job Description directly from a web link (URL).
    Input: The full URL string (e.g., 'https://company.com/jobs/123').
    """
    try:
        loader = WebBaseLoader(url)
        docs = loader.load()
        return "\n".join([doc.page_content for doc in docs])
    except Exception as e:
        return f"Error fetching URL: {e}"