#!/usr/bin/env python3
"""Browser acceptance for the actual single-file runtime. Test dependencies are not runtime dependencies."""
import argparse, hashlib, json, math, sys, time
from datetime import datetime, timezone
from pathlib import Path
from playwright.sync_api import sync_playwright

parser=argparse.ArgumentParser()
parser.add_argument('--url',default='http://127.0.0.1:8088/Luna-Line.html')
parser.add_argument('--output',default='qa/atelier')
parser.add_argument('--require-webgpu',action='store_true')
parser.add_argument('--live',action='store_true')
parser.add_argument('--set-content',help='Exercise DOM and Canvas2D where navigation is restricted; not a WebGPU claim.')
parser.add_argument('--browser',help='Optional browser executable path.')
args=parser.parse_args();out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
results=[];errors=[];shots=[];requests=[]
def record(name,ok,detail=None):
    result={'name':name,'status':'PASS' if ok else 'FAIL','detail':detail};results.append(result)
    print(result['status'],name,flush=True)

def skipped(name,detail):
    results.append({'name':name,'status':'UNVERIFIED','detail':detail});print('UNVERIFIED',name,flush=True)

with sync_playwright() as p:
    launch={'headless':True,'args':['--enable-unsafe-webgpu','--ignore-gpu-blocklist']}
    if args.browser:launch['executable_path']=args.browser
    browser=p.chromium.launch(**launch)
    context=browser.new_context(viewport={'width':1920,'height':1080},device_scale_factor=1,accept_downloads=True)
    page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)));page.on('request',lambda r:requests.append(r.url))
    if args.set_content:page.set_content(Path(args.set_content).read_text(),wait_until='load')
    else:page.goto(args.url,wait_until='networkidle',timeout=60000)
    page.wait_for_function('window.Luna?.gpu.ready',timeout=60000);page.wait_for_timeout(1200)
    def ev(code,arg=None):return page.evaluate(code,arg)
    def settle(ms=170):
        page.wait_for_timeout(ms)
        page.wait_for_function('Luna.line.playing || Luna.detail.cfg.process || (!renderNeeded && !Luna.gpu.pending)',timeout=30000)
    def snap():return ev('Luna.inspect.snapshot()')
    def check(name,code):
        try:val=ev(code);record(name,bool(val),val)
        except Exception as e:record(name,False,str(e))
    def act(name):ev('(a)=>Luna.inspect.act(a)',name);settle()
    def setv(key,val):ev('([k,v])=>Luna.inspect.set(k,v)',[key,val]);settle()
    def reset():act('resetAll');settle()
    def jump(i):ev('(i)=>Luna.inspect.jump(i)',i);settle(300)
    def pane(index):
        if page.locator('#drawer').is_hidden():page.locator('#detailToggle').click()
        page.locator('#tab'+str(index)).click();settle(100)
    def close():
        if page.locator('#drawer').is_visible():page.locator('#closeDrawer').click();settle(50)
    def ui_setting(key,val):
        loc=page.locator('[data-setting="'+key+'"]')
        if loc.count()>1:loc=loc.first
        kind=loc.get_attribute('type')
        if kind=='checkbox':loc.set_checked(bool(val))
        elif loc.evaluate('(el)=>el.tagName')=='SELECT':loc.select_option(str(val))
        else:loc.evaluate('(el,v)=>{el.value=v;el.dispatchEvent(new Event("input",{bubbles:true}))}',str(val))
        settle()
    def screenshot(name):
        if args.require_webgpu and name!='08-fallback.png': check('WebGPU remains active for '+name,'Luna.gpu.mode==="webgpu"&&!Luna.gpu.error')
        settle(180);path=out/name;page.screenshot(path=str(path));data=path.read_bytes()
        shots.append({'file':name,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data),'width':1920,'height':1080,'renderer':snap()['renderer']})
        print('SHOT',name,len(data),flush=True)
    initial=snap();record('Single-file contracts and part identity',initial['id']=='TA2026-00009-T04' and initial['dimensionsMM']==[597,715,19] and initial['seed']==409,initial)
    check('At least 50 documented new features','Luna.features.length>=50')
    if args.require_webgpu:record('Native WebGPU actually initialized',initial['renderer']=='webgpu',{'adapter':ev('Luna.gpu.adapter||null'),'error':initial['gpuError']})
    elif initial['renderer']!='webgpu':skipped('Native WebGPU execution','Navigation environment has no secure WebGPU context; Canvas2D is exercised instead.')
    check('CEO overlay off by default','!document.body.classList.contains("ceo")')
    for i,name in enumerate(['01-lager.png','02-cut.png','03-edge.png','04-press.png','05-crate.png','06-evening.png']):
        jump(i)
        check('Station '+str(i+1)+' and readable unique inscription',f'Luna.line.station==={i}&&document.querySelectorAll("#inscription").length===1&&document.getElementById("inscription").getBoundingClientRect().width>200')
        if not args.live or i in [1,5]:screenshot(name)
    if not args.live:
        act('overview');screenshot('07-full-line.png');check('All six station ticks visible','[...document.querySelectorAll(".station")].every(b=>{let r=b.getBoundingClientRect();return r.x>=0&&r.right<=innerWidth})')
        jump(3)
        page.mouse.move(1040,490);page.mouse.wheel(0,-450);settle();check('Mausrad zooms toward model','Luna.detail.nav.scale<1')
        for _ in range(22):page.locator('#zoomIn').click()
        check('Zoom has safe near limit','Luna.detail.nav.scale>=.13')
        page.locator('#zoomOut').click();check('Zoom-out button','Luna.detail.nav.scale>.13')
        page.locator('#resetView').click();settle();check('Camera reset','Luna.detail.nav.scale===1&&Luna.detail.nav.target===null')
        page.mouse.move(930,430);page.mouse.down();page.mouse.move(1000,460,steps=5);page.mouse.up();settle();check('Drag orbits camera','Math.abs(Luna.detail.nav.yaw)>.1')
        page.mouse.move(900,440);page.mouse.down(button='right');page.mouse.move(955,455,steps=4);page.mouse.up(button='right');settle();check('Right-drag pans camera','Luna.detail.nav.pan.some(x=>Math.abs(x)>.01)')
        page.mouse.dblclick(1020,425);settle();check('Double click focuses front','Luna.detail.nav.preset==="Frontdetail"')
        pane(0)
        for a,preset in [('front','Vorne'),('back','Hinten'),('left','Links'),('top','Oben'),('iso','Isometrie')]:
            page.locator('[data-action="'+a+'"]').click();settle();check('Camera preset '+preset,'Luna.detail.nav.preset==='+json.dumps(preset))
        page.locator('[data-action="saveView"]').click();settle();act('front');page.locator('[data-action="loadView"]').click();settle();check('Camera bookmark restores perspective','Luna.detail.nav.preset==="Isometrie"')
        for key,val in [('hud','quiet'),('dimensions',False),('bounds',False),('hotspots',False),('compass',False),('telemetry',True),('quality','economy')]:
            ui_setting(key,val);check('Visible view setting '+key,'Luna.detail.cfg['+json.dumps(key)+']==='+json.dumps(val))
        ui_setting('quality','balanced');ui_setting('hud','technical');close();jump(3)
        pane(1)
        for key,val in [('door',105),('explosion',.7),('shelves',3),('shelfPull',.7),('back',False),('holes',False),('clamps',True),('feet',True),('levelling',.6),('abs',False),('edgeMag',7),('cutProgress',.25),('waste',True),('dust',False),('crateLid',True),('straps',True),('crateExplode',True)]:
            ui_setting(key,val);check('Visible construction control '+key,'Luna.detail.cfg['+json.dumps(key)+']==='+json.dumps(val))
        check('Three independent press shelves exist','Luna.inspect.state().ranges.filter(r=>r.id==="shelf"&&r.center[0]<40).length===3')
        check('Back panel removed from press only','!Luna.inspect.state().ranges.some(r=>r.id==="back"&&r.center[0]<40)')
        page.locator('[data-action="cutaway"]').click();settle();check('Section removes right press wall','Luna.detail.cfg.cutaway&&!Luna.inspect.state().ranges.some(r=>r.id==="right"&&r.center[0]<40)')
        page.locator('[data-part="left"]').click();settle();check('Named component selection highlights real mesh','Luna.detail.cfg.selected==="left"&&Luna.detail.cfg.highlight')
        ui_setting('isolate',True);check('Isolation state','Luna.detail.cfg.isolate');close();screenshot('10-isolated.png');setv('isolate',False)
        reset();jump(3);setv('explosion',.56);setv('clamps',True);screenshot('11-exploded.png');setv('cutaway',True);setv('explosion',0);screenshot('12-section.png')
        reset();jump(3);setv('door',0);setv('explosion',0);setv('hotspots',False);act('front');setv('measure',True);close()
        settle(350)
        coords=ev('(()=>{let p=partPose(Luna.line.seconds);return [-.17,.17].map(x=>project(transform([x,0,.013],p.pos,p.rot),Luna.cam.vp))})()')
        pick_targets=ev('(qs)=>qs.map(q=>({x:q.x,y:q.y,target:document.elementFromPoint(q.x,q.y)?.id}))',coords)
        print('PICK_TARGETS',json.dumps(pick_targets),flush=True)
        for q in coords:page.mouse.click(q['x'],q['y']);settle(300)
        measure=ev('Luna.detail.measurements');record('Two actual surface picks measure 340 mm',bool(measure) and abs(measure[-1]['mm']-340)<6,measure)
        screenshot('13-measurement.png');act('clearMeasure');check('Clear measurements','Luna.detail.measurements.length===0');setv('measure',False)
        reset();jump(3)
        cdp=context.new_cdp_session(page)
        try:
            cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':800,'y':450},{'x':1000,'y':450}]})
            cdp.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':760,'y':450},{'x':1100,'y':450}]})
            cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]});settle();check('Two-finger native pinch zoom','Luna.detail.nav.scale<1')
        except Exception as e:record('Two-finger native pinch zoom',False,str(e))
        reset();jump(5);page.locator('#actionCard [data-action="openDoor"]').click();settle();check('First home door click actually opens','Luna.detail.cfg.homeDoor&&Luna.detail.cfg.door===105');screenshot('14-home-door.png')
        pane(2)
        for key,val in [('daylight',.8),('warmth',.2),('led',.35),('exposure',1.4),('workLights',False),('shadows',False),('reflections',False),('finish','smoked'),('roughness',.85)]:
            ui_setting(key,val);check('Visible lighting control '+key,'Luna.detail.cfg['+json.dumps(key)+']==='+json.dumps(val))
        close();screenshot('15-daylight-smoked.png');reset();jump(4);act('crate');act('strap');screenshot('16-crate-open.png')
        pane(3)
        for key,val in [('speed',2),('loop',True),('reverse',True),('process',True),('autoAssembly',True)]:
            ui_setting(key,val);check('Visible playback control '+key,'Luna.detail.cfg['+json.dumps(key)+']==='+json.dumps(val))
        close();setv('process',False);setv('autoAssembly',False)
        page.locator('#scrubber').evaluate('(el)=>{el.value=22;el.dispatchEvent(new Event("input",{bubbles:true}))}');settle();check('Timeline scrub seeks the actual camera','Math.abs(Luna.line.seconds-22)<.1')
        setv('loop',False);setv('speed',1);setv('reverse',True);page.locator('#play').focus();page.keyboard.press('Space');page.wait_for_function('Luna.line.seconds<21.5',timeout=15000);page.keyboard.press('Space');check('Reverse playback decreases timeline','Luna.line.seconds<22')
        setv('reverse',False);ev('Luna.inspect.seek(59.8)');setv('loop',True);page.locator('#play').focus();page.keyboard.press('Space');page.wait_for_function('Luna.line.seconds<3',timeout=15000);page.keyboard.press('Space');check('Loop wraps at end','Luna.line.seconds<3');setv('loop',False)
        ev('Luna.inspect.seek(20)');settle();page.keyboard.press('ArrowRight');settle();check('Arrow-key time nudge','Luna.line.seconds===22')
        reset();jump(3);page.locator('#shotButton').click();page.wait_for_function('Luna.detail.lastCapture?.bytes>0',timeout=30000);capture=ev('Luna.detail.lastCapture||null');record('PNG export created actual pixel blob',bool(capture) and capture['bytes']>10000,capture)
        act('export');check('Exported JSON includes part and measurements','Luna.detail.lastExport.part==="TA2026-00009-T04"&&Array.isArray(Luna.detail.lastExport.measurements)')
        act('share');check('Share URL contains actual time and configuration','new URL(Luna.detail.lastShare).searchParams.has("door")')
        page.keyboard.press('k');settle();check('Cinema hides tools but retains identity','document.body.classList.contains("cinema")&&getComputedStyle(document.getElementById("rail")).display==="none"');page.keyboard.press('Escape');settle();check('Escape restores normal view','!document.body.classList.contains("cinema")')
        if not args.set_content:
            setv('door',77);page.reload(wait_until='networkidle');page.wait_for_function('window.Luna?.gpu.ready');settle();check('Settings persist through a real reload','Luna.detail.cfg.door===77&&Luna.store.key==="luna.line.v1"')
        else:skipped('Storage and reload','about:blank test context has no origin storage.')
        reset();ev('Luna.inspect.seek(0)');page.locator('#play').focus();start=time.monotonic();page.keyboard.press('Space');page.wait_for_function('Luna.line.seconds>=60 && !Luna.line.playing',timeout=85000);elapsed=time.monotonic()-start;record('Complete unaccelerated 60-second journey',59<=elapsed<=80,{'wallSeconds':round(elapsed,3),'state':snap()})
        # Forced Canvas2D path and responsive layout both use the same actual runtime.
        ev("Luna.gpu.mode='canvas2d';document.body.classList.remove('gpu');document.getElementById('mode').textContent='Illustration · 2D';Luna.inspect.redraw()")
        jump(1);screenshot('08-fallback.png');check('Canvas2D fallback has raster pixels','document.getElementById("illustration").getContext("2d").getImageData(200,200,1,1).data[3]===255')
        page.set_viewport_size({'width':390,'height':844});jump(3);settle();path=out/'09-mobile.png';page.screenshot(path=str(path));shots.append({'file':'09-mobile.png','width':390,'height':844,'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'renderer':'canvas2d'})
        check('Mobile has no document overflow','document.documentElement.scrollWidth===innerWidth')
        check('Mobile ticks fit','[...document.querySelectorAll(".station")].every(b=>{let r=b.getBoundingClientRect();return r.x>=0&&r.right<=innerWidth})')
        page.locator('#detailToggle').click();settle();check('Mobile inspector is operable','document.getElementById("drawer").getBoundingClientRect().right<=innerWidth')
    else:
        jump(3);page.locator('#zoomIn').click();settle();check('Live zoom changes actual camera','Luna.detail.nav.scale<1');page.keyboard.press('o');settle();check('Live cabinet door control','Luna.detail.cfg.door===0');page.keyboard.press('e');settle();check('Live exploded construction','Luna.detail.cfg.explosion===0')
    record('No uncaught browser errors',not errors,errors)
    external=[u for u in requests if u.startswith('http') and not u.startswith(args.url.split('?')[0].rsplit('/',1)[0])]
    record('No external runtime resources',not external,external)
    report={'product':'LUNA LINE Atelier','observedAt':datetime.now(timezone.utc).isoformat(),'url':args.url if not args.set_content else 'about:blank / exact local HTML injected','browserVersion':browser.version,'runtimeSha256':hashlib.sha256(Path('Luna-Line.html').read_bytes()).hexdigest(),'adapter':ev('Luna.gpu.adapter||null'),'initial':initial,'status':'PASS' if all(r['status']!='FAIL' for r in results) else 'FAIL','tests':results,'shots':shots,'errors':errors,'limitations':['about:blank navigation restrictions; native GPU and origin storage unverified'] if args.set_content else []}
    (out/'report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False))
    (out/'features.json').write_text(json.dumps(ev('Luna.features'),indent=2,ensure_ascii=False))
    browser.close()
print(json.dumps({'status':report['status'],'pass':sum(r['status']=='PASS' for r in results),'fail':sum(r['status']=='FAIL' for r in results),'unverified':sum(r['status']=='UNVERIFIED' for r in results),'shots':len(shots)}),flush=True)
sys.exit(0 if report['status']=='PASS' else 1)
