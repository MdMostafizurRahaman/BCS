import sys,urllib.request,json,concurrent.futures
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'artifacts/python'))
from bs4 import BeautifulSoup
out=Path(__file__).resolve().parent.parent/'artifacts/sources/special-medical'
s=BeautifulSoup((out/'satt39-exam-1.html').read_text(encoding='utf-8'),'html.parser')
links={a['href'] for a in s.find_all('a',href=True) if '?page=' in a['href']}
def get(url):
 n=url.split('page=')[-1];p=out/f'satt39-exam-{n}.html'
 if not p.exists():
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=60) as r:p.write_bytes(r.read())
 return n,p.stat().st_size
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 for result in pool.map(get,sorted(links)):print(result,flush=True)
