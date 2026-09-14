"""Bounded responsiveness fixes, plus frame-synchronized browser checks."""
from pathlib import Path
import hashlib, platform
h=lambda s:hashlib.sha256(s.encode()).hexdigest()
p=Path('Luna-Line.html');s=p.read_text()
assert h(s)=='376435ad79488a06d8002cdd4ea570f8038385c9f78648f52eef9d90480ba295'
old='let dt=Math.min(1,(now-last)/1000||0);'
assert old in s
s=s.replace(old,'let dt=Math.max(0,(now-last)/1000||0);')
old='if(!renderNeeded&&!running&&!animate)return;renderNeeded=false;'
assert old in s
s=s.replace(old,"if(!renderNeeded&&!running&&!animate)return;if(Luna.gpu.mode==='webgpu'&&Luna.gpu.pending)return;renderNeeded=false;")
old='device.queue.submit([enc.finish()]);Luna.gpu.frames++}'
assert old in s
s=s.replace(old,"device.queue.submit([enc.finish()]);Luna.gpu.frames++;Luna.gpu.pending=true;device.queue.onSubmittedWorkDone().then(()=>{Luna.gpu.pending=false}).catch(e=>{Luna.gpu.pending=false;Luna.gpu.error=String(e);fallback();renderNeeded=true})}")
assert h(s)=='cba13c87caf3cf2cfb02567d019b4fed6cf9f2af9d56005e78b4f12042f985ec'
p.write_text(s);print('RUNTIME',len(s.encode()),h(s))
q=Path('qa/atelier/run-qa.py');t=q.read_text()
assert h(t)=='e8aecfc68b8ede9545d0612966555a92806369a8befcbcecc22faee3a8981dc9'
if platform.system()=='Darwin':
    a=t.index('    launch=');b=t.index('\n    if args.browser:',a)
    t=t[:a]+"    launch={'headless':True,'args':['--enable-unsafe-webgpu','--ignore-gpu-blocklist']}"+t[b:]
t=t.replace("def settle(ms=170):page.wait_for_timeout(ms)", "def settle(ms=170):\n        page.wait_for_timeout(ms)\n        page.wait_for_function('Luna.line.playing || Luna.detail.cfg.process || (!renderNeeded && !Luna.gpu.pending)',timeout=30000)")
t=t.replace("coords=ev('(()=>", "settle(350)\n        coords=ev('(()=>")
t=t.replace("for q in coords:page.mouse.click(q['x'],q['y']);settle(300)", "pick_targets=ev('(qs)=>qs.map(q=>({x:q.x,y:q.y,target:document.elementFromPoint(q.x,q.y)?.id}))',coords)\n        print('PICK_TARGETS',json.dumps(pick_targets),flush=True)\n        for q in coords:page.mouse.click(q['x'],q['y']);settle(300)")
t=t.replace("setv('reverse',True);page.keyboard.press('Space');settle(1000);page.keyboard.press('Space');check", "setv('reverse',True);page.locator('#play').focus();page.keyboard.press('Space');page.wait_for_function('Luna.line.seconds<21.5',timeout=15000);page.keyboard.press('Space');check")
t=t.replace("setv('loop',True);page.keyboard.press('Space');settle(700);page.keyboard.press('Space');check", "setv('loop',True);page.locator('#play').focus();page.keyboard.press('Space');page.wait_for_function('Luna.line.seconds<3',timeout=15000);page.keyboard.press('Space');check")
t=t.replace("page.locator('#shotButton').click();settle(1300);capture=", "page.locator('#shotButton').click();page.wait_for_function('Luna.detail.lastCapture?.bytes>0',timeout=30000);capture=")
t=t.replace("start=time.monotonic();page.keyboard.press('Space');", "page.locator('#play').focus();start=time.monotonic();page.keyboard.press('Space');")
t=t.replace("'browserVersion':browser.version,", "'browserVersion':browser.version,'runtimeSha256':hashlib.sha256(Path('Luna-Line.html').read_bytes()).hexdigest(),'adapter':ev('Luna.gpu.adapter||null'),")
q.write_text(t);print('RUNNER',h(t))
