from pathlib import Path
from typing import Dict
import json

def read_prompt_template(prompt_path: str = "data/prompt.md") -> str:
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()

def format_prompt(template: str, trade_data: Dict) -> str:
    # Insert trade data as JSON for clarity in the prompt
    trade_json = json.dumps(trade_data, indent=2)
    return template.replace("{{trade_data}}", trade_json) 