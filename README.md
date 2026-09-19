# Enterprise AI Operations Copilot

An enterprise-focused AI assistant that combines **Retrieval-Augmented Generation (RAG)** with **agentic tool calling** to answer internal policy questions and perform operational tasks.

## Overview

The Enterprise AI Operations Copilot is a prototype designed to demonstrate how an enterprise AI assistant can:

- Answer questions from internal company documents using RAG.
- Ground responses in retrieved knowledge-base content.
- Create IT support tickets through an AI-selected tool.
- Check the status of existing IT tickets.
- Calculate business expenses with tax.
- Avoid inventing information when the knowledge base does not contain an answer.
- Provide a simple conversational interface through Streamlit.

The enterprise documents and operational tools in this project are **synthetic/demo data** intended for demonstration purposes.

## Architecture

```text
                    ┌─────────────────────────┐
                    │       Streamlit UI      │
                    │       Chat Interface    │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │     Agent / LLM Layer   │
                    │   OpenRouter + LangChain│
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

## RAG Pipeline

The knowledge-base workflow follows:

```text
Enterprise Documents
        ↓
Document Loading
        ↓
Recursive Chunking
        ↓
Hugging Face Embeddings
        ↓
ChromaDB Vector Store
        ↓
Similarity Search
        ↓
Retrieved Context
        ↓
LLM
        ↓
Grounded Answer + Sources
```

The assistant is instructed to avoid fabricating policies when the requested information is not present in the knowledge base.

## Agentic Workflow

The LLM is provided with several tools and decides which tool is appropriate based on the user's request.

### Available tools

#### `create_it_ticket`

Creates a demo IT support ticket using:

- Employee ID
- Issue description
- Priority

Example:

```text
My employee ID is EMP3050 and my laptop is completely broken.
Create a high priority IT ticket.
```

#### `check_ticket_status`

Checks the status of a demo IT ticket.

Example:

```text
What is the current status of IT-2048-001?
```

#### `calculate_expense`

Calculates an expense including a percentage-based tax.

Example:

```text
I spent 2500 on a hotel during a business trip.
Calculate the expense with 18 percent tax.
```

#### `search_knowledge_base`

Searches the enterprise knowledge base and returns an answer grounded in the indexed company documents.

## Tech Stack

- **Python**
- **LangChain**
- **OpenRouter**
- **Hugging Face Sentence Transformers**
- **ChromaDB**
- **Streamlit**
- **python-dotenv**
- **Git / GitHub**

## Project Structure

```text
enterprise-ai-copilot/
│
├── app/
│   ├── __init__.py
│   ├── agent.py
│   ├── config.py
│   ├── embeddings.py
│   ├── llm.py
│   ├── loader.py
│   ├── rag.py
│   ├── splitting.py
│   ├── tools.py
│   ├── ui.py
│   └── vectorstore.py
│
├── data/
│   └── documents/
│       ├── hr_policy.md
│       └── it_support.md
│
├── test_llm.py
├── .gitignore
└── README.md
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Alieno1/enterprise-ai-copilot.git
cd enterprise-ai-copilot
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

Install the required packages used by the project:

```powershell
python -m pip install langchain langchain-openai langchain-community langchain-chroma langchain-huggingface sentence-transformers chromadb python-dotenv streamlit
```

### 4. Configure the API key

Create a `.env` file in the project root:

```text
OPENROUTER_API_KEY=your_api_key_here
```

The `.env` file is excluded from Git through `.gitignore`.

### 5. Build the vector store

```powershell
python -c "from app.vectorstore import build_vectorstore; build_vectorstore(); print('Vector store built successfully.')"
```

### 6. Run the application

```powershell
python -m streamlit run app/ui.py
```

Then open the local Streamlit URL shown in the terminal, normally:

```text
http://localhost:8501
```

## Example Queries

### Knowledge-base question

```text
How many paid annual leave days do employees receive?
```

Expected knowledge-base answer:

```text
Employees receive 18 days of paid annual leave per calendar year.
```

### IT support policy

```text
What are the standard IT support hours?
```

### IT ticket creation

```text
My employee ID is EMP3050 and my laptop is completely broken.
Create a high priority IT ticket.
```

### Ticket status

```text
What is the current status of IT-2048-001?
```

### Expense calculation

```text
I spent 2500 on a hotel during a business trip.
Calculate the expense with 18 percent tax.
```

### Unknown information

```text
What is the company policy for international business travel reimbursement?
```

The assistant should indicate that the available knowledge base does not contain the requested information rather than inventing a policy.

## Design Considerations

### Grounded generation

The RAG component explicitly instructs the LLM to use the retrieved enterprise context and avoid inventing policies.

### Tool determinism

Operational tools such as ticket creation, ticket status, and expense calculation return their tool results directly. This prevents the final LLM response from adding unsupported operational claims.

### Local vector storage

ChromaDB is persisted locally under:

```text
data/chroma/
```

This generated directory is excluded from Git because it can be rebuilt from the source documents.

## Limitations

This is a prototype and uses synthetic enterprise data.

- IT ticket operations are simulated rather than connected to a real ITSM platform.
- Ticket data is stored in demo/static structures.
- The knowledge base contains only a small set of example documents.
- Authentication and authorization are not implemented.
- Production monitoring, evaluation, and observability are not included.
- The application is not designed to process confidential enterprise data in its current form.

## Future Improvements

Potential extensions include:

- Integration with ServiceNow or another ITSM platform.
- Enterprise authentication and role-based access control.
- Larger document collections and metadata filtering.
- Hybrid search combining keyword and semantic retrieval.
- Reranking for improved retrieval accuracy.
- Conversation memory.
- Structured tool execution and approval workflows.
- Automated RAG evaluation.
- LangSmith or equivalent observability.
- Docker-based deployment.
- Cloud deployment with managed vector databases.
- Guardrails and enterprise security controls.

## Author

**Himanshu Singh**

Computer Science | AI/ML | Generative AI | Agentic AI | Computer Vision

GitHub: https://github.com/Alieno1
