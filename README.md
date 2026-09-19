# Enterprise AI Operations Copilot

An enterprise-focused AI assistant that combines **Retrieval-Augmented Generation (RAG)** with **agentic tool calling** to answer internal policy questions and perform operational tasks seamlessly.

## Overview

The Enterprise AI Operations Copilot is a prototype designed to demonstrate how an enterprise AI assistant can:

- Answer questions from internal company documents using RAG.
- Ground responses in retrieved knowledge-base content.
- Create IT support tickets through an AI-selected tool.
- Check the status of existing IT tickets.
- Calculate business expenses with tax.
- Avoid inventing information when the knowledge base does not contain an answer.
- Provide a simple conversational interface through Streamlit.

## Architecture & Tech Stack

This project uses a professional, layered architectural pattern designed for scalability and testing.

- **Orchestration**: LangChain, Python
- **LLM Engine**: Google Gemini API (`gemini-3.6-flash`) via `langchain-google-genai`
- **Vector Database**: ChromaDB (locally persisted)
- **Embeddings**: Hugging Face Sentence Transformers
- **Frontend UI**: Streamlit
- **Testing**: Pytest & Pytest-Mock

```text
                    ┌─────────────────────────┐
                    │       Streamlit UI      │
                    │       Chat Interface    │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │     Agent Orchestrator  │
                    │   Google Gemini + Tools │
                    └────────────┬────────────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
                    ▼                         ▼
             Knowledge Base              Action Tools
                  / RAG                       │
                    │                  ┌──────┼─────────┐
                    ▼                  ▼      ▼         ▼
              ChromaDB             Create   Check    Expense
                    │               Ticket  Status   Calculator
                    ▼
          Hugging Face Embeddings
                    │
                    ▼
          Enterprise Markdown Docs
```

## Project Structure

```text
enterprise-ai-copilot/
│
├── app/
│   ├── agent/          # Orchestrator and logic handling
│   ├── core/           # Configuration, exceptions, and logging
│   ├── knowledge/      # RAG pipeline, loaders, and ChromaDB connection
│   ├── llm/            # LLM initialization and embeddings layer
│   ├── tools/          # IT & Expense standalone tool registry
│   └── ui/             # Streamlit web interface
│
├── data/               # Vectorstore output and raw docs
├── scripts/            # Script to build vectorstore database
├── tests/              # Pytest mocking and validation suite
│
├── .env                # API Keys
├── requirements.txt    # Python dependencies
└── README.md
```

## Setup & Deployment

### 1. Clone the repository

```bash
git clone https://github.com/Alieno1/enterprise-ai-copilot.git
cd enterprise-ai-copilot
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate    # Linux/Mac
# .venv\Scripts\Activate     # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Google API key

Create a `.env` file in the project root:

```text
GOOGLE_API_KEY=your_gemini_api_key_here
```

### 5. Build the vector store

Run the compilation script to chunk and embed all the markdown data:

```bash
python scripts/build_vectorstore.py
```

### 6. Run the application

Ensure your virtual environment is activated and start up Streamlit:

```bash
streamlit run app/ui/app.py
```
Open the local URL shown in the terminal (usually `http://localhost:8501`).

### 7. Run the automated test suite
The infrastructure is heavily tested across 4 domains (Agent, Config, RAG, Tools). Run:

```bash
PYTHONPATH=. pytest tests/
```

## Example Queries

Try asking the assistant these questions once the app is loaded:

- **RAG lookup**: "How many paid annual leave days do employees receive?"
- **IT action**: "My employee ID is EMP123 and my laptop screen cracked. Create a high priority IT ticket."
- **Status check**: "What is the current status of IT-2048-001?"
- **Expense math**: "I spent 2500 on a hotel during a business trip. Calculate the expense with 18 percent tax."
- **Unknown bounds**: "What is the company policy for international business travel reimbursement?" *(The bot will explicitly say it doesn't know rather than hallucinate).*

## Author

**Himanshu Singh**

Computer Science | AI/ML | Generative AI | Agentic AI | Computer Vision

GitHub: https://github.com/Alieno1
