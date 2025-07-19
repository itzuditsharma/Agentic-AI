import re
import json

def chunk_misra_rules(text):
    pattern = r"(Rule|Directive)\s+\d+\.\d+.*?(?=(Rule|Directive)\s+\d+\.\d+|$)"
    matches = re.finditer(pattern, text, re.DOTALL)

    chunks = []
    for match in matches:
        rule_text = match.group().strip()
        chunks.append({"rule": rule_text})

    return chunks

with open("misra_raw.txt", "r", encoding="utf-8") as f:
    text = f.read()

chunks = chunk_misra_rules(text)

# Save to JSON for RAG
with open("misra_rules.json", "w", encoding="utf-8") as f:
    json.dump(chunks, f, indent=2)

print(f"[✓] Extracted and chunked {len(chunks)} MISRA rules.")
