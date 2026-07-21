#!/usr/bin/env python3
"""Read-only search over Lengmo's local Claude session archive."""

from __future__ import annotations

import argparse
import json
import os
import sqlite3
from pathlib import Path


DEFAULT_DB = Path.home() / "Desktop/cc-memory/memory/data/memory.db"


def connect() -> sqlite3.Connection:
    db_path = Path(os.environ.get("CLAUDE_MEMORY_DB", DEFAULT_DB)).expanduser().resolve()
    if not db_path.is_file():
        raise SystemExit(f"Memory database not found: {db_path}")
    connection = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    return connection


def print_json(rows: list[sqlite3.Row]) -> None:
    print(json.dumps([dict(row) for row in rows], ensure_ascii=False, indent=2))


def search(connection: sqlite3.Connection, query: str, limit: int) -> None:
    sql = """
        SELECT
            s.id AS session_id,
            s.started_at,
            s.title,
            s.project_path,
            snippet(messages_fts, 0, '[', ']', ' … ', 28) AS snippet
        FROM messages_fts
        JOIN messages AS m ON m.id = messages_fts.rowid
        JOIN sessions AS s ON s.id = m.session_id
        WHERE messages_fts MATCH ?
        ORDER BY bm25(messages_fts), s.started_at DESC
        LIMIT ?
    """
    try:
        rows = connection.execute(sql, (query, limit)).fetchall()
    except sqlite3.OperationalError:
        phrase = '"' + query.replace('"', '""') + '"'
        rows = connection.execute(sql, (phrase, limit)).fetchall()
    print_json(rows)


def session(connection: sqlite3.Connection, session_id: str, limit: int) -> None:
    selected = connection.execute(
        """
        SELECT id, started_at, title, project_path
        FROM sessions
        WHERE id = ?
        """,
        (session_id,),
    ).fetchone()
    if selected is None:
        raise SystemExit("Session not found.")

    rows = connection.execute(
        """
        SELECT role, timestamp, substr(content, 1, 4000) AS content
        FROM messages
        WHERE session_id = ?
        ORDER BY id
        LIMIT ?
        """,
        (session_id, limit),
    ).fetchall()
    payload = {"session": dict(selected), "messages": [dict(row) for row in rows]}
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    search_parser = subparsers.add_parser("search")
    search_parser.add_argument("query")
    search_parser.add_argument("--limit", type=int, default=8, choices=range(1, 51))

    session_parser = subparsers.add_parser("session")
    session_parser.add_argument("session_id")
    session_parser.add_argument("--limit", type=int, default=40, choices=range(1, 201))

    args = parser.parse_args()
    with connect() as connection:
        if args.command == "search":
            search(connection, args.query, args.limit)
        else:
            session(connection, args.session_id, args.limit)


if __name__ == "__main__":
    main()
