"""MCP server exposing the same read-only data tools."""
from mcp.server.fastmcp import FastMCP
from app.data_tools import run_readonly_query, summarize_csv

mcp = FastMCP("enterprise-data-assistant")

@mcp.tool()
def query_database(sql: str) -> dict:
    """Run a read-only SQL query against the enterprise SQLite database."""
    return run_readonly_query(sql)

@mcp.tool()
def summarize_csv_file() -> dict:
    """Summarize the configured CSV file and return a five-row preview."""
    return summarize_csv()

if __name__ == "__main__":
    mcp.run()
