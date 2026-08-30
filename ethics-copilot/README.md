# Ethics Copilot

An AI-powered assistant for navigating the company's Code of Ethics using RAG + MCP.

## Technology Stack

- **LLM**: Google Gemini (via Google AI Studio)
- **RAG**: ChromaDB + Sentence Transformers
- **MCP**: MCP Python SDK
- **Backend**: FastAPI
- **UI**: Streamlit
- **External Systems**: Case API (FastAPI + SQLite), Microsoft Graph (Outlook)

## Setup

### Prerequisites

- Python 3.10+
- Gemini API key from Google AI Studio
- Microsoft Graph app registration (for Outlook)

### Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt