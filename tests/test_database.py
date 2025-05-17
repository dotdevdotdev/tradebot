import pytest
from datetime import datetime
from src.database.database import Database
from src.models.models import Trade, Item, ItemAttribute


@pytest.fixture
def db():
    """Create a test database instance."""
    return Database(":memory:")  # Use in-memory SQLite for testing


def test_create_tables(db):
    """Test that tables are created correctly."""
    # Tables should be created during initialization
    cursor = db.conn.cursor()
    
    # Check if tables exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    
    assert "trades" in tables
    assert "items" in tables
    assert "item_attributes" in tables


def test_save_trade(db):
    """Test saving a trade with items and attributes."""
    # Create test data
    trade = Trade(
        timestamp=datetime.now(),
        player_name="TestPlayer",
        server="TestServer",
        trade_type="WTS",
        message="WTS [rare sword] 10s",
        price_amount=10.0,
        price_currency="silver"
    )
    
    item = Item(
        name="sword",
        rarity="rare",
        quality_level=100.0,
        weight=2.0,
        damage=10.0
    )
    
    attribute = ItemAttribute(
        name="WoA",
        value="100"
    )
    
    item.attributes.append(attribute)
    trade.items.append(item)
    
    # Save trade
    db.save_trade(trade)
    
    # Verify trade was saved
    cursor = db.conn.cursor()
    cursor.execute("SELECT * FROM trades WHERE player_name = ?", ("TestPlayer",))
    trade_row = cursor.fetchone()
    
    assert trade_row is not None
    assert trade_row[2] == "TestPlayer"
    assert trade_row[3] == "TestServer"
    assert trade_row[4] == "WTS"
    
    # Verify item was saved
    cursor.execute("SELECT * FROM items WHERE name = ?", ("sword",))
    item_row = cursor.fetchone()
    
    assert item_row is not None
    assert item_row[1] == "sword"
    assert item_row[2] == "rare"
    assert item_row[3] == 100.0
    
    # Verify attribute was saved
    cursor.execute("SELECT * FROM item_attributes WHERE name = ?", ("WoA",))
    attr_row = cursor.fetchone()
    
    assert attr_row is not None
    assert attr_row[1] == "WoA"
    assert attr_row[2] == "100" 