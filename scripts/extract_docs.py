import json
import re

try:
    with open('/mnt/c/Users/gnana/.gemini/antigravity/brain/2d44e082-689f-4f2e-bdd7-4c56bb699019/.system_generated/steps/315/content.md', 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Just grab text using simple regex
    text = re.sub(r'<[^>]+>', ' ', html)
    text = re.sub(r'\s+', ' ', text)
    
    idx = text.lower().find('openclaw cli')
    if idx != -1:
        print("FOUND CLI SECTION:")
        print(text[max(0, idx-50):idx+3000])
    else:
        print("Not found. Printing some text:")
        print(text[:1000])
except Exception as e:
    print('Error:', e)
