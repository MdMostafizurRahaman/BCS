let bank=[], index=0, answered=0, correct=0, wrongSet=new Set(), locked=false;
const $=id=>document.getElementById(id);
async function init(){
  bank=await fetch('questions.json').then(r=>r.json());
  const saved=JSON.parse(localStorage.getItem('bcs-progress')||'{}');
  answered=saved.answered||0; correct=saved.correct||0; wrongSet=new Set(saved.wrong||[]);
  $('total').textContent=bank.length; updateStats(); render();
}
function save(){localStorage.setItem('bcs-progress',JSON.stringify({answered,correct,wrong:[...wrongSet]}))}
function updateStats(){ $('answered').textContent=answered; $('correct').textContent=correct; $('score').textContent=(answered?Math.round(correct/answered*100):0)+'%'; $('progressBar').style.width=Math.min(100,answered/bank.length*100)+'%';}
function render(){
  locked=false;$('explanation').classList.add('hidden');$('nextBtn').classList.add('hidden');$('status').textContent='';
  const x=bank[index]; $('qno').textContent=`প্রশ্ন ${index+1} / ${bank.length}`;$('question').textContent=x.q;
  $('options').innerHTML='';
  x.o.forEach((opt,i)=>{const b=document.createElement('button');b.className='option';b.textContent=`${String.fromCharCode(2453+i)}) ${opt}`;b.onclick=()=>answer(i);$('options').appendChild(b)})
}
function answer(choice){
 if(locked)return;locked=true;answered++;const x=bank[index];const buttons=[...document.querySelectorAll('.option')];
 buttons.forEach((b,i)=>{b.classList.add('disabled');if(i===x.a)b.classList.add('correct');if(i===choice&&choice!==x.a)b.classList.add('wrong')});
 if(choice===x.a){correct++;$('status').textContent='✓ সঠিক';$('status').style.color='#1e7a4b'}
 else{wrongSet.add(index);$('status').textContent='✗ ভুল';$('status').style.color='#c53d3d'}
 $('explanation').innerHTML=`<b>সঠিক উত্তর:</b> ${String.fromCharCode(2453+x.a)}) ${x.o[x.a]}<br><br><b>ব্যাখ্যা:</b> ${x.e}`;
 $('explanation').classList.remove('hidden');$('nextBtn').classList.remove('hidden');updateStats();save();
}
$('nextBtn').onclick=()=>{index=(index+1)%bank.length;render()};
$('randomBtn').onclick=()=>{index=Math.floor(Math.random()*bank.length);render()};
$('allBtn').onclick=()=>{index=0;render()};
$('wrongBtn').onclick=()=>{const a=[...wrongSet];if(!a.length){alert('এখনও কোনো ভুল প্রশ্ন নেই।');return}index=a[Math.floor(Math.random()*a.length)];render()};
$('resetBtn').onclick=()=>{if(confirm('Progress reset করবে?')){answered=0;correct=0;wrongSet.clear();save();updateStats();index=0;render()}};
init();
