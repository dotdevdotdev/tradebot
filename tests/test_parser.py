import pytest
from datetime import datetime, timedelta

from src.parser.parser import TradeParser


def test_parse_line():
    parser = TradeParser()
    
    # Test valid trade line
    line = "[00:19:24] <Valentyan> (Cad) WTB 100+C skiller pickaxe (grinding prospecting)"
    result = parser.parse_line(line)
    
    assert result is not None
    assert result["player_name"] == "Valentyan"
    assert result["server"] == "Cadence"
    assert result["trade_type"] == "WTB"
    
    # Test system message
    line = "[15:23:26] <System> This is the Trade channel."
    result = parser.parse_line(line)
    assert result is None
    
    # Test invalid line
    line = "Invalid line format"
    result = parser.parse_line(line)
    assert result is None


def test_parse_items():
    parser = TradeParser()
    
    # Test item with attributes
    message = "[rare iron pickaxe QL:96.0086 DMG:0.0 WT:2.0 WoA 89 • CoC 93]"
    items = parser._parse_items(message)
    
    assert len(items) == 1
    item = items[0]
    assert item["name"] == "iron pickaxe"
    assert item["rarity"] == "rare"
    assert item["quality_level"] == 96.0086
    assert item["weight"] == 2.0
    assert item["damage"] == 0.0
    
    # Test attributes
    assert any(attr["name"] == "WoA" and attr["value"] == "89" for attr in item["attributes"])
    assert any(attr["name"] == "CoC" and attr["value"] == "93" for attr in item["attributes"])


def test_parse_price():
    parser = TradeParser()
    
    # Test silver price
    message = "WTS [common iron hammer] 10s"
    amount, currency = parser._parse_price(message)
    assert amount == 10.0
    assert currency == "silver"
    
    # Test gold price
    message = "WTS [rare sword] 1g"
    amount, currency = parser._parse_price(message)
    assert amount == 1.0
    assert currency == "gold"
    
    # Test no price
    message = "WTS [common iron hammer]"
    amount, currency = parser._parse_price(message)
    assert amount is None
    assert currency is None 