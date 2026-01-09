# LLM Based Recruitment Agent

This project implements an autonomous agent that automates the candidate resume screening process. It uses **LangChain** and **claude-sonnet-4-5-20250929** to read a resume (PDF), fetch a Job Description (URL), and generate a structured JSON file.

## Architecture
The agent utilizes the **ReAct (Reasoning + Acting)** pattern:
1.  **Tools:**
    * `read_resume_file`: Uses `pdfplumber` to extract text from local PDFs.
    * `fetch_jd_from_url`: Uses `WebBaseLoader` to scrape Job Descriptions from live URLs.

2.  **Logic:** The LLM decides which tools to call, processes the text, and evaluates the candidate.

3.  **Output:** Enforces a strict Pydantic schema to produce valid JSON and prints on the console.

## Setup & Usage

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Environment Variables:**
    Create a `.env` file and add your Anthropic API key:
    ```bash
    ANTHROPIC_API_KEY=<your_api_key>
    ```
    For Conda Environment, type the following command in your virtual env terminal
    ```bash
    conda env config vars set ANTHROPIC_API_KEY=<your_api_key>
    ```

4.  **Run the Agent:**
    ```bash
    python main.py --resume_path "./my_resume.pdf" --job_url "[https://jobs.apple.com/](https://jobs.apple.com/)..."
    ```
      or
      ```
      python main.py
      ```

## 📝 Assumptions
1.  **Resume Format:** Assumes the PDF contains selectable text (not a scanned image).
2.  **JD Accessibility:** Assumes the Job URL is accessible via a standard GET request (not behind a login wall or captcha).
3.  **LLM Model:** Uses `claude-3-5-sonnet-latest` for high-reasoning capability.

## Output
The script saves a `candidate.json` file in the root directory:
```json
{
  "name": "Jane Doe",
  "contact": {
    "Phone": 7827787045,
    "email": "janedoe@gmail.com",
    "address": "Toronto, Ontario"
  },
  "skills": ["python", "C++"],
  "experience": [......, .......],
  "education": [......, ........],
  "score": 88.5,
}
