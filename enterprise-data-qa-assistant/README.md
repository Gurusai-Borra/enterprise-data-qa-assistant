# Enterprise Data Q&A Assistant using LangChain and MCP

An AI-powered assistant that lets non-technical users ask natural-language questions about enterprise data stored in SQLite and CSV files.

## Features

- LangChain agent with tools for database queries and CSV summaries.
- MCP server exposing the same data operations as reusable tools.
- FastAPI endpoint for application integration.
- Read-only SQLite connections and SQL validation.
- Input length validation and audit logging.
- Sample sales database and employee CSV.
- pytest tests for data access and API validation.

## Architecture

User question -> FastAPI -> LangChain agent -> tools -> SQLite / CSV -> natural-language answer.

The standalone MCP server exposes `query_database` and `summarize_csv_file` over the Model Context Protocol. The FastAPI/LangChain path uses the same underlying Python tool functions. This keeps the example modular; the API does not currently act as an MCP client.

## Tech stack

Python, LangChain, Model Context Protocol (MCP), FastAPI, SQLite, CSV, pytest.

## Project structure

```text
enterprise-data-qa-assistant/
├── app/
│   ├── __init__.py
│   ├── agent.py
│   ├── config.py
│   ├── data_tools.py
│   └── main.py
├── data/
│   ├── employees.csv
│   └── enterprise.db
├── scripts/
│   └── seed_database.py
├── tests/
│   ├── test_api.py
│   └── test_data_tools.py
├── .env.example
├── .gitignore
├── mcp_server.py
├── requirements.txt
└── README.md
```

## Setup

Python 3.10+ is recommended.

1. Clone the repository:

   ```bash
   git clone https://github.com/YOUR-USERNAME/enterprise-data-qa-assistant.git
   cd enterprise-data-qa-assistant
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # macOS/Linux:
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure the API key:

   ```bash
   cp .env.example .env
   ```

   Add your OpenAI API key to `.env`. Never commit `.env` or expose your key.

5. Create the sample database:

   ```bash
   python scripts/seed_database.py
   ```

   A sample SQLite database is included, but you can regenerate it with this command.

## Run the FastAPI application

```bash
uvicorn app.main:app --reload
```

Open the interactive API documentation at:

`http://127.0.0.1:8000/docs`

Example request:

```bash
curl -X POST "http://127.0.0.1:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question":"What are total sales by region?"}'
```

Other example questions:

- What is the total sales amount?
- Which product generated the highest revenue?
- Show sales records from the South region.
- Summarize the employee CSV.
- How many employees are in the Engineering department?

## Run the MCP server

```bash
python mcp_server.py
```

The server uses stdio transport by default. Configure it in an MCP-compatible client using the absolute path to your Python interpreter and `mcp_server.py`. For example, a local MCP client configuration can launch:

```json
{
  "mcpServers": {
    "enterprise-data": {
      "command": "/absolute/path/to/.venv/bin/python",
      "args": ["/absolute/path/to/enterprise-data-qa-assistant/mcp_server.py"]
    }
  }
}
```

On Windows, use the virtual environment's `Scripts/python.exe` path.

## Run tests

```bash
pytest -v
```

The test suite checks successful read-only queries, rejection of write operations, rejection of multiple SQL statements, and API validation. Tests do not require an OpenAI API key.

## Security and responsible AI

- SQLite is opened in read-only URI mode.
- SQL validation rejects common write and schema-changing operations.
- Only one SQL statement is accepted.
- Query results are capped at 200 rows.
- API input is limited to 4,000 characters.
- Prompt and response audit logging is enabled.

Important: this is an educational portfolio implementation, not a production security boundary. SQL keyword validation is not a complete SQL parser or authorization system. For production, use a dedicated read-only database account, strict table/column allowlists, query timeouts, access control, PII redaction, secret management, and structured audit retention. Avoid logging sensitive prompts or results.

## Current limitations

- The sample data is synthetic.
- The assistant requires an OpenAI API key to generate natural-language answers.
- CSV support currently provides metadata and a preview, not semantic retrieval over arbitrary large documents.
- The MCP server is independently runnable; the FastAPI agent currently calls shared Python tools directly rather than connecting to the MCP server as a client.
- No authentication or multi-tenant access control is included.

## Future improvements

- Add an MCP client connection inside the LangChain application.
- Add embeddings and a vector database for semantic retrieval over PDF/DOCX/CSV documents.
- Add user authentication and role-based access control.
- Add conversation memory with per-user session isolation.
- Add Docker deployment and CI with GitHub Actions.

## License

MIT
