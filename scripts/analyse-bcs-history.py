"""Publish aggregate research only, not third-party questions or solve notes."""
import json, collections, re, hashlib
from pathlib import Path
root=Path(__file__).resolve().parent.parent
source=root/'artifacts/sources/bcs-historical-analysis.json'
db=json.loads(source.read_text(encoding='utf-8'))
forms={'negative_or_exception':r'নয়|নয়|ব্যতীত|except|incorrect|not\b', 'calculation':r'শতকরা|সমীকরণ|অনুপাত|লগ|log\b|গড়|গড়|বর্গ|ত্রিভুজ|লসাগু|গসাগু', 'author_title':r'রচয়িতা|রচয়িতা|রচনা|লেখক|কাব্য|উপন্যাস|author|wrote|poet', 'language_rule':r'সন্ধি|সমাস|কারক|প্রত্যয়|প্রত্যয়|উপসর্গ|বানান|spelling|preposition|sentence|verb|tense|voice|article', 'date_or_number':r'কত সালে|কবে|কতটি|কতজন|কোন সালে|কত তারিখ|which year'}
exams=[]
for slug in ['39th_bcs','42nd_bcs','48th_bcs']:
 qs=[q for q in db['questions'] if q['exam_slug']==slug]
 exams.append({'exam':slug,'sourceRows':len(qs),'scope':'general section only; medical absent','subjects':dict(collections.Counter(q['subject_en'] for q in qs)),'questionFormsNonExclusive':{k:sum(bool(re.search(pattern,q['question'],re.I)) for q in qs) for k,pattern in forms.items()},'imageDependent':sum(bool(q['has_question_image']) for q in qs),'missingExplanation':sum(not q.get('solve_note','').strip() for q in qs)})
def norm(s):return re.sub(r'[^\w]+','',s.casefold())
groups=collections.defaultdict(set)
for q in db['questions']:groups[norm(q['question'])].add(q['exam_slug'])
repeats=sum(len(x)>1 for x in groups.values())
report={'source':'https://github.com/SangbitDas/bcs-dataset','sourcePublisher':'uttoron.academy (via research compilation)','sourceSHA256':hashlib.sha256(source.read_bytes()).hexdigest(),'allExamRows':len(db['questions']),'allExamCount':len(db['exams']),'scopeLimitations':['Not authenticated against original PSC scans','Special-health rows cover only general sections','Publisher subject labels may differ from official subject distribution','Regex forms overlap and are not human-validated topic classifications','Text-exact repeats do not measure concept recurrence','Historical metadata and answer keys may contain errors'],'specialHealthGeneral':exams,'exactStemGroupsAcrossMultipleExams':repeats,'methods':forms,'prediction':'No estimated chance of appearing in a future examination is established.'}
out=root/'data/research/historical-patterns.json';out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'sourceRows':len(db['questions']),'exams':len(db['exams']),'specialGeneralRows':sum(x['sourceRows'] for x in exams),'crossExamExactRepeatGroups':repeats}))
