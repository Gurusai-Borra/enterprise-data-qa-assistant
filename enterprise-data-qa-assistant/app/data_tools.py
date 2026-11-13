"""Read-only tools shared by the API, LangChain agent, and MCP server."""
import csv
import sqlite3
from pathlib import Path
from typing import Any
from app.config import DB_PATH, CSV_PATH

ALLOWED_PREFIXES = ("SELECT", "WITH", "PRAGMA")

def run_readonly_query(query: str) -> dict[str, Any]:
    """Run one read-only SQL statement against the local SQLite database."""
    cleaned = query.strip()
    if not cleaned:
        raise ValueError("SQL query cannot be empty.")
    if ";" in cleaned.rstrip(";"):
        raise ValueError("Only one SQL statement is allowed.")
    normalized = cleaned.upper()
    if not normalized.startswith(ALLOWED_PREFIXES):
        raise ValueError("Only SELECT, WITH, and PRAGMA statements are permitted.")
    forbidden = ("INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE",
                 "ATTACH", "DETACH", "REPLACE", "VACUUM")
    padded = " " + normalized.replace("\n", " ") + " "
    if any(f" {word} " in padded for word in forbidden):
        raise ValueError("Write or schema-changing SQL is not permitted.")

    db_file = Path(DB_PATH)
    if not db_file.exists():
        raise FileNotFoundError(f"Database not found: {db_file}")
    connection = sqlite3.connect(f"file:{db_file}?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    try:
        cursor = connection.execute(cleaned)
        rows = [dict(row) for row in cursor.fetchmany(200)]
        return {"columns": [item[0] for item in cursor.description or []],
                "rows": rows, "row_count_returned": len(rows),
                "max_rows": 200}
    finally:
        connection.close()

def summarize_csv() -> dict[str, Any]:
    """Return basic metadata and a small preview of the configured CSV."""
    path = Path(CSV_PATH)
    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
    columns = reader.fieldnames or []
    return {
        "file": path.name,
        "row_count": len(rows),
        "columns": columns,
        "preview": rows[:5],
    }
