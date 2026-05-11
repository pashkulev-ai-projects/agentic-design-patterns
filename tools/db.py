from pathlib import Path
from agents import function_tool
import sqlite3


MEMORY_DB = Path(__file__).parent.parent / "memory_demo.db"


def _init_db() -> sqlite3.Connection:
    conn = sqlite3.connect(MEMORY_DB, timeout=5, isolation_level=None, check_same_thread=False)
    conn.execute("CREATE TABLE IF NOT EXISTS memory (key TEXT PRIMARY KEY, value TEXT)")
    return conn


_db = _init_db()
_db.execute("DELETE FROM memory")


@function_tool
async def remember(key: str, value: str) -> str:
    """Store a fact about the user persistently for future sessions."""
    _db.execute("INSERT OR REPLACE INTO memory VALUES (?, ?)", (key, value))
    return f"Stored: {key} = {value}"


@function_tool
async def recall_all() -> str:
    """Retrieve all stored facts about the user."""
    rows = _db.execute("SELECT key, value FROM memory").fetchall()
    return "\n".join(f"{k}: {v}" for k, v in rows) if rows else "No memories yet."