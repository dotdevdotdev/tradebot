# Trade Data Processor

A Python application for processing and analyzing trade data from Wurm Online game chat logs.

## Features

- Parse trade chat logs from Wurm Online
- Extract item information, attributes, and traits
- Store data in SQLite database
- Handle multiple servers (Harmony, Melody, Cadence)
- Process various item types and rarities
- Track prices in different currencies (iron, copper, silver, gold)
- Convert timestamps from MST to GMT

## Project Structure

```
tradebot/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── database/
│   │   ├── __init__.py
│   │   └── database.py
│   └── parser/
│       ├── __init__.py
│       └── parser.py
├── data/
│   ├── trade-2025-05--small.txt
│   ├── database-structure.md
│   └── prompt.md
├── tests/
├── config/
├── logs/
├── requirements.txt
└── setup.py
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install the package in development mode:
```bash
pip install -e .
```

## Usage

Process a trade log file:
```bash
python src/main.py data/trade-2025-05--small.txt --date 2025-05-01
```

The application will:
1. Parse the trade log file
2. Extract trade information, items, and their attributes
3. Convert timestamps from MST to GMT
4. Store everything in a SQLite database (tradebot.db)

## Database Schema

The application uses the following database structure:

### trades
- id (PRIMARY KEY)
- timestamp (DATETIME, GMT)
- server (ENUM: 'Har', 'Mel', 'Cad')
- player_name (VARCHAR)
- trade_type (ENUM: 'WTS', 'WTB', 'WTT', 'PC')
- message (TEXT)

### items
- id (PRIMARY KEY)
- trade_id (FOREIGN KEY)
- name (VARCHAR)
- rarity (ENUM: 'common', 'rare', 'supreme', 'fantastic')
- quality_level (DECIMAL)
- weight (DECIMAL)
- damage (DECIMAL)
- price_amount (DECIMAL)
- price_currency (ENUM: 'iron', 'copper', 'silver', 'gold')

### item_attributes
- id (PRIMARY KEY)
- item_id (FOREIGN KEY)
- attribute_name (VARCHAR)
- attribute_value (VARCHAR)

### item_traits
- id (PRIMARY KEY)
- item_id (FOREIGN KEY)
- trait_type (VARCHAR)
- trait_value (INTEGER)

## Development

### Running Tests
```bash
pytest tests/
```

### Code Style
The project uses:
- Black for code formatting
- isort for import sorting
- mypy for type checking

Run the formatters:
```bash
black src/ tests/
isort src/ tests/
mypy src/ tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License 