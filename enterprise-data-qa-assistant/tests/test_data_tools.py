import sqlite3
import pytest
from app import data_tools

@pytest.fixture
def sample_db(tmp_path, monkeypatch):
    path = tmp_path / "test.db"
    with sqlite3.connect(path) as conn:
        conn.execute("CREATE TABLE sales (id INTEGER, amount REAL)")
        conn.executemany("INSERT INTO sales VALUES (?, ?)", [(1, 10), (2, 20)])
    monkeypatch.setattr(data_tools, "DB_PATH", path)
    return path

def test_select_query_returns_rows(sample_db):
    result = data_tools.run_readonly_query("SELECT * FROM sales ORDER BY id")
    assert result["row_count_returned"] == 2
    assert result["rows"][0]["amount"] == 10

@pytest.mark.parametrize("query", [
    "DELETE FROM sales",
    "DROP TABLE sales",
    "UPDATE sales SET amount=0",
    "INSERT INTO sales VALUES (3, 30)",
])
def test_write_queries_are_rejected(sample_db, query):
    with pytest.raises(ValueError):
        data_tools.run_readonly_query(query)

def test_multiple_statements_are_rejected(sample_db):
    with pytest.raises(ValueError):
        data_tools.run_readonly_query("SELECT * FROM sales; DROP TABLE sales")

def test_empty_query_is_rejected(sample_db):
    with pytest.raises(ValueError):
        data_tools.run_readonly_query(" ")
