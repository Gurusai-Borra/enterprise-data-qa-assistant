import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
db = DATA / "enterprise.db"

with sqlite3.connect(db) as conn:
    conn.execute("""CREATE TABLE IF NOT EXISTS sales (
        sale_id INTEGER PRIMARY KEY,
        employee_id INTEGER,
        region TEXT,
        product TEXT,
        amount REAL,
        sale_date TEXT
    )""")
    conn.execute("DELETE FROM sales")
    conn.executemany(
        "INSERT INTO sales(employee_id, region, product, amount, sale_date) VALUES(?,?,?,?,?)",
        [
            (101, "South", "Laptop", 65000, "2026-01-12"),
            (102, "North", "Monitor", 18000, "2026-01-15"),
            (103, "West", "Laptop", 72000, "2026-02-02"),
            (104, "South", "Keyboard", 2500, "2026-02-11"),
            (101, "East", "Monitor", 19500, "2026-03-05"),
            (105, "North", "Laptop", 68000, "2026-03-18"),
        ],
    )
print(f"Seeded database: {db}")
