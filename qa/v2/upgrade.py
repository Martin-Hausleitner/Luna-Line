#!/usr/bin/env python3
"""Materialize the reviewed single runtime; reject unreviewed source baselines.
The data segments are a gzip JSON text delta, never an application dependency.
"""
from pathlib import Path
import base64
import gzip
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
BASE = 'dcddf69b5be159d7025c7aa1118da8c51cf0570ed0281971b338dbe40d49846c'
INTERMEDIATE = '8c4808dc1bdcf672271c91c8b949fde023efdf51de5b4d8ee3d9ae2c255b0dcb'
PREVIOUS = '5496f29c6d4d97ecf32ac70ee048ab612655468a42121efeddae83f27990525a'
TARGET = '6307a708ce63996df3688e8b0c29f8567854b16e6a7cf7e37c3602e062162911'
SEGMENTS = ['cd75adc6aae637bcb4a40c178d05dfadad723ab3','235edf734cb7e5783072f50a814cbd019d6a401d','8fe8b4ff6400d2c7ebd0033ef03300ac4ee1d7e4','0f1961927f5bab96fbee0896e6600afaab2899d0']

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def main() -> None:
    path = ROOT / 'Luna-Line.html'
    original = path.read_bytes()
    digest = sha256(original)
    if digest not in (BASE, INTERMEDIATE, PREVIOUS, TARGET):
        raise SystemExit('Refusing to replace an unreviewed runtime: ' + digest)
    result = original
    if digest == BASE:
        chunks = []
        for i, expected in enumerate(SEGMENTS):
            chunk = (HERE / f'upgrade-{i:02}.b64').read_bytes()
            blob = hashlib.sha1(b'blob ' + str(len(chunk)).encode() + b'\0' + chunk).hexdigest()
            if blob != expected:
                raise SystemExit(f'Delta segment {i} failed integrity verification.')
            chunks.append(chunk.decode('ascii'))
        delta = json.loads(gzip.decompress(base64.b64decode(''.join(chunks), validate=True)))
        text = original.decode('utf-8')
        previous_end = 0
        for start, end, replacement in delta:
            if not (isinstance(start, int) and isinstance(end, int) and previous_end <= start <= end <= len(text) and isinstance(replacement, str)):
                raise SystemExit('Invalid or overlapping text delta.')
            previous_end = end
        for start, end, replacement in reversed(delta):
            text = text[:start] + replacement + text[end:]
        result = text.encode('utf-8')
        if sha256(result) != INTERMEDIATE:
            raise SystemExit('The assembled spatial-detail delta failed verification.')
    if sha256(result) == INTERMEDIATE:
        text = result.decode('utf-8')
        before = 'let dt=Math.min(1,(now-last)/1000||0);'
        after = 'let dt=Math.max(0,(now-last)/1000||0);'
        if text.count(before) != 1:
            raise SystemExit('Unrecognized animation clock.')
        result = text.replace(before, after).encode('utf-8')
    if sha256(result) == PREVIOUS:
        text = result.decode('utf-8')
        changes = [
            (" const story=$('title').getBoundingClientRect();", " if(Detail.open){const dock=$('viewDock').getBoundingClientRect();if(dock.width&&dock.height)occupied.push([dock.left-10,dock.top-10,dock.width+20,dock.height+20])}\n const story=$('title').getBoundingClientRect();"),
            ("' %':'zusammengefügt';renderNeeded=true}", "' %':'zusammengefügt';if(Detail.open)$('detailSummary').textContent='Eiche · 597 × 715 × 19 mm · '+(Detail.explode?'Schichten getrennt':'Originalmaße am Modell');renderNeeded=true}"),
            (" Detail.open=true;Detail.selection=selection;Detail.tab=tab;", " Detail.open=true;Detail.selection=selection;Detail.tab=tab;Detail.lastStation=currentIndex();"),
            ("function stopForDetail(){Luna.line.playing=false;manualJump=null;updatePlay();Luna.store.save()}", "function stopForDetail(){Luna.line.playing=false;manualJump=null;setStation(clamp(Math.floor(Luna.line.seconds/10),0,5));updatePlay();Luna.store.save()}"),
            ("function frame(now){requestAnimationFrame(frame);", "function frame(now){if(Luna.gpu.mode==='canvas2d')setTimeout(()=>frame(performance.now()),33);else requestAnimationFrame(frame);")
        ]
        for before, after in changes:
            if text.count(before) != 1:
                raise SystemExit('Unrecognized detail markup: ' + before)
            text = text.replace(before, after)
        result = text.encode('utf-8')
    if sha256(result) != TARGET or len(result) != 109866:
        raise SystemExit('The resulting runtime does not match the reviewed build.')
    if result != original:
        temporary = path.with_suffix('.html.new')
        temporary.write_bytes(result)
        temporary.replace(path)
    manifest = {
        'build': '2.0.0-spatial-details', 'runtime': 'Luna-Line.html',
        'bytes': len(result), 'sourceSHA256': TARGET, 'baseSHA256': BASE,
        'singleFileRuntime': True, 'operationCount': 30,
        'partId': 'TA2026-00009-T04', 'finishedDimensionsMM': [597,715,19],
        'constructionAndOperations': 'Explicit demo assumptions; no actual machine measurements.',
        'animationClock': 'Elapsed wall time; native GPU uses requestAnimationFrame; illustrated fallback uses a 33 ms timer; hidden documents pause playback.',
        'localInteractionRun': {'status':'PASS','checks':46,'renderer':'canvas2d','nativeWebGPU':'NOT_RUN in the restricted local container'},
        'nativeBrowserEvidence': '../report.json', 'liveBrowserEvidence': '../live/report.json',
        'note':'This manifest is not a native GPU or live-site test result. Consult the separate browser reports.'
    }
    (HERE/'BUILD.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    readme = ROOT/'README.md'
    content = readme.read_text(encoding='utf-8')
    marker = '## Spatial detail upgrade / Räumliche Details (v2)'
    if marker not in content:
        content += '''

## Spatial detail upgrade / Räumliche Details (v2)

### English

Click the tracked front or a floating dimension to pause and inspect it.
Four tabs expose 30 selectable process steps, orthographic dimension drawings,
material layers and verification limits. The original six-station journey stays.

**1–6** stations; **Space** play/pause; **D** inspect; **M** dimensions;
**X** explode layers; **R** reset; **Escape** close; **C** CEO; **G** full line;
**F** fullscreen. Drag to orbit and scroll to zoom in inspection. Front, back,
top and station-context presets, three finishes, a real exploded model and
an opening front are available. SVG and JSON exports are actual downloads.

The front remains 597 × 715 × 19 mm with grain seed 409. Additional construction,
hinges and operation targets are explicit demo assumptions, not measured data
or approved manufacturing instructions. No machine or booking system is connected.

The restricted local container exercised 46 Canvas2D checks. Native WebGPU and
live Pages results are separate in `qa/report.json` and `qa/live/report.json`.
Each report identifies its actual adapter. Publishing uses hosted macOS and an
Apple GPU, not your personal Mac. Failed Linux SwiftShader trials and historical
v1 results are not v2 acceptance evidence. The manifest alone proves no browser
acceptance. QA files are not runtime requirements: Pages serves one HTML file.

### Deutsch

Klicken Sie auf die Front oder ein schwebendes Maß. Die Fahrt pausiert; Sie sehen
Arbeitsschritte, Maße, Aufbau und Prüfung. Alle 30 Arbeitsschritte sind einzeln
anwählbar. Drehen, Zoomen, Rückseite, Draufsicht und aufgetrennte Schichten zeigen
die Details. Die Tür lässt sich in passenden Stationen öffnen. Maßzeichnung
(SVG) und Bauteildaten (JSON) können Sie direkt exportieren.

**D** öffnet Details, **M** schaltet Maße, **X** trennt Schichten, **R** setzt die
Ansicht zurück und **Esc** schließt sie. **1–6** und **Leertaste** bedienen die
Reise; der Regler unten springt zu jedem Zeitpunkt.

Modellmaße, errechnete Sollwerte und fehlende echte Prüfnachweise bleiben getrennt.
Die Maße folgen dem Modell live, nicht einer Messmaschine. Die Prüfung erfindet
keine erledigten Messungen. Die Reise verwirft bei langsamen Grafikgeräten keine
verstrichene Zeit. Beim Verbergen der Seite pausiert sie.

LINE proves the build; WAWI still books the hours.
'''
        readme.write_text(content,encoding='utf-8')
    print(json.dumps({'status':'MATERIALIZED','sha256':TARGET,'bytes':len(result)}))

if __name__ == '__main__':
    main()
