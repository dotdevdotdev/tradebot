import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple

class TradeParser:
    def __init__(self):
        # Regular expressions for parsing
        self.trade_line_pattern = re.compile(r'\[(\d{2}:\d{2}:\d{2})\] <([^>]+)> \(([^)]+)\) (WTS|WTB|WTT|PC) (.+)')
        self.item_pattern = re.compile(r'\[(common|rare|supreme|fantastic)?\s*([^\]]+?)(?:\s+QL:(\d+\.?\d*))?(?:\s+DMG:(\d+\.?\d*))?(?:\s+WT:(\d+\.?\d*))?(?:\s+([^\]]+))?\]')
        self.attribute_pattern = re.compile(r'(\w+)\s+(\d+)')
        self.price_pattern = re.compile(r'(\d+(?:\.\d+)?)\s*(g|s|c|i)')

    def parse_line(self, line: str) -> Optional[Dict]:
        """Parse a single trade line."""
        match = self.trade_line_pattern.match(line)
        if not match:
            return None

        timestamp, player_name, server, trade_type, message = match.groups()
        
        # Parse timestamp
        try:
            timestamp = datetime.strptime(timestamp, "%H:%M:%S")
        except ValueError:
            return None

        # Parse items and price
        items = self._parse_items(message)
        price_amount, price_currency = self._parse_price(message)

        return {
            "timestamp": timestamp,
            "player_name": player_name,
            "server": server,
            "trade_type": trade_type,
            "message": message,
            "items": items,
            "price_amount": price_amount,
            "price_currency": price_currency
        }

    def _parse_items(self, message: str) -> List[Dict]:
        """Parse items from the message."""
        items = []
        for match in self.item_pattern.finditer(message):
            rarity, name, ql, dmg, wt, attributes = match.groups()
            
            item = {
                "name": name.strip(),
                "rarity": rarity or "common",
                "quality_level": float(ql) if ql else None,
                "damage": float(dmg) if dmg else None,
                "weight": float(wt) if wt else None,
                "attributes": []
            }

            # Parse attributes if present
            if attributes:
                for attr_match in self.attribute_pattern.finditer(attributes):
                    attr_name, attr_value = attr_match.groups()
                    item["attributes"].append({
                        "name": attr_name,
                        "value": attr_value
                    })

            items.append(item)
        return items

    def _parse_price(self, message: str) -> Tuple[Optional[float], Optional[str]]:
        """Parse price from the message."""
        match = self.price_pattern.search(message)
        if not match:
            return None, None

        amount, currency = match.groups()
        currency_map = {
            'g': 'gold',
            's': 'silver',
            'c': 'copper',
            'i': 'iron'
        }
        return float(amount), currency_map.get(currency) 