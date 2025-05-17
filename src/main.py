import argparse
from datetime import datetime
from pathlib import Path
from typing import Optional

from src.database.database import init_db, get_db, add_trade
from src.parser.parser import TradeParser


def process_file(file_path: Path, date: Optional[datetime] = None) -> None:
    """Process a trade log file and store the data in the database."""
    parser = TradeParser()
    
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Parse the line
            trade_data = parser.parse_line(line)
            if not trade_data:
                continue

            # Add date to timestamp if not present
            if date and not isinstance(trade_data["timestamp"], datetime):
                trade_data["timestamp"] = datetime.combine(
                    date.date(), trade_data["timestamp"].time()
                )

            # Store in database
            with get_db() as db:
                add_trade(db, trade_data)


def main() -> None:
    """Main entry point for the trade data processor."""
    parser = argparse.ArgumentParser(description="Process trade log files")
    parser.add_argument("file", type=Path, help="Path to the trade log file")
    parser.add_argument(
        "--date",
        type=lambda s: datetime.strptime(s, "%Y-%m-%d"),
        help="Date of the log file (YYYY-MM-DD)",
    )
    args = parser.parse_args()

    # Initialize database
    init_db()

    # Process file
    process_file(args.file, args.date)


if __name__ == "__main__":
    main() 