import re

def parse_expense(text: str):
    match = re.match(r"(.+)\s+(\d+)", text.strip())
    if not match:
       return None
    
    title = match.group(1)
    amount = int(match.group(2))

    return title, amount