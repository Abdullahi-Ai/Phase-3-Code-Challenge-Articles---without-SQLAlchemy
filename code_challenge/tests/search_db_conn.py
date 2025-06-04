import sqlite3
import os

def get_connection():
    """
    Returns a new SQLite3 connection to the database file.

    Make sure to adjust the database filename/path below
    to match your actual SQLite database file.
    """
    # Path to your SQLite database file (change if needed)
    db_path = os.path.join(os.path.dirname(__file__), "test.db")

    # Create and return a new connection
    return sqlite3.connect(db_path)
