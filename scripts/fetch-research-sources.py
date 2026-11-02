"""Download public source material; credentials and private groups are never used."""
import json, urllib.request, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
DEST=ROOT/'artifacts'/'sources'
DEST.mkdir(parents=True,exist_ok=True)
def fetch(url,path):
    req=urllib.request.Request(url,headers={'User-Agent':'BCSMaster-Research/1.0'})
    with urllib.request.urlopen(req,timeout=120) as response, path.open('wb') as output:
        while block:=response.read(1024*1024): output.write(block)
    return {'url':url,'path':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bytes':path.stat().st_size}
def metadata(repo):
    return json.load(urllib.request.urlopen('https://huggingface.co/api/datasets/'+repo,timeout=60))
manifest=[]
for repo,files in [('awinml/medmcqa',['README.md','train.json']),('azminetoushikwasi/bangla-bcs-qs',['README.md'])]:
    meta=metadata(repo)
    (DEST/(repo.replace('/','-')+'-metadata.json')).write_text(json.dumps(meta,indent=2),encoding='utf-8')
    sha=meta['sha'];print(repo,sha,flush=True)
    for filename in files:
        path=DEST/(repo.replace('/','-')+'-'+filename)
        if path.exists():print('Already downloaded',path.name,flush=True);continue
        manifest.append(fetch(f'https://huggingface.co/datasets/{repo}/resolve/{sha}/{filename}',path));print('Downloaded',path.name,path.stat().st_size,flush=True)
manifest.append(fetch('https://raw.githubusercontent.com/medmcqa/medmcqa/main/LICENSE.md',DEST/'medmcqa-LICENSE.md'))
manifest.append(fetch('https://raw.githubusercontent.com/SangbitDas/bcs-dataset/main/bcs_preliminary_question_bank.json',DEST/'bcs-historical-analysis.json'))
manifest.append(fetch('https://raw.githubusercontent.com/SangbitDas/bcs-dataset/main/DATA_LICENSE.md',DEST/'bcs-DATA_LICENSE.md'))
(DEST/'downloads.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print('All source downloads complete',flush=True)
