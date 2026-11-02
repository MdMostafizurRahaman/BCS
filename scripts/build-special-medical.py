"""Build the local Bangladesh special-BCS supplement from public source snapshots.

Publisher explanations are not copied. Notes are separately authored study notes.
Downloaded transcripts remain in the ignored local personal-study archive.
"""
import sys,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'artifacts/python'))
from bs4 import BeautifulSoup
OUT=ROOT/'artifacts/sources/special-medical'
LIVE='https://web.livemcq.com/blog/48th-special-bcs-question-pdf'

# Original published numbering, topic and independently written concept notes.
NOTES='''101|Medicine|Early compensation can increase respiratory rate before hypotension or reduced urine output develops.
102|Physiology|About two thirds of total body water is intracellular; plasma and interstitial fluid belong to the extracellular compartment.
103|Obstetrics & Gynaecology|Postpartum haemorrhage can complicate caesarean delivery as well as vaginal birth.
104|Anatomy|Epidermal Langerhans cells process antigen and present it to T lymphocytes.
105|Anatomy|Hepatic veins carry blood from the liver directly into the inferior vena cava.
106|Anatomy|The median nerve and flexor tendons traverse the carpal tunnel; the ulnar nerve passes through Guyon's canal.
107|Forensic Medicine|Adipocere develops during later postmortem change in suitable moist conditions; cooling and rigor are earlier changes.
108|Obstetrics & Gynaecology|Timely obstetric care prevents prolonged obstructed labour, an important cause of obstetric fistula.
109|Community Medicine|Screening seeks unsuspected disease or risk in apparently healthy people; diagnostic testing evaluates a clinical suspicion.
110|Pharmacology|Atropine blocks muscarinic effects. Tachycardia may occur, but treatment endpoints require clinical assessment, especially respiratory secretions.
111|Surgery|Inhalation injury can threaten the airway even when the visible skin burn is small. Other referral criteria can also apply.
112|Obstetrics & Gynaecology|Increased iron requirements make iron deficiency the commonest cause of anaemia in pregnancy.
113|Obstetrics & Gynaecology|Fetal urine contributes substantially to amniotic fluid later in gestation; bilateral renal agenesis can cause severe oligohydramnios.
114|Surgery|Published key: absent guarding. The stem mixes symptoms and signs, and guarding or rebound varies with severity; this item needs editorial review.
115|Medicine|Nikolsky sign denotes epidermal separation with pressure. It is associated with SJS/TEN but is not exclusive to it.
116|Anatomy|Olfaction is conveyed by cranial nerve I; the trigeminal nerve also detects irritant sensations in the nose.
117|Anatomy|Urothelium, traditionally called transitional epithelium, lines much of the urinary collecting tract and accommodates distension.
118|Anatomy|The posterior base of the heart is formed predominantly by the left atrium.
119|Pathology|Persistent infection with oncogenic human papillomavirus types is a major cause of cervical carcinoma.
120|Surgery|An everted edge suggests a malignant ulcer, classically squamous carcinoma; an undermined edge suggests other causes such as tuberculosis.
121|Anatomy|The ciliary ganglion relays parasympathetic fibres to the sphincter pupillae and ciliary muscle.
122|Community Medicine|Stratified random sampling uses random selection within defined strata; quota and purposive sampling are non-probability methods.
123|Surgery|Pathological phimosis can be an indication for circumcision. Hypospadias requires assessment because the foreskin may be needed for repair.
124|Obstetrics & Gynaecology|Congenital toxoplasmosis can cause fetal injury. Varicella can also cause congenital abnormalities, so this single-best-answer stem is ambiguous.
125|Pathology|Mitochondrial cytochrome-c release activates the intrinsic apoptotic pathway; apoptosis also has an extrinsic death-receptor pathway.
126|Obstetrics & Gynaecology|Pelvic organ prolapse commonly produces pressure or a bulge that becomes more noticeable while standing or straining.
127|Pathology|IL-1 is an endogenous pyrogen; cytokine signalling promotes hypothalamic prostaglandin production and raises the temperature set point.
128|Obstetrics & Gynaecology|Amenorrhoea followed by abdominal pain is a typical presentation of ectopic pregnancy. The tubal ampulla is the commonest implantation site.
129|Physiology|The bicarbonate-carbon dioxide system is the major extracellular buffer and is regulated by the lungs and kidneys.
130|Surgery|A grade-V splenic injury is severe. The historical key favours splenectomy; actual management also depends on haemodynamic stability and available interventions.
131|Pathology|Activated leukocytes can injure surrounding tissue during inflammatory arthritis. The broad wording does not uniquely describe every listed disease.
132|Medicine|Many nosebleeds have no identified systemic cause and are labelled idiopathic; examination still looks for local and systemic causes.
133|Surgery|Hartmann's is a balanced crystalloid used in burn resuscitation. Fluid choice and volume must follow the patient's clinical assessment.
134|Anatomy|Longitudinal growth occurs at the epiphyseal growth plate; cartilage proliferation and replacement lengthen the bone.
135|Medicine|Historical published key: new LBBB. New LBBB alone is not a current standalone indication for thrombolysis; assess symptoms, ECG criteria and contemporary ACS guidance.
136|Medicine|Primary aldosteronism (Conn's syndrome) causes secondary hypertension. Renal ischaemia can also cause it, making this item ambiguous.
137|Obstetrics & Gynaecology|A prophylactic uterotonic is a central element of active management of the third stage; the published option specifies oxytocin 10 IU IM.
138|Pathology|Ziehl-Neelsen staining detects acid-fast bacilli. The organism's lipid-rich cell wall resists conventional decolourisation.
139|Pharmacology|Ceftriaxone has renal and biliary elimination and often needs no adjustment for isolated renal impairment; combined organ dysfunction needs caution.
140|Physiology|Published key: platelet aggregation. Platelet adhesion, activation and aggregation form primary haemostasis; coagulation then stabilises the plug with fibrin.
141|Medicine|The publisher groups non-ulcer dyspepsia with acid-peptic presentations; dyspepsia does not itself establish an ulcer or acid-mediated disease.
142|Obstetrics & Gynaecology|Severe hypertension and cerebrovascular complications, including intracranial haemorrhage, can cause maternal death in eclampsia.
143|Pharmacology|Sulfasalazine may be used in pregnancy with appropriate folate and specialist review; methotrexate and mycophenolate are teratogenic.
144|Physiology|Published option: plasminogen. Its activated form, plasmin, directly digests fibrin; the distinction matters because the stem is imprecise.
145|Surgery|Secondary-intention healing closes an open tissue defect through granulation, contraction and epithelialisation, typically with more inflammation and scarring.
146|Medicine|Thyrotoxicosis with low radioactive iodine uptake suggests release of stored hormone, as in thyroiditis, rather than increased synthesis in Graves disease.
147|Surgery|Published key: mild serosanguineous discharge. Discharge alone is not a diagnostic criterion for infection; use clinical findings and accepted SSI definitions.
148|Medicine|Vitamin-B12 deficiency can produce megaloblastic anaemia and neurological injury; isolated folate deficiency generally lacks the characteristic neuropathy.
149|Medicine|Ascites is a decompensating event in cirrhosis; splenomegaly may precede decompensation. The source appears to mean decompensation rather than decompression.
150|Surgery|Periampullary malignancy may obstruct the bile duct and cause painless jaundice; stones and cholangitis more often cause pain or systemic illness.
151|Medicine|Rheumatic fever follows streptococcal infection through an immune-mediated process that can affect the heart, joints, skin and nervous system.
152|Obstetrics & Gynaecology|Poorly controlled maternal diabetes increases risks including fetal malformations and stillbirth; respiratory distress syndrome is principally a neonatal condition.
153|Medicine|Longstanding recurrent haemoptysis with clubbing suggests bronchiectasis in this vignette; imaging and the wider clinical history distinguish alternatives.
154|Anatomy|The liver is the largest gland in the human body; the skin is the largest organ overall.
155|Anatomy|The submucosa contains larger blood vessels, lymphatics and the submucosal nerve plexus; vessels and nerves also occur in other gut layers.
156|Forensic Medicine|Valid consent requires decision-making capacity. Illiteracy, age or illness alone does not establish incapacity; assess the particular decision.
157|Community Medicine|The historical Bangladesh EPI answer is BCG at birth. National vaccine schedules can change and should be checked against the current schedule.
158|Forensic Medicine|A typical hanging ligature mark tends to run obliquely upward and is often incomplete; findings must be interpreted with the whole investigation.
159|Pharmacology|Glycosuria caused by SGLT2 inhibitors increases the risk of genital mycotic infection.
160|Anatomy|Alveoli are the principal gas-exchange units. An acinus comprises the gas-exchanging structures distal to a terminal bronchiole.
161|Obstetrics & Gynaecology|Pregnancy is hypercoagulable, with increases in several clotting factors including factor X.
162|Community Medicine|Rapid antigen testing is often cheaper and faster than laboratory nucleic-acid testing. Accuracy depends on the assay, timing and sampling.
163|Physiology|Primary carbon-dioxide retention increases carbonic acid and produces respiratory acidosis; renal compensation takes time.
164|Surgery|Published key: non-electrolyte. The terminology is unusual; ideal sutures should be predictable, minimally reactive and non-carcinogenic. Source wording needs review.
165|Pharmacology|Idiosyncrasy is an unusual, often unpredictable individual drug response; it differs from a predictable extension of the usual pharmacological effect.
166|Pharmacology|Phenobarbital induces hepatic enzymes and can reduce warfarin's anticoagulant effect, increasing thromboembolic risk if the interaction is unmanaged.
167|Surgery|The left internal mammary artery has excellent long-term patency and is commonly preferred for the left anterior descending coronary target.
168|Medicine|Acute type-II respiratory failure causes hypercapnia and hypoxaemia; a substantial bicarbonate rise usually indicates renal compensation or another process.
169|Surgery|A vascular swelling such as a haemangioma can decrease with compression; this differs from reducibility into a body cavity.
170|Medicine|Keratomalacia destroys corneal tissue and can cause irreversible blindness; earlier ocular manifestations of vitamin-A deficiency may be reversible.
171|Medicine|HLA-B27 is associated with the spondyloarthritis group but is not positive in every patient; the source's word 'all' overstates the association.
172|Medicine|Raised intracranial pressure may produce bradycardia as part of the Cushing response, usually with hypertension and abnormal respiration.
173|Surgery|Follicular thyroid carcinoma spreads haematogenously and can metastasise to bone. The other cancers are not categorically incapable of bone spread.
174|Anatomy|Muscle develops from mesoderm. Skin contains tissues with different embryological origins, so distinguishing epidermis from dermis matters.
175|Forensic Medicine|Radiographs can assist age estimation from skeletal and dental development. They can also locate foreign bodies, so the options are not mutually exclusive.
176|Obstetrics & Gynaecology|CA-125 is associated with epithelial ovarian cancer but is neither specific enough for diagnosis alone nor a general-population screening test.
177|Obstetrics & Gynaecology|Endometriosis is an important cause of severe or persistent dysmenorrhoea in adolescents, particularly when initial management fails.
178|Pharmacology|Ethambutol can cause optic neuropathy affecting acuity and colour vision. This historical stem should not imply that it is universally avoided in children today.
179|Community Medicine|Historical Bangladesh key: four ANC visits. WHO recommends eight contacts; check the current national guidance instead of treating an old exam key as current policy.
180|Anatomy|The uterus is a female reproductive organ; the bladder and urethra primarily belong to the urinary system.
181|Medicine|Thrombocytopenia is a common feature of dengue. Other viral infections can also lower platelets, so the intended answer reflects the typical exam association.
182|Medicine|Anti-HBc IgG and anti-HBs positivity with negative HBsAg generally indicates resolved natural hepatitis-B infection; vaccination alone does not produce anti-HBc.
183|Pharmacology|Published key: six-hourly. A dosing interval cannot be determined from half-life alone; therapeutic window, formulation and pharmacodynamics also matter.
184|Obstetrics & Gynaecology|Ovarian fibroma is a solid stromal tumour; the alternatives listed are principally cystic lesions.
185|Medicine|Historical key: amikacin. This is not a current treatment recommendation: modern drug-resistant TB regimens prioritise eligible all-oral combinations under current guidance.
186|Physiology|Trypsin is a pancreatic protease that cleaves peptide bonds; amylase digests starch and lipase digests fat.
187|Community Medicine|Infant mortality rate is a widely used population-health indicator, reflecting several aspects of maternal, child and social conditions.
188|Physiology|Parathyroid hormone regulates calcium and phosphate balance through effects on bone, kidneys and vitamin-D activation.
189|Medicine|Scabies mites form burrows in the stratum corneum; itching and distribution help distinguish it from psoriasis or acne.
190|Forensic Medicine|Sudden entrapment without access to food can cause acute starvation; duration and water availability strongly affect its course.
191|Medicine|Calcium-channel blockers are effective antihypertensives in older people, but the best agent depends on comorbidities and current guidance.
192|Surgery|The secondary trauma survey includes a head-to-toe examination after immediate threats have been addressed in the primary survey.
193|Obstetrics & Gynaecology|The historical key is insulin. Contemporary management distinguishes pre-existing diabetes from gestational diabetes and may allow metformin in selected settings.
194|Pharmacology|Fluoxetine tends to have less early weight gain than some alternatives; individual and longer-term weight changes vary, so 'does not have any' is too absolute.
195|Physiology|Medullary respiratory networks generate the basic breathing rhythm, with modulation from pontine and higher centres.
196|Obstetrics & Gynaecology|Amniotic-fluid embolism can cause abrupt hypoxia, cardiovascular collapse and coagulopathy; cyanosis reflects severe oxygenation failure.
197|Surgery|A tense, tender groin lump raises concern for strangulation, especially with irreducibility and obstruction; urgent clinical assessment is essential.
198|Obstetrics & Gynaecology|The historical key describes fundal dominance of coordinated labour contractions; contractions are involuntary and may be painful partly through ischaemia.
199|Physiology|Renal tubular acidosis causes hyperchloraemic normal-anion-gap metabolic acidosis; ketoacidosis usually increases the anion gap.
200|Physiology|Albumin is a major contributor to plasma colloid osmotic pressure and also transports many substances. Fibrinogen has the principal clotting role.'''
notes={int(n):(topic,note) for n,topic,note in (line.split('|',2) for line in NOTES.splitlines())}
data=json.loads((ROOT/'artifacts/sources/bcs-historical-analysis.json').read_text(encoding='utf8'))
supp=[]
def row(slug,n,q,o,a,url,topic,note,printed=None):
 return dict(exam_slug=slug,question_number=n,question=q,**{'option_'+k:v for k,v in zip('abcd',o)},correct_answer='ABCD'[a],subject_en='Medical Science',solve_note=note,question_image_paths=[],solve_note_image_paths=[],source_url=url,medical_topic=topic,printed_question_number=printed)
