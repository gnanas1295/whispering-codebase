import re

with open('/home/gnana/clones/whispering-codebase/parsed_docs.txt', 'r') as f:
    text = f.read()

print("Searching for 'api' or 'query' or 'fetch'...")
# Find snippets containing words related to fetching data
for match in re.finditer(r'.{0,100}(?:api|query|fetch|search|read).{0,100}', text, re.IGNORECASE):
    snippet = match.group(0).replace('\n', ' ')
    if 'bronto' in snippet.lower():
        print(snippet)
