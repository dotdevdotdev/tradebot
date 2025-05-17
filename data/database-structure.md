# Trade Database Structure

## Tables

### trades
- id (PRIMARY KEY)
- timestamp (DATETIME, GMT)
- server (ENUM: 'Har', 'Mel', 'Cad')
- player_name (VARCHAR)
- trade_type (ENUM: 'WTS', 'WTB', 'WTT', 'PC')
- message (TEXT)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)

### items
- id (PRIMARY KEY)
- trade_id (FOREIGN KEY -> trades.id)
- name (VARCHAR)
- rarity (ENUM: 'common', 'rare', 'supreme', 'fantastic')
- quality_level (DECIMAL(10,4))
- weight (DECIMAL(10,4))
- damage (DECIMAL(10,4))
- price_amount (DECIMAL(10,2))
- price_currency (ENUM: 'iron', 'copper', 'silver', 'gold')
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)

### item_attributes
- id (PRIMARY KEY)
- item_id (FOREIGN KEY -> items.id)
- attribute_name (VARCHAR)
- attribute_value (VARCHAR)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)

### item_traits
- id (PRIMARY KEY)
- item_id (FOREIGN KEY -> items.id)
- trait_type (VARCHAR)
- trait_value (INTEGER)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)

## Notes
- All timestamps should be stored in GMT
- Item names should be stored without brackets
- Special attributes (like CoC, BoTD, etc.) should be stored in item_attributes
- Animal traits (like 4s, 4d) should be stored in item_traits
- Currency conversions should be handled at the application level
- Server tags should be normalized to full names (Harmony, Melody, Cadence)
