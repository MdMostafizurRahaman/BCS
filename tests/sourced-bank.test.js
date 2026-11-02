import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,existsSync} from 'node:fs';
import {filterBank,MEDICAL_MARKS} from '../core.js';
const bank=JSON.parse(readFileSync(new URL('../questions.json',import.meta.url),'utf8'));
const supplemental=JSON.parse(readFileSync(new URL('../data/supplemental-medmcqa.json',import.meta.url),'utf8'));
const all=[...bank,...supplemental];
test('separate 10,000 supplemental questions are attributed and never misrepresented as BCS papers',()=>{
 assert.equal(supplemental.length,10000);
 for(const q of supplemental){assert.equal(q.type,'practice');assert.equal(q.editorial,'dataset-sourced-unreviewed');assert.equal(q.provenance.split,'train');assert.ok(q.provenance.upstreamID);assert.ok(q.source.startsWith('https://huggingface.co/'));assert.ok(q.e.length>=180);assert.equal(q.year,undefined);}
 for(const topic of Object.keys(MEDICAL_MARKS))assert.equal(supplemental.filter(q=>q.topic===topic).length,1000);
});
test('source and subtopic filters return precisely the matching collection',()=>{
 const q=supplemental[0];const result=filterBank(all,{subject:'medical',topic:q.topic,subtopic:q.subtopic,collection:'medmcqa'});
 assert.ok(result.length);assert.ok(result.every(x=>x.topic===q.topic&&x.subtopic===q.subtopic&&x.collection==='medmcqa'));
 assert.equal(filterBank(bank,{collection:'authored'}).length,264);
});
test('converted raw 1-based keys match every published dataset option',{skip:!existsSync(new URL('../artifacts/sources/awinml-medmcqa-train.json',import.meta.url))},()=>{
 const ids=new Map(supplemental.map(q=>[q.provenance.upstreamID,q]));
 const rows=readFileSync(new URL('../artifacts/sources/awinml-medmcqa-train.json',import.meta.url),'utf8').trim().split('\n');
 let checked=0;for(const line of rows){const r=JSON.parse(line);const q=ids.get(r.id);if(q){assert.equal(q.a,r.cop-1);checked++;}}
 assert.equal(checked,10000);
});
