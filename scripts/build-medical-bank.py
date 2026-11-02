"""Build an attributed supplemental bank; never label dataset items as BCS papers.
Raw JSON cop is ONE-based (the Hugging Face Parquet version differs).
"""
import json,re,html,hashlib,collections,random,difflib
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
RAW=ROOT/'artifacts/sources/awinml-medmcqa-train.json'
BASE=ROOT/'data/authored-questions.json'
if not BASE.exists():BASE.write_bytes((ROOT/'questions.json').read_bytes())
base=json.loads(BASE.read_text(encoding='utf-8'))
mapping={'Anatomy':'Anatomy','Physiology':'Physiology','Biochemistry':'Biochemistry','Pharmacology':'Pharmacology','Forensic Medicine':'Forensic Medicine','Social & Preventive Medicine':'Community Medicine','Pathology':'Pathology','Medicine':'Medicine','Surgery':'Surgery','Gynaecology & Obstetrics':'Obstetrics & Gynaecology'}
def clean(s):return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',str(s or '')))).strip()
def norm(s):return re.sub(r'[^\w]+','',s.casefold())
def words(s):return re.findall(r'[a-z]+|\d+',s.casefold())
def grams(s):
 w=words(s);return {' '.join(w[i:i+3]) for i in range(len(w)-2)}
rejected=collections.Counter();pools=collections.defaultdict(lambda:collections.defaultdict(list));labelCounts=collections.Counter()
bad=re.compile(r'\b(?:india|indian|ipc|crpc|mci|nmc|rupees?|bharat|supreme court|national programme|national program|rntcp|naco|nfhs|census|pndt|mtp act|esi act|factory act|in the figure|shown below|following image|see diagram)\b',re.I)
for line in RAW.open(encoding='utf-8'):
 r=json.loads(line);subject=r.get('subject_name');labelCounts[r.get('cop')]+=1
 if subject not in mapping:rejected['outside_selected_subjects']+=1;continue
 q=clean(r.get('question'));e=clean(r.get('exp'));opts=[clean(r.get(k)) for k in ['opa','opb','opc','opd']]
 if r.get('choice_type')!='single' or r.get('cop') not in [1,2,3,4]:rejected['invalid_choice_type_or_key']+=1;continue
 if len(q)<30 or len(q)>1800 or len(e)<180 or len(e)>4000 or len(e.split())<28:rejected['insufficient_or_oversized_text']+=1;continue
 if any(not x or len(x)>600 for x in opts) or len({norm(x) for x in opts})!=4:rejected['invalid_options']+=1;continue
 if bad.search(q+' '+e+' '+clean(r.get('topic_name'))):rejected['country_specific_or_missing_visual']+=1;continue
 if re.search(r'\b(?:aoa|aoic|veebra|veebrae|aery|aeries|poion|impoant|propeies|peaining)\b',q+' '+e) or re.search(r'\b(?:figure|diagram|photograph|image|shown)\b',q,re.I):rejected['corrupted_word_or_visual_dependency']+=1;continue
 if any(re.search(r'\b(?:all|none|both) (?:of )?(?:the )?(?:above|these|following)|(?:a and b|a & b|b and c|all are correct|all are true)\b',x,re.I) for x in opts):rejected['compound_options']+=1;continue
 if re.search(r'\b(?:not given|no explanation|answer is not|image|img\d|http)\b',e,re.I):rejected['weak_or_external_explanation']+=1;continue
 topic=mapping[subject];sub=clean(r.get('topic_name')) or 'General concepts'
 pools[topic][sub].append({'id':'medmcqa-'+r['id'],'q':q,'o':opts,'a':r['cop']-1,'e':e,'subject':'medical','topic':topic,'subtopic':sub,'type':'practice','collection':'medmcqa','editorial':'dataset-sourced-unreviewed','source':'https://huggingface.co/datasets/awinml/medmcqa','provenance':{'dataset':'MedMCQA','upstreamID':r['id'],'split':'train','revision':'ae3036c873dbd3bc9f33078616cffd20611eb9b1','labelConvention':'raw JSON 1-based, converted to 0-based','originalSubject':subject},'license':'MIT upstream; Apache-2.0 mirror declaration','language':'en','syllabusAlignment':'subject-level only; not historical BCS evidence'})
assert set(labelCounts)=={1,2,3,4},f'Unexpected raw label convention: {labelCounts}'
seen={norm(q['q']) for q in base};signatures={};inverted=collections.defaultdict(set)
def admit(q):
 key=norm(q['q'])
 if key in seen:rejected['exact_normalized_duplicate']+=1;return False
 gs=grams(q['q']);candidate=set()
 for g in sorted(gs,key=lambda g:len(inverted[g]))[:6]:candidate.update(inverted[g])
 for idx in candidate:
  old=signatures[idx];overlap=len(gs&old)
  if overlap/max(1,len(gs|old))>=.62:rejected['near_duplicate_stem']+=1;return False
 # Digits and punctuation changes alone are never new questions.
 numeric=re.sub(r'\d+','#',key)
 if numeric in numericSeen:rejected['numeric_variant']+=1;return False
 numericSeen.add(numeric);seen.add(key);idx=q['id'];signatures[idx]=gs
 for g in gs:inverted[g].add(idx)
 return True
numericSeen={re.sub(r'\d+','#',norm(q['q'])) for q in base}
selected=[];topicStats={}
for topic,subtopics in pools.items():
 # Round-robin across source subtopics prevents one system from dominating selection.
 rng=random.Random(20261103)
 for qs in subtopics.values():rng.shuffle(qs)
 chosen=[];keys=sorted(subtopics);cursor=0
 while len(chosen)<1000 and any(subtopics.values()):
  sub=keys[cursor%len(keys)];cursor+=1
  if subtopics[sub]:
   q=subtopics[sub].pop()
   if admit(q):chosen.append(q)
 if len(chosen)<1000:raise RuntimeError(f'{topic}: only {len(chosen)} eligible questions; refusing padding')
 selected.extend(chosen);topicStats[topic]={'questions':len(chosen),'subtopics':len({q['subtopic'] for q in chosen})};print(topic,len(chosen),flush=True)
assert len(selected)==10000
bank=selected
(ROOT/'data/supplemental-medmcqa.json').write_text(json.dumps(bank,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8',newline='\n')
manifest={'activeQuestions':len(base),'separateSupplementalQuestions':len(bank),'authoredOrInherited':len(base),'sourcedMedical':len(selected),'topics':topicStats,'rejectionCounts':dict(rejected),'rawLabelDistribution':dict(labelCounts),'sourceSHA256':hashlib.sha256(RAW.read_bytes()).hexdigest(),'rawRows':sum(labelCounts.values()),'selection':'1000 per mapped medical subject; round-robin subtopics; deterministic seed; normalized and trigram similarity filters','limitations':['Syllabus alignment is subject-level, not independent item-by-item validation','No historical BCS identity or prediction claim','Dataset answers and explanations have not received independent medical editorial review','Trigram screening reduces but cannot prove absence of semantic redundancy','General subjects retain the smaller authored starter bank']}
(ROOT/'data/research/medical-selection.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('SEPARATE SUPPLEMENT:',len(bank),flush=True)
