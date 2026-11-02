import urllib.request,json,hashlib
from pathlib import Path
out=Path(__file__).resolve().parent.parent/'artifacts/sources/special-medical'
out.mkdir(parents=True,exist_ok=True)
urls={
'39-preview.html':'https://pdfcoffee.com/39th-bcs-medical-part-questions-solution-and-analysis-pdf-free.html',
'42-original-links.html':'https://jobstestbd.com/42-bcs-preliminary-mcq-exam-question-solution-2021/',
'48-links.html':'https://porikha.com/48th-bcs-medical-part-solution-2025/',
'48-combined.html':'https://lokkha.com/latest-exam/read/45',
'medical-digest.pdf':'https://heartsmedistudy.com/api/book/pdf/68d49f4d-c567-4ede-8100-ad04632fd9aa',
'three-special-public-preview.html':'https://www.scribd.com/document/1066178029/Bcs-39th-42nd-47th-Special-Bcs-Mcq-Booklet'
}
manifest=[]
for filename,url in urls.items():
 p=out/filename
 try:
  if not p.exists():
   with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=90) as response:p.write_bytes(response.read())
  manifest.append({'file':filename,'url':url,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()});print(filename,p.stat().st_size,flush=True)
 except Exception as e:print(filename,type(e).__name__,str(e),flush=True)
(out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
