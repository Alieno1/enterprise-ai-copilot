# Enterprise AI Operations Copilot

Welcome to the **Enterprise AI Operations Copilot**! This is a smart, enterprise-ready AI assistant that acts as a virtual IT and HR helper. 

It handles everything from answering questions based on your company's internal documents to performing real actions (like calculating expenses or raising IT support tickets) all through a friendly chat interface.

---

## What Does It Do?

- **Reads Company Policies:** It securely reads your internal markdown documents and answers questions based *only* on that verified info.
- **Calculates Expenses:** You can ask it to calculate travel expenses with tax, and it uses a built-in calculator tool mathematically.
- **IT Support:** It can automatically generate IT support tickets and look up ticket statuses for employees.
- **No Hallucinations:** If it doesn't know the answer, it tells you, instead of making things up!

---

## How It Works (The Tech Stack)

This project is built using modern, industry-standard AI tools:
- **Google Gemini** (`gemini-3.6-flash`) for the core brain and tool-calling.
- **LangChain** for orchestrating the AI logic and tools.
- **ChromaDB & Hugging Face** for securely storing and searching your company documents locally.
- **Streamlit** for the beautiful, easy-to-use web chat interface.
- **Pytest** for running automated unit tests on the code to ensure it's bug-free.

---

## Quickstart: How to Run This Project

Follow these exact steps to get the AI Copilot running on your local machine in less than 2 minutes!

### Step 1: Download the Code
Open your terminal and clone this repository down to your computer:
```bash
git clone https://github.com/Alieno1/enterprise-ai-copilot.git
cd enterprise-ai-copilot
```

### Step 2: Set Up the Environment
Create an isolated Python environment so it doesn't interfere with your computer:
```bash
python -m venv .venv
source .venv/bin/activate    # (If you are on Windows, run: .venv\Scripts\Activate)
```

### Step 3: Install Requirements
Install all the AI and web frameworks we need:
```bash
pip install -r requirements.txt
```

### Step 4: Add Your Google API Key
Create a new file named `.env` in the main folder and paste your Google Gemini API Key inside it like this:
```text
GOOGLE_API_KEY=your_gemini_api_key_here
```
*(Need a key? Get one for free at https://aistudio.google.com/app/apikey)*

### Step 5: Build the Copilot's Brain
Run this script to let the AI read, chunk, and index the sample company documents:
```bash
python scripts/build_vectorstore.py
```

### Step 6: Launch the App
Start up the web interface:
```bash
streamlit run app/ui/app.py
```
Click the link it gives you (usually `http://localhost:8501`) and start chatting!

---

## Testing the AI (For Developers)
Want to inspect the logic under the hood? The project is fully tested. Just run:
```bash
PYTHONPATH=. pytest tests/
```

## Author
**Himanshu Singh**  
*Computer Science | AI/ML | Generative AI | Agentic AI | Computer Vision | Backend Engineer | Spring Boot | Distributed Systems*  
GitHub: [Alieno1](https://github.com/Alieno1)
