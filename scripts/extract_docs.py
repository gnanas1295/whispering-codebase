import json
import re

try:
    with open('/mnt/c/Users/gnana/.gemini/antigravity/brain/2d44e082-689f-4f2e-bdd7-4c56bb699019/.system_generated/steps/315/content.md', 'r', encoding='utf-8') as f:
        html = f.read()
    
    text = re.sub(r'<[^>]+>', ' ', html)
    text = re.sub(r'\s+', ' ', text)
    
    with open('parsed_docs.txt', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Done")
except Exception as e:
    print('Error:', e)
