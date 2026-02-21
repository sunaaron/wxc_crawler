import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
resp = requests.get('https://bbs.wenxuecity.com/znjy/', headers=headers)
soup = BeautifulSoup(resp.text, 'html.parser')

# Find tables with many rows (likely the article list)
tables = soup.find_all('table')
print(f'Found {len(tables)} tables')
for i, t in enumerate(tables[:10]):
    rows = t.find_all('tr')
    cls = t.get('class', [])
    tid = t.get('id', '')
    if len(rows) > 3:
        print(f'--- Table {i}: class={cls}, id={tid}, rows={len(rows)} ---')
        # Print second row as sample
        if len(rows) > 1:
            print(str(rows[1])[:500])
        print()

# Look for anchor tags that look like article links
print("\n--- Searching for article links ---")
# WXC article URLs match pattern /znjy/XXXXXXX.html
import re
article_links = soup.find_all('a', href=re.compile(r'/znjy/\d+\.html'))
print(f'Found {len(article_links)} article links')
for link in article_links[:5]:
    print(f'  href={link["href"]}, text={link.get_text(strip=True)[:80]}')
    parent = link.find_parent('tr')
    if parent:
        print(f'  parent TR: {str(parent)[:300]}')
    print()
