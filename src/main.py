import argparse
from datetime import datetime
from pathlib import Path
from typing import Optional, List

from src.database.database import init_db, get_db, add_trade
from src.parser.trade_parser import TradeParser, FilterMode


def process_file(file_path: Path, date: Optional[datetime] = None, filter_mode: FilterMode = FilterMode.ALL) -> None:
    """Process a trade log file and store the data in the database."""
    parser = TradeParser(filter_mode=filter_mode)
    
    print(f"📂 Reading {file_path}")
    print(f"🔍 Filter mode: {filter_mode.value}")
    
    with open(file_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    
    total_lines = len(lines)
    print(f"📊 Found {total_lines} lines")
    
    trades_processed = 0
    trades_stored = 0
    errors = 0
    
    for i, line in enumerate(lines, 1):
        if i % 100 == 0:
            print(f"🔄 Processing line {i}/{total_lines}")
        
        try:
            trade = parser.parse_line(line)
            if trade:
                trades_processed += 1
                trade_dict = parser.to_dict(trade)
                add_trade(trade_dict)
                trades_stored += 1
                
                # Log the processed trade
                print(f"\n📝 Trade #{trades_processed}:")
                print(f"   ⏰ {trade.timestamp}")
                print(f"   👤 {trade.player_name} ({trade.server})")
                print(f"   🏷️  {trade.trade_type.value}")
                
                if trade.items:
                    print("   📦 Items:")
                    for item in trade.items:
                        item_str = f"      • {item.name}"
                        if item.rarity != "common":
                            item_str += f" [{item.rarity}]"
                        if item.quality_level:
                            item_str += f" QL:{item.quality_level}"
                        if item.damage:
                            item_str += f" DMG:{item.damage}"
                        if item.weight:
                            item_str += f" WT:{item.weight}"
                        if item.fragment:
                            item_str += f" {item.fragment}"
                        print(item_str)
                        if item.attributes:
                            for attr in item.attributes:
                                print(f"        - {attr.name}: {attr.value}")
                
                if trade.price_amount and trade.price_currency:
                    print(f"   💰 Price: {trade.price_amount} {trade.price_currency.value}")
                
                print("   📄 Message:", trade.message)
                print("   " + "─" * 50)
                
        except Exception as e:
            errors += 1
            print(f"❌ Error on line {i}: {str(e)}")
            continue
    
    # Print summary
    print("\n=== Summary ===")
    print(f"📊 Total lines: {total_lines}")
    print(f"📝 Trades processed: {trades_processed}")
    print(f"💾 Trades stored: {trades_stored}")
    print(f"❌ Errors: {errors}")
    print("==============\n")


def main() -> None:
    """Main entry point for the trade data processor."""
    parser = argparse.ArgumentParser(description="Process trade log files")
    parser.add_argument("file", type=Path, help="Path to the trade log file")
    parser.add_argument(
        "--date",
        type=lambda s: datetime.strptime(s, "%Y-%m-%d"),
        help="Date of the log file (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--filter",
        type=str,
        choices=[mode.value for mode in FilterMode],
        default=FilterMode.ALL.value,
        help="Filter mode: all, items_only, or no_items"
    )
    args = parser.parse_args()

    # Initialize database
    init_db()

    # Process file
    process_file(args.file, args.date, FilterMode(args.filter))


if __name__ == "__main__":
    main() 