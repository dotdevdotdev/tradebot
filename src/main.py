import argparse
from datetime import datetime
from pathlib import Path
from typing import Optional, List
import csv
import io

from src.database.database import init_db, get_db, add_trade
from src.parser.parser import TradeParser
from src.llm.claude_client import ClaudeClient
from src.llm.prompt_utils import read_prompt_template, format_prompt


def chunk_data(data: List[str], chunk_size: int = 10) -> List[List[str]]:
    """Split data into chunks of specified size."""
    return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]


def parse_csv_response(csv_text: str) -> List[dict]:
    """Parse a multi-line CSV response into a list of dictionaries."""
    reader = csv.DictReader(io.StringIO(csv_text.strip()))
    return list(reader)


def process_file(file_path: Path, date: Optional[datetime] = None) -> None:
    """Process a trade log file and store the data in the database."""
    parser = TradeParser()
    claude = ClaudeClient()
    prompt_template = read_prompt_template()
    
    with open(file_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    
    # Chunk the data into reasonable sizes
    chunks = chunk_data(lines, chunk_size=10)
    
    for chunk in chunks:
        # Parse each line in the chunk
        trade_data_list = []
        for line in chunk:
            trade_data = parser.parse_line(line)
            print(trade_data)
            # if trade_data:
            #     # Add date to timestamp if not present
            #     if date and not isinstance(trade_data["timestamp"], datetime):
            #         trade_data["timestamp"] = datetime.combine(
            #             date.date(), trade_data["timestamp"].time()
            #         )
            #     trade_data_list.append(trade_data)
        
        if not trade_data_list:
            continue
        
        # Format prompt with the chunk of trade data
        prompt = format_prompt(prompt_template, {"trades": trade_data_list})
        llm_response = claude.complete(prompt)
        
        # Parse CSV response
        try:
            structured_data = parse_csv_response(llm_response)
        except Exception as e:
            print(f"Failed to parse CSV from LLM: {llm_response}\nError: {e}")
            continue
        
        # Store structured data in database
        for data in structured_data:
            add_trade(data)


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