import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,existsSync} from 'node:fs';
import {parseArchive,selectArchive,fullPaperAvailable} from '../archive-exams.js';
import {scoreExam} from '../core.js';
import {setArchive,buildArchiveExam,archiveMedicalQuestions} from '../archive-ui.js';
const row=(paper,n,subject='Bangla Language & Literature')=>({exam_slug:paper,question_number:n,question:`Question ${paper} ${n}`,option_a:'A answer',option_b:'B answer',option_c:'C answer',option_d:'D answer',correct_answer:'B',subject_en:subject,solve_note:'Explanation',question_image_paths:[],solve_note_image_paths:[]});
const exam=(slug,total=2)=>({slug,title:slug,date:'2021-02-26',total_questions:total,set_code:'A'});
const fixture=()=>({exams:[exam('35th_bcs'),exam('42nd_bcs')],questions:[row('35th_bcs',1),row('35th_bcs',2,'English Language & Literature'),row('42nd_bcs',1),row('42nd_bcs',2,'English Language & Literature')]});
test('year and subject selections cannot leak another paper or subject',()=>{const p=parseArchive(fixture());const q=selectArchive(p,{papers:['35th_bcs'],subjects:['bangla']});assert.equal(q.length,1);assert.equal(q[0].id,'archive-35th_bcs-1');assert.equal(q[0].a,1);});
test('multiple years and multiple subjects combine while respecting limits',()=>{const p=parseArchive(fixture());assert.equal(selectArchive(p,{papers:['35th_bcs','42nd_bcs'],subjects:['bangla']}).length,2);assert.equal(selectArchive(p,{papers:['35th_bcs','42nd_bcs'],limit:3}).length,3);assert.equal(selectArchive(p,{papers:[]}).length,0);});
test('general-only special BCS is never treated as a full medical paper',()=>{const p=parseArchive(fixture());assert.equal(fullPaperAvailable(p.find(x=>x.number===35)),true);assert.equal(fullPaperAvailable(p.find(x=>x.number===42)),false);});
test('a genuinely complete 100 medical + 100 general health paper enables its full exam',()=>{const p=parseArchive({exams:[exam('42nd_bcs',200)],questions:Array.from({length:200},(_,i)=>row('42nd_bcs',i+1,i<100?'Medical Science':'Bangla Language & Literature'))})[0];assert.equal(fullPaperAvailable(p),true);});
test('missing keys are excluded and prevent a full-set claim',()=>{const f=fixture();f.questions[0].correct_answer='';const p=parseArchive(f).find(x=>x.number===35);assert.equal(p.questions.length,1);assert.equal(p.complete,false);assert.deepEqual(p.excluded,[1]);assert.equal(fullPaperAvailable(p),false);});
test('duplicate original question numbers fail instead of corrupting exam identity',()=>{const f=fixture();f.questions.push({...f.questions[0]});assert.throws(()=>parseArchive(f));});
test('figures are preserved only from safe source paths, with a truthful missing-explanation message',()=>{const f=fixture();f.questions[0].question='';f.questions[0].question_image_paths=['images/35th_bcs/q1_img1.png','../../private.png'];f.questions[0].solve_note='';const q=parseArchive(f).find(x=>x.number===35).questions[0];assert.equal(q.images.length,1);assert.ok(q.images[0].startsWith('https://raw.githubusercontent.com/'));assert.match(q.e,/উৎসে/);});
test('mixed-year deduplication is optional and never changes original full-paper content',()=>{const f=fixture();f.questions[2].question=f.questions[0].question;const p=parseArchive(f);assert.equal(selectArchive(p,{papers:['35th_bcs','42nd_bcs'],dedupe:true}).length,3);assert.equal(selectArchive(p,{papers:['35th_bcs','42nd_bcs'],dedupe:false}).length,4);assert.equal(p.find(x=>x.number===35).questions.length,2);});
test('archive IDs grade correctly, including unanswered questions and negative marks',()=>{const qs=parseArchive(fixture()).find(x=>x.number===35).questions;assert.deepEqual(scoreExam(qs,{[qs[0].id]:0}),{correct:0,wrong:1,skipped:1,score:-.5,total:2});});
const local=new URL('../artifacts/sources/bcs-historical-analysis.json',import.meta.url);
test('local corpus supplies exactly 35 Bangla items for BCS 35 and 200 in its complete paper',{skip:!existsSync(local)},()=>{const p=parseArchive(JSON.parse(readFileSync(local,'utf8')));assert.equal(selectArchive(p,{papers:['35th_bcs'],subjects:['bangla']}).length,35);assert.equal(p.find(x=>x.number===35).questions.length,200);assert.equal(fullPaperAvailable(p.find(x=>x.number===35)),true);assert.equal(fullPaperAvailable(p.find(x=>x.number===48)),false);});

const special=new URL('../artifacts/sources/bcs-with-special-medical.json',import.meta.url);
test('Bangladesh medical supplement has 100 actual 48th questions, separate from Indian practice',{skip:!existsSync(special)},()=>{
 const raw=JSON.parse(readFileSync(special,'utf8'));setArchive(raw);
 const full=buildArchiveExam('48th_bcs','full'),medical=buildArchiveExam('48th_bcs','medical'),general=buildArchiveExam('48th_bcs','general');
 assert.equal(full.questions.length,200);assert.match(full.title,/সমন্বিত/);
 assert.equal(medical.questions.length,100);assert.ok(medical.questions.every(q=>q.subject==='medical'&&q.year===2025&&q.source==='https://web.livemcq.com/blog/48th-special-bcs-question-pdf'));
 assert.deepEqual(medical.questions.map(q=>q.printedNumber),Array.from({length:100},(_,i)=>i+101));
 assert.equal(general.questions.length,100);assert.ok(general.questions.every(q=>q.subject!=='medical'));
 assert.ok(medical.questions.every(q=>q.e.length>50&&q.collection!=='medmcqa'));
 assert.match(medical.questions.find(q=>q.printedNumber===135).e,/not a current standalone/);
 assert.match(medical.questions.find(q=>q.printedNumber===185).e,/not a current treatment recommendation/);
 assert.equal(archiveMedicalQuestions().length,108);
});
test('partial 39th and 42nd medical collections remain usable without enabling fabricated full papers',{skip:!existsSync(special)},()=>{
 setArchive(JSON.parse(readFileSync(special,'utf8')));
 for(const [paper,n] of [['39th_bcs',7],['42nd_bcs',1]]){
  assert.equal(buildArchiveExam(paper,'medical').questions.length,n);
  assert.ok(buildArchiveExam(paper,'general').questions.every(q=>q.subject!=='medical'));
  assert.throws(()=>buildArchiveExam(paper,'full'));
 }
});
