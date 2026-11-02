import {readFileSync,writeFileSync,mkdirSync} from 'node:fs';
import {SUBJECTS,validateBank} from '../core.js';
import {screenRedundancy} from '../content-quality.js';
const bank=validateBank(JSON.parse(readFileSync(new URL('../questions.json',import.meta.url),'utf8')));
const normalize=text=>text.normalize('NFKC').toLowerCase().replace(/\[রিভিশন\]/g,'').replace(/[\p{P}\p{S}\s]/gu,'');
const byStem=new Map();
for(const q of bank){const key=normalize(q.q);byStem.set(key,[...(byStem.get(key)||[]),q.id]);}
const duplicates=[...byStem.values()].filter(ids=>ids.length>1);
const redundancy=screenRedundancy(bank);
const topics=SUBJECTS.flatMap(subject=>[...new Set(bank.filter(q=>q.subject===subject.id).map(q=>q.topic))].map(topic=>{
 const qs=bank.filter(q=>q.subject===subject.id&&q.topic===topic);
 const reviewed=qs.filter(q=>q.editorial==='reviewed'&&q.review?.reviewer&&q.review?.at&&q.review?.reference&&q.learningObjective&&q.patternEvidence?.length);
 return {subject:subject.id,topic,target:500,total:qs.length,reviewed:reviewed.length,remaining:Math.max(0,500-reviewed.length),ready:reviewed.length>=500};
}));
const papers=[39,42,48].map(exam=>{const qs=bank.filter(q=>q.type==='past'&&q.examNumber===exam);const verified=qs.filter(q=>q.provenance?.originalScan&&q.provenance?.page&&q.provenance?.questionNumber&&q.provenance?.transcriptionChecked&&q.provenance?.answerChecked);return {exam,total:qs.length,verified:verified.length,required:200,ready:verified.length===200};});
const report={schema:1,generatedAt:new Date().toISOString(),targetPerTopic:500,minimumTarget:topics.length*500,activeQuestions:bank.length,reviewedQuestions:topics.reduce((n,t)=>n+t.reviewed,0),topics,papers,normalizedDuplicateGroups:duplicates,redundancy,complete:topics.every(t=>t.ready)&&papers.every(p=>p.ready)&&duplicates.length===0&&redundancy.parameterVariants.length===0&&redundancy.missingObjectives.length===0};
mkdirSync(new URL('../data/research/',import.meta.url),{recursive:true});
writeFileSync(new URL('../data/research/coverage.json',import.meta.url),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify({topics:topics.length,target:report.minimumTarget,active:bank.length,reviewed:report.reviewedQuestions,verifiedPapers:papers.filter(p=>p.ready).length,complete:report.complete},null,2));
if(process.argv.includes('--require-complete')&&!report.complete)process.exitCode=1;
