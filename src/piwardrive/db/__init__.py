"""Database abstraction layer with multiple backends."""

from .adapter import DatabaseAdapter
from .manager import DatabaseManager
from .mysql import MySQLAdapter
from .postgres import PostgresAdapter
from .sqlite import SQLiteAdapter

__all__ = [
    "DatabaseAdapter",
    "SQLiteAdapter",
    "PostgresAdapter",
    "MySQLAdapter",
    "DatabaseManager",
]
