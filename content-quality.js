// Screening aids, not a substitute for subject-level semantic review.
export function canonicalStem(text){return text.normalize('NFKC').toLowerCase().replace(/\[রিভিশন\]/g,'').replace(/[\p{P}\p{S}\s]/gu,'');}
function parameterStem(q){
 const text=q.q.normalize('NFKC').toLowerCase();
 return text.replace(/[০-৯]/g,c=>String(c.charCodeAt(0)-0x09e6)).replace(/\d+(?:[.,/]\d+)*/g,'#').replace(/\s+/g,' ').trim();
}
export function screenRedundancy(bank){
 const exact=new Map(),parameters=new Map(),objectives=new Map();
 for(const q of bank){
  const stem=canonicalStem(q.q);exact.set(stem,[...(exact.get(stem)||[]),q.id]);
  if(['math','mental'].includes(q.subject)){
   const key=`${q.subject}:${q.topic}:${parameterStem(q)}`;
   parameters.set(key,[...(parameters.get(key)||[]),q.id]);
  }
  if(q.learningObjective){const key=`${q.subject}:${q.topic}:${q.learningObjective}`;objectives.set(key,[...(objectives.get(key)||[]),q.id]);}
 }
 return {exact:[...exact.values()].filter(ids=>ids.length>1),parameterVariants:[...parameters.values()].filter(ids=>ids.length>1),sharedObjectives:[...objectives.values()].filter(ids=>ids.length>1),missingObjectives:bank.filter(q=>!q.learningObjective).map(q=>q.id)};
}
