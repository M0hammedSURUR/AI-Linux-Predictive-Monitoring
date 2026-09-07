from datetime import datetime, timezone
from pathlib import Path
import sqlite3

from src.database.database import get_connection
from src.prediction.models import PredictionResult


class PredictionRepository:
    """Provides persistence operations for prediction results."""

    def __init__(self, database_path: Path | None = None):
        self.database_path = database_path

    def save(self, prediction: PredictionResult) -> None:
        """Store one prediction result in the database."""

        query = """
        INSERT INTO prediction_events (
            timestamp,
            metric,
            current_value,
            predicted_value,
            threshold,
            risk_level,
            message,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """

        # NEW: Record when the prediction was persisted
        created_at = datetime.now(timezone.utc).isoformat()

        values = (
            prediction.timestamp.isoformat(),
            prediction.metric,
            prediction.current_value,
            prediction.predicted_value,
            prediction.threshold,
            prediction.risk_level,
            prediction.message,
            created_at,
        )

        if self.database_path is None:
            with get_connection() as connection:
                connection.execute(query, values)
                connection.commit()
            return

        with sqlite3.connect(self.database_path) as connection:
            connection.execute(query, values)
            connection.commit()

    def get_all(self) -> list[PredictionResult]:
        """Load all prediction results from the database."""

        query = """
        SELECT
            timestamp,
            metric,
            current_value,
            predicted_value,
            threshold,
            risk_level,
            message
        FROM prediction_events
        ORDER BY timestamp
        """

        if self.database_path is None:
            with get_connection() as connection:
                rows = connection.execute(query).fetchall()
        else:
            with sqlite3.connect(self.database_path) as connection:
                connection.row_factory = sqlite3.Row
                rows = connection.execute(query).fetchall()

        return [
            PredictionResult(
                timestamp=datetime.fromisoformat(row["timestamp"]),
                metric=row["metric"],
                current_value=row["current_value"],
                predicted_value=row["predicted_value"],
                threshold=row["threshold"],
                risk_level=row["risk_level"],
                message=row["message"],
            )
            for row in rows
        ]
