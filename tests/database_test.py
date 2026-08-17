from pathlib import Path

from src.database.database import (
    DATABASE_PATH,
    get_connection,
    initialize_database,
)


def test_database_initialization():
    initialize_database()

    assert DATABASE_PATH.exists()

    with get_connection() as connection:
        table = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            AND name = 'telemetry'
            """
        ).fetchone()

    assert table is not None
