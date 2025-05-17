import pytest
from pathlib import Path
from src.main import main


def test_main_with_invalid_file():
    """Test main function with non-existent file."""
    with pytest.raises(FileNotFoundError):
        main("nonexistent.txt")


def test_main_with_empty_file(tmp_path):
    """Test main function with empty file."""
    # Create empty file
    file_path = tmp_path / "empty.txt"
    file_path.write_text("")
    
    # Run main
    main(str(file_path))
    
    # Verify database was created
    db_path = Path("trades.db")
    assert db_path.exists()
    
    # Clean up
    db_path.unlink()


def test_main_with_sample_data(tmp_path):
    """Test main function with sample trade data."""
    # Create sample data file
    file_path = tmp_path / "sample.txt"
    file_path.write_text("""[00:19:24] <Valentyan> (Cad) WTB 100+C skiller pickaxe (grinding prospecting)
[00:19:24] <Valentyan> (Cad) WTS [rare iron pickaxe QL:96.0086 DMG:0.0 WT:2.0 WoA 89 • CoC 93] 10s
[15:23:26] <System> This is the Trade channel.""")
    
    # Run main
    main(str(file_path))
    
    # Verify database was created and contains data
    db_path = Path("trades.db")
    assert db_path.exists()
    
    # Clean up
    db_path.unlink() 