soup=BeautifulSoup((OUT/'live48.html').read_text(encoding='utf8'),'html.parser')
for c in soup.select('.qc'):
 n=int(c.select_one('.qc__num').get_text(strip=True))
 if n<101:continue
 opts=c.select('.qc__opt'); correct=[i for i,x in enumerate(opts) if 'qc__opt--correct' in x.get('class',[])]
 assert len(opts)==4 and len(correct)==1
 topic,note=notes[n]
 supp.append(row('48th_bcs',n,c.select_one('.qc__q').get_text(' ',strip=True),[x.select_one('.qc__opt-text').get_text(' ',strip=True) for x in opts],correct[0],LIVE,topic,note,n))
assert len(supp)==100 and {x['question_number'] for x in supp}==set(range(101,201))
# These seven publicly readable records explicitly carry the 39th BCS tag.
seen=set()
for filename in ['satt39-heart.html','satt39-exam-1.html']:
 s=BeautifulSoup((OUT/filename).read_text(encoding='utf8'),'html.parser')
 for q in s.select('.question-span'):
  c=q.find_parent('div',class_='card');tags=[a.get_text(' ',strip=True) for a in c.select('.tag-div a')]
  if '39th BCS Preli-2018' not in tags or not any('বিজ্ঞান' in t for t in tags):continue
  stem=q.get_text(' ',strip=True)
  if stem in seen:continue
  seen.add(stem);o=[x.get_text(' ',strip=True) for x in c.select('.reading-mode-data label')];a=int(c.select_one('input[name=answer]')['value'])-1
  note={
   'Acute heart failure may occur in':'Acute rheumatic carditis can impair cardiac function and cause heart failure.',
   'Atherosclerosis:':'Atherosclerosis is an inflammatory disease of arterial walls involving lipid accumulation and plaque formation; it can begin well before age forty.',
   'Which of the  following type of necrosis is seen in acute myocardial infarction?':'Ischaemic infarction in solid organs such as the heart typically produces coagulative necrosis; cerebral infarction is a classic exception.',
   'In progressive phase of shock :':'Persistent hypoperfusion causes widespread tissue hypoxia, anaerobic metabolism and organ dysfunction. This phase is not synonymous with irreversible shock.',
   'Non cardiac causes of atrial fibrillation is :':'Acute pneumonia can precipitate atrial fibrillation through hypoxia, inflammation and physiological stress.',
   'Cardiogenic shock may be due to :':'Cardiogenic shock results from failure of the heart to maintain effective forward flow; loss of circulating volume instead causes hypovolaemic shock.',
   'Heparin is :':'Heparin enhances antithrombin activity and inhibits coagulation. It is a glycosaminoglycan, not an enzyme.'}[stem]
  supp.append(row('39th_bcs',101+len(seen)-1,stem,o,a,c.select_one('.card-title a')['href'].strip(),'Pharmacology' if stem=='Heparin is :' else 'Medicine',note))
