export const SUBJECTS = [
 {id:'medical',name:'মেডিকেল সায়েন্স',en:'Medical Science',icon:'✚',marks:100,color:'#eaf4ee',tone:'#307657'},
 {id:'bangla',name:'বাংলা ভাষা ও সাহিত্য',en:'Bangla',icon:'অ',marks:20,color:'#f9efe9',tone:'#b47954'},
 {id:'english',name:'ইংরেজি ভাষা ও সাহিত্য',en:'English',icon:'Aa',marks:20,color:'#edf1fa',tone:'#617eaf'},
 {id:'bangladesh',name:'বাংলাদেশ বিষয়াবলি',en:'Bangladesh Affairs',icon:'◎',marks:20,color:'#f1eef9',tone:'#9376ac'},
 {id:'international',name:'আন্তর্জাতিক বিষয়াবলি',en:'International Affairs',icon:'⊕',marks:20,color:'#eaf4f6',tone:'#5c98a2'},
 {id:'math',name:'গাণিতিক যুক্তি',en:'Mathematical Reasoning',icon:'∑',marks:10,color:'#fbf4e8',tone:'#b28e49'},
 {id:'mental',name:'মানসিক দক্ষতা',en:'Mental Ability',icon:'◇',marks:10,color:'#f7edf1',tone:'#ae728b'}
];
export const MEDICAL_MARKS = {'Anatomy':12,'Physiology':13,'Biochemistry':5,'Pharmacology':5,'Forensic Medicine':5,'Community Medicine':5,'Pathology':5,'Medicine':17,'Surgery':17,'Obstetrics & Gynaecology':16};
export const SYLLABUS_URL='https://bpsc.portal.gov.bd/sites/default/files/files/bpsc.portal.gov.bd/psc_exam/2ece87ae_8b68_40a5_93e5_0b4c425e35e6/বিসিএস%20%28বিশেষ%29%20পরীক্ষা-২০২৫%20%20এর%20সিলেবাস.pdf';
export const emptyState=()=>({version:2,answers:{},bookmarks:[],history:[],activity:{},goal:20,imports:[],theme:'light'});
export function validateQuestion(q){
 return q && typeof q.id==='string' && q.id.length>0 && typeof q.q==='string' && q.q.trim().length>0 && Array.isArray(q.o) && q.o.length===4 && q.o.every(x=>typeof x==='string'&&x.trim()) && new Set(q.o).size===4 && Number.isInteger(q.a) && q.a>=0 && q.a<4 && typeof q.e==='string' && q.e.trim().length>0 && SUBJECTS.some(s=>s.id===q.subject) && typeof q.topic==='string' && q.topic.trim() && ['practice','past'].includes(q.type) && (q.type!=='past'||(typeof q.paper==='string'&&q.paper.trim()&&Number.isInteger(q.year)&&q.year>=1972&&q.year<=2100&&safeURL(q.source)));
}
export function safeURL(url){try{const u=new URL(url);return ['https:','http:'].includes(u.protocol)?u.href:null}catch{return null}}
export function validateBank(data){
 if(!Array.isArray(data)||!data.length||data.length>20000)throw Error('১–২০,০০০ প্রশ্নের JSON array প্রয়োজন।');
 const ids=new Set(),texts=new Set();
 data.forEach((q,i)=>{if(!validateQuestion(q))throw Error(`প্রশ্ন ${i+1}: schema, ৪টি ভিন্ন option, answer, explanation বা source ঠিক নেই।`);if(ids.has(q.id)||texts.has(q.q.trim()))throw Error(`প্রশ্ন ${i+1}: একই ID বা প্রশ্ন একাধিকবার আছে।`);ids.add(q.id);texts.add(q.q.trim())});return data;
}
export function filterBank(bank,f={}){const search=f.search?.toLowerCase();return bank.filter(q=>(!f.subject||q.subject===f.subject)&&(!f.topic||q.topic===f.topic)&&(!f.subtopic||q.subtopic===f.subtopic)&&(!f.collection||(f.collection==='authored'?!q.collection:q.collection===f.collection))&&(!search||`${q.q} ${q.e} ${q.topic} ${q.subtopic||''}`.toLowerCase().includes(search))&&(!f.type||q.type===f.type)&&(!f.paper||q.paper===f.paper));}
export function shuffle(items,random=Math.random){const out=[...items];for(let i=out.length-1;i>0;i--){const j=Math.floor(random()*(i+1));[out[i],out[j]]=[out[j],out[i]]}return out}
export function scoreExam(questions,answers,penalty=.5){let correct=0,wrong=0;questions.forEach(q=>{if(Number.isInteger(answers[q.id])){if(answers[q.id]===q.a)correct++;else wrong++}});return {correct,wrong,skipped:questions.length-correct-wrong,score:correct-wrong*penalty,total:questions.length};}
export function fullMock(bank){const result=[];for(const s of SUBJECTS){const pool=bank.filter(q=>q.subject===s.id);if(pool.length<s.marks)return null;if(s.id==='medical'){for(const [topic,marks] of Object.entries(MEDICAL_MARKS)){const sub=pool.filter(q=>q.topic===topic);if(sub.length<marks)return null;result.push(...shuffle(sub).slice(0,marks))}}else result.push(...shuffle(pool).slice(0,s.marks))}return result;}
export function dayKey(d=new Date()){return new Intl.DateTimeFormat('en-CA',{timeZone:'Asia/Dhaka',year:'numeric',month:'2-digit',day:'2-digit'}).format(d)}
export function recordAnswer(state,q,choice){const old=state.answers[q.id];const right=choice===q.a;state.answers[q.id]={choice,correct:right,attempts:(old?.attempts||0)+1,at:Date.now(),due:Date.now()+(right?3:1)*86400000};const key=dayKey();state.activity[key]=(state.activity[key]||0)+1;return right;}
