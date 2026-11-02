// Local personal-study adapter. Publisher data is not bundled or publicly deployed.
export const ARCHIVE_SUBJECTS=[
 ['bangla','বাংলা ভাষা ও সাহিত্য','Bangla Language & Literature'],['english','ইংরেজি ভাষা ও সাহিত্য','English Language & Literature'],
 ['bangladesh','বাংলাদেশ বিষয়াবলি','Bangladesh Affairs'],['international','আন্তর্জাতিক বিষয়াবলি','International Affairs'],
 ['math','গাণিতিক যুক্তি','Mathematical Reasoning'],['mental','মানসিক দক্ষতা','Mental Ability'],
 ['science','সাধারণ বিজ্ঞান','General Science'],['ict','কম্পিউটার ও তথ্যপ্রযুক্তি','Computer & Information Technology'],
 ['geography','ভূগোল ও পরিবেশ','Geography, Environment & Disaster Management'],['ethics','নৈতিকতা ও সুশাসন','Ethics, Values & Good Governance'],['medical','মেডিকেল সায়েন্স','Medical Science']
].map(([id,name,en])=>({id,name,en}));
const byEnglish=new Map(ARCHIVE_SUBJECTS.map(x=>[x.en,x]));
const text=s=>typeof s==='string'?s.trim():'';
const asset=path=>typeof path==='string'&&/^images\/[\w-]+\/[\w.-]+\.(png|jpe?g|webp)$/i.test(path)?'https://raw.githubusercontent.com/SangbitDas/bcs-dataset/main/'+path:null;
export function parseArchive(data){
 if(!data||!Array.isArray(data.exams)||!Array.isArray(data.questions)||data.questions.length>30000)throw Error('পরীক্ষা ও প্রশ্নসহ সঠিক archive JSON প্রয়োজন।');
 const papers=new Map(),ids=new Set();
 for(const e of data.exams){if(!/^[\w-]+$/.test(e.slug)||papers.has(e.slug)||!Number.isInteger(e.total_questions)||e.total_questions<1||e.total_questions>500)throw Error('পরীক্ষার metadata ঠিক নেই।');const number=Number(e.slug.match(/^\d+/)?.[0]);papers.set(e.slug,{id:e.slug,title:text(e.title)||e.slug,date:text(e.date),number,setCode:text(e.set_code),assembled:e.assembled===true,expected:e.total_questions,scope:[39,42,48,49].includes(number)?'general':'paper',questions:[],excluded:[],originalScanVerified:false});}
 for(const r of data.questions){const p=papers.get(r.exam_slug);if(!p)throw Error('প্রশ্নের পরীক্ষা খুঁজে পাওয়া যায়নি।');const id=`archive-${p.id}-${r.question_number}`;
  if(!Number.isInteger(r.question_number)||r.question_number<1||ids.has(id))throw Error('একই paper-এর প্রশ্ন নম্বর একাধিকবার আছে।');ids.add(id);
  const images=(r.question_image_paths||[]).map(asset).filter(Boolean),solutionImages=(r.solve_note_image_paths||[]).map(asset).filter(Boolean);
  const subject=byEnglish.get(r.subject_en),o=['a','b','c','d'].map(k=>text(r['option_'+k])),a=/^[ABCD]$/.test(r.correct_answer)?'ABCD'.indexOf(r.correct_answer):-1;
  if(!subject||a<0||o.some(v=>!v)||(!text(r.question)&&!images.length)){p.excluded.push(r.question_number);continue;}
  p.questions.push({id,q:text(r.question)||'প্রশ্নের চিত্র দেখুন।',o,a,e:text(r.solve_note)||'উৎসে এই প্রশ্নের লিখিত ব্যাখ্যা নেই। উত্তরটি প্রকাশিত সংগ্রহের key অনুযায়ী দেখানো হয়েছে; স্বাধীন যাচাই বাকি।',subject:subject.id,topic:text(r.medical_topic)||subject.name,type:'past',collection:'local-archive',paper:p.title,paperId:p.id,year:Number(p.date.slice(0,4)),originalNumber:r.question_number,printedNumber:r.printed_question_number??(p.assembled?null:r.question_number),images,solutionImages,source:/^https?:\/\//.test(r.source_url||'')?r.source_url:'https://github.com/SangbitDas/bcs-dataset',editorial:'publisher-transcription-unverified'});
 }
 for(const p of papers.values()){p.questions.sort((a,b)=>a.originalNumber-b.originalNumber);p.complete=p.questions.length===p.expected&&p.excluded.length===0&&p.questions.every((q,i)=>q.originalNumber===i+1);if([39,42,48].includes(p.number)&&p.complete&&p.expected===200&&p.questions.filter(q=>q.subject==='medical').length===100)p.scope='paper';}
 return [...papers.values()].sort((a,b)=>b.number-a.number);
}
export function selectArchive(papers,{papers:paperIds=[],subjects=[],limit=0,order='original',dedupe=false}={}){
 if(!paperIds.length)return [];
 const chosen=paperIds.map(id=>papers.find(p=>p.id===id)).filter(Boolean);
 let qs=chosen.flatMap(p=>p.questions.filter(q=>!subjects.length||subjects.includes(q.subject)));
 if(dedupe){const seen=new Set();qs=qs.filter(q=>{const key=q.q.normalize('NFKC').toLowerCase().replace(/[\p{P}\p{S}\s]/gu,'')+q.images.join('');if(seen.has(key))return false;seen.add(key);return true;});}
 if(order==='random'){qs=[...qs];for(let i=qs.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[qs[i],qs[j]]=[qs[j],qs[i]];}}
 return limit>0?qs.slice(0,limit):qs;
}
export function fullPaperAvailable(paper){return Boolean(paper?.complete&&paper.scope==='paper');}
export function archiveTitle(papers,selection){const chosen=papers.filter(p=>selection.papers.includes(p.id));const part=selection.subjects.length?selection.subjects.map(id=>ARCHIVE_SUBJECTS.find(s=>s.id===id)?.name||id).join(' + '):'সব উপলব্ধ বিষয়';return `${chosen.map(p=>p.title).join(' + ')} · ${part}`;}
