import {test} from 'node:test';
import assert from 'node:assert/strict';
import {screenRedundancy} from '../content-quality.js';
test('formatting and revision prefixes do not turn repeats into unique questions',()=>{
 const result=screenRedundancy([{id:'a',subject:'bangla',topic:'grammar',q:'শব্দ কী?'},{id:'b',subject:'bangla',topic:'grammar',q:'[রিভিশন] শব্দ কী !'}]);
 assert.deepEqual(result.exact,[['a','b']]);
});
test('merely swapping values in a calculation is flagged, not counted as new coverage',()=>{
 const result=screenRedundancy([{id:'a',subject:'math',topic:'শতকরা',q:'৫০০ টাকার ১০% কত?'},{id:'b',subject:'math',topic:'শতকরা',q:'800 টাকার 20% কত?'}]);
 assert.deepEqual(result.parameterVariants,[['a','b']]);
});
test('different learning objectives remain visible for editorial review',()=>{
 const result=screenRedundancy([{id:'a',subject:'medical',topic:'Anatomy',q:'Identify the nerve.',learningObjective:'phrenic-roots'},{id:'b',subject:'medical',topic:'Anatomy',q:'Identify the muscle.',learningObjective:'diaphragm-function'}]);
 assert.equal(result.exact.length,0);assert.equal(result.sharedObjectives.length,0);assert.equal(result.missingObjectives.length,0);
});
