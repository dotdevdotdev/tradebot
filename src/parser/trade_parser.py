import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class TradeType(str, Enum):
    WTS = "WTS"
    WTB = "WTB"
    WTT = "WTT"
    PC = "PC"

class Rarity(str, Enum):
    COMMON = "common"
    RARE = "rare"
    SUPREME = "supreme"
    FANTASTIC = "fantastic"

class Currency(str, Enum):
    IRON = "iron"
    COPPER = "copper"
    SILVER = "silver"
    GOLD = "gold"

class FilterMode(str, Enum):
    ALL = "all"  # Process all messages
    ITEMS_ONLY = "items_only"  # Only messages with item links
    NO_ITEMS = "no_items"  # Only messages without item links

@dataclass
class ItemAttribute:
    name: str
    value: str

@dataclass
class Item:
    name: str
    rarity: Rarity
    quality_level: Optional[float]
    weight: Optional[float]
    damage: Optional[float]
    attributes: List[ItemAttribute]
    fragment: Optional[str] = None

@dataclass
class Trade:
    timestamp: str
    player_name: str
    server: str
    trade_type: TradeType
    message: str
    items: List[Item]
    price_amount: Optional[float]
    price_currency: Optional[Currency]

class TradeParser:
    def __init__(self, filter_mode: FilterMode = FilterMode.ALL):
        # Regular expressions for parsing
        self.trade_line_pattern = re.compile(r'\[(\d{2}:\d{2}:\d{2})\] <([^>]+)> \(([^)]+)\) (WTS|WTB|WTT|PC) (.+)')
        self.item_pattern = re.compile(r'\[(common|rare|supreme|fantastic)?\s*([^\]]+?)(?:\s+QL:(\d+\.?\d*))?(?:\s+DMG:(\d+\.?\d*))?(?:\s+WT:(\d+\.?\d*))?(?:\s+([^\]]+))?\]')
        self.attribute_pattern = re.compile(r'(\w+)\s+(\d+)')
        self.price_pattern = re.compile(r'(\d+(?:\.\d+)?)\s*(g|s|c|i)')
        self.fragment_pattern = re.compile(r'\[(\d+)/(\d+)\]')
        
        # Server name mapping
        self.server_map = {
            'Har': 'Harmony',
            'Mel': 'Melody',
            'Cad': 'Cadence'
        }
        
        self.filter_mode = filter_mode

    def parse_line(self, line: str) -> Optional[Trade]:
        """Parse a single trade line into a Trade object."""
        match = self.trade_line_pattern.match(line)
        if not match:
            return None

        timestamp, player_name, server, trade_type, message = match.groups()
        
        # Parse items and price
        items = self._parse_items(message)
        price_amount, price_currency = self._parse_price(message)

        # Apply filtering
        if self.filter_mode == FilterMode.ITEMS_ONLY and not items:
            return None
        if self.filter_mode == FilterMode.NO_ITEMS and items:
            return None

        return Trade(
            timestamp=timestamp,
            player_name=player_name,
            server=self.server_map.get(server, server),
            trade_type=TradeType(trade_type),
            message=message,
            items=items,
            price_amount=price_amount,
            price_currency=Currency(price_currency) if price_currency else None
        )

    def _parse_items(self, message: str) -> List[Item]:
        """Parse items from the message."""
        items = []
        for match in self.item_pattern.finditer(message):
            rarity, name, ql, dmg, wt, attributes = match.groups()
            
            # Parse fragment if present
            fragment = None
            fragment_match = self.fragment_pattern.search(name)
            if fragment_match:
                fragment = f"{fragment_match.group(1)}/{fragment_match.group(2)}"
                name = name[:fragment_match.start()].strip()

            # Parse attributes
            item_attributes = []
            if attributes:
                for attr_match in self.attribute_pattern.finditer(attributes):
                    attr_name, attr_value = attr_match.groups()
                    item_attributes.append(ItemAttribute(
                        name=attr_name,
                        value=attr_value
                    ))

            items.append(Item(
                name=name.strip(),
                rarity=Rarity(rarity or "common"),
                quality_level=float(ql) if ql else None,
                weight=float(wt) if wt else None,
                damage=float(dmg) if dmg else None,
                attributes=item_attributes,
                fragment=fragment
            ))
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

    def to_dict(self, trade: Trade) -> Dict:
        """Convert a Trade object to a dictionary format suitable for database storage."""
        return {
            "timestamp": trade.timestamp,
            "player_name": trade.player_name,
            "server": trade.server,
            "trade_type": trade.trade_type.value,
            "message": trade.message,
            "items": [
                {
                    "name": item.name,
                    "rarity": item.rarity.value,
                    "quality_level": item.quality_level,
                    "weight": item.weight,
                    "damage": item.damage,
                    "attributes": [
                        {"name": attr.name, "value": attr.value}
                        for attr in item.attributes
                    ],
                    "fragment": item.fragment
                }
                for item in trade.items
            ],
            "price_amount": trade.price_amount,
            "price_currency": trade.price_currency.value if trade.price_currency else None
        }
