# Trade Data Parsing Instructions

## Overview
You will be provided with raw trade chat logs from the game. Your task is to parse these logs and extract structured information about trades, items, and their attributes.

## Data Format
The input data will be in the following format:
```
[HH:MM:SS] <PlayerName> (Server) TradeType Message
```

## Key Elements to Extract

### Basic Trade Information
- Timestamp (convert from MST to GMT)
- Player Name
- Server (Har=Harmony, Mel=Melody, Cad=Cadence)
- Trade Type (WTS, WTB, WTT, PC)
- Full Message

### Item Information
For each item in the message, extract:
- Item Name (remove brackets)
- Rarity (common, rare, supreme, fantastic)
- Quality Level (QL)
- Weight (WT)
- Damage (DMG)
- Price (if specified)
- Currency (iron, copper, silver, gold)

### Special Attributes
Look for and extract:
- Enchantments (CoC, BoTD, WoA, etc.)
- Animal Traits (4s, 4d, etc.)
- Other special attributes

## Rules
1. Convert all timestamps from MST to GMT
2. Remove brackets from item names
3. Normalize server names to full names
4. Extract prices and convert to standard currency (silver)
5. Handle multiple items in a single message
6. Skip system messages and non-trade messages
7. Handle [null] items appropriately
8. Extract and normalize animal traits
9. Handle item fragments (e.g., [1/3])

## Output Format
Provide the extracted information in a structured format that can be easily inserted into the database tables defined in database-structure.md.

## Example
Input:
```
[00:19:24] <Valentyan> (Cad) WTB 100+C skiller pickaxe (grinding prospecting)
```

Output:
```json
{
  "trade": {
    "timestamp": "2025-05-01 07:19:24",
    "server": "Cadence",
    "player_name": "Valentyan",
    "trade_type": "WTB",
    "message": "WTB 100+C skiller pickaxe (grinding prospecting)"
  },
  "items": [{
    "name": "pickaxe",
    "rarity": "common",
    "quality_level": 100.0,
    "attributes": [{
      "name": "CoC",
      "value": "100+"
    }]
  }]
}
```
