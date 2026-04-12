"""
Seed the instruments table with the canonical instrument list.
Idempotent — safe to run multiple times (uses ON CONFLICT DO NOTHING).

Usage (from backend/):
    python scripts/seed_instruments.py
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from app.core.database import engine

INSTRUMENTS = [
    # Commodities
    ("XAUUSD", "Gold / US Dollar",                    "commodity", True),
    ("USOIL",  "US Crude Oil",                        "commodity", True),
    # Major forex pairs
    ("EURUSD", "Euro / US Dollar",                    "forex",     True),
    ("GBPUSD", "British Pound / US Dollar",           "forex",     True),
    ("USDJPY", "US Dollar / Japanese Yen",            "forex",     True),
    ("USDCHF", "US Dollar / Swiss Franc",             "forex",     True),
    ("AUDUSD", "Australian Dollar / US Dollar",       "forex",     True),
    ("NZDUSD", "New Zealand Dollar / US Dollar",      "forex",     True),
    ("USDCAD", "US Dollar / Canadian Dollar",         "forex",     True),
    # Crosses
    ("EURGBP", "Euro / British Pound",                "forex",     True),
    ("EURJPY", "Euro / Japanese Yen",                 "forex",     True),
    ("GBPJPY", "British Pound / Japanese Yen",        "forex",     True),
]


def seed() -> None:
    stmt = text(
        """
        INSERT INTO instruments (symbol, name, asset_class, is_active)
        VALUES (:symbol, :name, :asset_class, :is_active)
        ON CONFLICT (symbol) DO NOTHING
        """
    )
    rows = [
        {"symbol": sym, "name": name, "asset_class": asset_class, "is_active": is_active}
        for sym, name, asset_class, is_active in INSTRUMENTS
    ]

    with engine.begin() as conn:
        result = conn.execute(stmt, rows)

    inserted = result.rowcount
    skipped = len(INSTRUMENTS) - inserted
    print(f"Seeded instruments: {inserted} inserted, {skipped} already existed.")


if __name__ == "__main__":
    seed()