# The first publicly indexed medical question of the 42nd paper. Do not pad the rest.
supp.append(row('42nd_bcs',101,'A major sign of cardiac tamponade is',['Bradycardia','Ventricular dilatation','3rd degree heart block','Pulsus paradoxus'],3,'https://www.scribd.com/document/1052913928/42nd-Special-BCS-Medical-Part-1','Medicine','Pulsus paradoxus is an exaggerated inspiratory fall in systolic blood pressure, classically greater than 10 mmHg. It is associated with tamponade but is not specific to it.',101))
for exam in data['exams']:
 if exam['slug'] in ['39th_bcs','42nd_bcs','48th_bcs']:
  exam.update(total_questions=200,assembled=True,medical_expected=100)
data['questions']=[q for q in data['questions'] if not(q['exam_slug'] in ['39th_bcs','42nd_bcs','48th_bcs'] and q.get('subject_en')=='Medical Science')]+supp
(ROOT/'artifacts/sources/bcs-with-special-medical.json').write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8')
report={'medicalQuestions':len(supp),'byPaper':{slug:sum(q['exam_slug']==slug for q in supp) for slug in ['39th_bcs','42nd_bcs','48th_bcs']},'notes':'Original medical numbering retained only when available. General and medical sources may use different set orders; combined sets are labelled assembled. Publisher answer keys are not official BPSC keys. Study notes are independently written and require medical editorial review. The 39th and 42nd medical collections remain incomplete.','sourceSHA256':hashlib.sha256((OUT/'live48.html').read_bytes()).hexdigest()}
(ROOT/'data/research/special-medical-coverage.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps(report,ensure_ascii=True))
