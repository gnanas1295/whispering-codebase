import re
try:
    with open('/mnt/c/Users/gnana/.gemini/antigravity/brain/2d44e082-689f-4f2e-bdd7-4c56bb699019/.system_generated/steps/315/content.md', 'r', encoding='utf-8') as f:
        text = f.read()
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if 'mcp' in line.lower() or 'brontoscope' in line.lower() or 'search' in line.lower() or 'fetch' in line.lower():
            clean_line = re.sub(r'<[^>]+>', '', line).strip()
            if len(clean_line) > 5 and len(clean_line) < 200:
                print(f"Line {i}: {clean_line}")
except Exception as e:
    print("Error:", e)
