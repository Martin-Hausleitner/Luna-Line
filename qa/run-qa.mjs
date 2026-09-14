// Dependency-free CDP QA. Node 22+ and an installed Chromium/Chrome.
import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import os from 'node:os';
import crypto from 'node:crypto';
import {spawn} from 'node:child_process';
const root=path.resolve(import.meta.dirname,'..');
const arg=process.argv.slice(2),baseArg=arg.find(a=>a.startsWith('--base='))?.slice(7),live=!!baseArg,full=arg.includes('--full');
const out=path.join(root,'qa',live?'live':'');fs.mkdirSync(out,{recursive:true});
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const report={started:new Date().toISOString(),environment:{platform:os.platform(),arch:os.arch(),node:process.version},viewport:{width:1920,height:1080},sourceSHA256:crypto.createHash('sha256').update(fs.readFileSync(path.join(root,'Luna-Line.html'))).digest('hex'),tests:[],shots:[],errors:[],requests:[]};
let server,browser,socket;const pending=new Map();let id=0;
function test(name,ok,detail){report.tests.push({name,status:ok?'PASS':'FAIL',detail});if(!ok)console.error('FAIL',name,detail);else console.log('PASS',name);}
function send(method,params={}){return new Promise((resolve,reject)=>{let n=++id,t=setTimeout(()=>{pending.delete(n);reject(Error('CDP timeout '+method))},30000);pending.set(n,{resolve,reject,t});socket.send(JSON.stringify({id:n,method,params}));})}
async function evaluate(expression){let r=await send('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});if(r.exceptionDetails)throw Error(JSON.stringify(r.exceptionDetails));return r.result.value;}
async function wait(expression,timeout=35000){let start=Date.now();while(Date.now()-start<timeout){try{if(await evaluate(expression))return;}catch{}await sleep(160);}throw Error('Wait timeout '+expression);}
async function key(key,code=key){let vk=key===' '?32:key.toUpperCase().charCodeAt(0);await send('Input.dispatchKeyEvent',{type:'keyDown',key,code,windowsVirtualKeyCode:vk});await send('Input.dispatchKeyEvent',{type:'keyUp',key,code,windowsVirtualKeyCode:vk});}
async function shot(name){await sleep(350);let r=await send('Page.captureScreenshot',{format:'png',captureBeyondViewport:false,fromSurface:true});let b=Buffer.from(r.data,'base64');fs.writeFileSync(path.join(out,name),b);report.shots.push({name,bytes:b.length,sha256:crypto.createHash('sha256').update(b).digest('hex'),state:await evaluate('Luna.inspect.snapshot()')});console.log('SHOT',name,b.length);}
try{
 let base=baseArg;
 if(!base){server=http.createServer((req,res)=>{if(req.url?.startsWith('/favicon')){res.writeHead(204);res.end();return}res.writeHead(200,{'Content-Type':'text/html; charset=utf-8','Cache-Control':'no-store'});res.end(fs.readFileSync(path.join(root,'Luna-Line.html')));});await new Promise(r=>server.listen(0,'127.0.0.1',r));base='http://127.0.0.1:'+server.address().port+'/Luna-Line.html';}
 report.base=base;
 const chrome=process.env.CHROME_PATH||(os.platform()==='darwin'?'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome':'/usr/bin/chromium');
 const port=9600+process.pid%400,profile=fs.mkdtempSync(path.join(os.tmpdir(),'luna-line-qa-'));
 browser=spawn(chrome,['--headless=new','--no-first-run','--no-default-browser-check','--disable-background-networking','--enable-unsafe-webgpu','--remote-debugging-port='+port,'--user-data-dir='+profile,'--window-size=1920,1080','about:blank'],{stdio:['ignore','ignore','pipe']});
 let logs='';browser.stderr.on('data',d=>logs+=d.toString());let endpoints;
 for(let n=0;n<100;n++){try{endpoints=await (await fetch('http://127.0.0.1:'+port+'/json/list')).json();if(endpoints.length)break}catch{}await sleep(150)}
 if(!endpoints?.length)throw Error('Chrome did not launch: '+logs.slice(-3000));
 socket=new WebSocket(endpoints.find(e=>e.type==='page').webSocketDebuggerUrl);await new Promise((r,j)=>{socket.onopen=r;socket.onerror=j});socket.onmessage=e=>{let d=JSON.parse(e.data);if(d.id&&pending.has(d.id)){let p=pending.get(d.id);clearTimeout(p.t);pending.delete(d.id);d.error?p.reject(Error(JSON.stringify(d.error))):p.resolve(d.result);}else if(d.method==='Runtime.exceptionThrown')report.errors.push(d.params.exceptionDetails);else if(d.method==='Network.requestWillBeSent')report.requests.push(d.params.request.url);};
 await send('Page.enable');await send('Runtime.enable');await send('Network.enable');await send('Emulation.setDeviceMetricsOverride',{width:1920,height:1080,deviceScaleFactor:1,mobile:false});
 await send('Page.navigate',{url:base+(base.includes('?')?'&':'?')+'station=1'});await wait('window.Luna?.gpu.ready && Luna.gpu.frames>0');await sleep(2000);
 report.browser=await send('Browser.getVersion');report.adapter=await evaluate('Luna.gpu.adapter||null');report.initial=await evaluate('Luna.inspect.snapshot()');
 test('Native WebGPU rendering',report.initial.renderer==='webgpu',report.initial);
 test('CEO overlay off on startup',await evaluate('getComputedStyle(document.getElementById("ceo")).display==="none"'));
 test('Single runtime / shared contracts',await evaluate('!!Luna.theme&&!!Luna.gpu&&!!Luna.cam&&Luna.line.id==="TA2026-00009-T04"&&Luna.store.key==="luna.line.v1"'));
 let names=['01-lager.png','02-cut.png','03-edge.png','04-press.png','05-crate.png','06-evening.png'];
 for(let i=0;i<6;i++){await evaluate('Luna.inspect.jump('+i+')');await sleep(400);if(!live||i===1||i===5)await shot(names[i]);test('Station '+(i+1)+' / readable identity',await evaluate('Luna.line.station==='+i+'&&document.getElementById("inscription").innerText.includes("TA2026-00009")&&document.querySelectorAll(".station[aria-current=true]").length===1'));}
 if(!live){await evaluate('Luna.inspect.overview()');await shot('07-full-line.png');test('All six station ticks in frame',await evaluate('[...document.querySelectorAll(".station")].every(e=>{let r=e.getBoundingClientRect();return r.left>=0&&r.right<=innerWidth&&r.bottom<=innerHeight})'));}
 await key('c','KeyC');test('C shows 4.2 / 5.0 Soll',await evaluate('getComputedStyle(document.getElementById("ceo")).display!=="none"&&document.getElementById("ceo").innerText.includes("4,2 h")'));await key('c','KeyC');
 await key('2','Digit2');await sleep(2200);test('Key 2 jumps to cut',await evaluate('Luna.line.station===1&&!Luna.line.playing'));
 await key(' ','Space');let start=await evaluate('Luna.line.seconds');await sleep(1300);await key(' ','Space');let end=await evaluate('Luna.line.seconds');test('Space plays and pauses',end>start+.5&&await evaluate('!Luna.line.playing'),{start,end});
 let paused=await evaluate('Luna.line.seconds');await sleep(450);test('Paused time remains frozen',Math.abs((await evaluate('Luna.line.seconds'))-paused)<.001);
 await evaluate('Luna.store.save()');test('Local persistence version/id',await evaluate('(()=>{let s=JSON.parse(localStorage.getItem("luna.line.v1"));return s.version===1&&s.id==="TA2026-00009-T04"})()'));
 test('No external runtime requests',report.requests.filter(u=>!u.startsWith(base.split('?')[0])&&!u.startsWith('data:')&&!u.includes('/favicon')).length===0,report.requests);
 if(full&&!live){await evaluate('Luna.inspect.seek(0)');await key(' ','Space');let realStart=Date.now();await wait('Luna.line.seconds>=60&&!Luna.line.playing',70000);test('One real 60-second playback',Math.abs((Date.now()-realStart)/1000-60)<3,{wallSeconds:(Date.now()-realStart)/1000,end:await evaluate('Luna.inspect.snapshot()')});
  await send('Page.navigate',{url:base+'?renderer=2d&station=5'});await wait('window.Luna?.gpu.ready&&Luna.gpu.frames>0');await sleep(500);await shot('08-fallback.png');test('Canvas2D fallback not blank',await evaluate('Luna.gpu.mode==="canvas2d"&&Luna.gpu.frames>0'));await key(' ','Space');let s=await evaluate('Luna.line.seconds');await sleep(1100);await key(' ','Space');test('Canvas2D moving journey',await evaluate('Luna.line.seconds')>s+.5);
  await send('Page.navigate',{url:base+'?station=6'});await wait('window.Luna?.gpu.ready');await send('Emulation.setDeviceMetricsOverride',{width:390,height:844,deviceScaleFactor:1,mobile:true});await sleep(800);await shot('09-mobile.png');test('Mobile ticks and inscription fit',await evaluate('document.documentElement.scrollWidth===innerWidth&&[...document.querySelectorAll(".station")].every(e=>{let r=e.getBoundingClientRect();return r.right<=innerWidth+1&&r.left>=0})'));}
 test('No uncaught browser errors',report.errors.length===0,report.errors);
 report.status=report.tests.every(t=>t.status==='PASS')?'PASS':'FAIL';
}catch(e){report.status='FAIL';report.errors.push(String(e.stack||e));console.error(e);}finally{report.finished=new Date().toISOString();fs.writeFileSync(path.join(out,'report.json'),JSON.stringify(report,null,2));try{await send('Browser.close')}catch{}socket?.close();browser?.kill();server?.close();console.log(JSON.stringify({status:report.status,tests:report.tests.length,shots:report.shots.length,report:path.join(out,'report.json'),errors:report.errors}));}
