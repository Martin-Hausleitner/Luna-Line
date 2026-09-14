#!/usr/bin/env python3
"""Materialize the reviewed single-file runtime; refuse any unreviewed baseline.

The four data files contain a gzip-compressed JSON text delta, not executable
Python or a runtime dependency. All resulting JavaScript is committed openly in
Luna-Line.html and syntax/browser-tested before Pages publication.
"""
from pathlib import Path
import base64
import gzip
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
BASE = 'dcddf69b5be159d7025c7aa1118da8c51cf0570ed0281971b338dbe40d49846c'
TARGET = '8c4808dc1bdcf672271c91c8b949fde023efdf51de5b4d8ee3d9ae2c255b0dcb'
SEGMENTS = [
    'cd75adc6aae637bcb4a40c178d05dfadad723ab3',
    '235edf734cb7e5783072f50a814cbd019d6a401d',
    '8fe8b4ff6400d2c7ebd0033ef03300ac4ee1d7e4',
    '0f1961927f5bab96fbee0896e6600afaab2899d0',
]

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def main() -> None:
    path = ROOT / 'Luna-Line.html'
    original = path.read_bytes()
    digest = sha256(original)
    if digest not in (BASE, TARGET):
        raise SystemExit('Refusing to replace an unreviewed runtime: ' + digest)
    if digest == BASE:
        chunks = []
        for i, expected in enumerate(SEGMENTS):
            chunk = (HERE / f'upgrade-{i:02}.b64').read_bytes()
            git_blob = hashlib.sha1(b'blob ' + str(len(chunk)).encode() + b'\0' + chunk).hexdigest()
            if git_blob != expected:
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
        if sha256(result) != TARGET or len(result) != 109387:
            raise SystemExit('The resulting runtime does not match the reviewed build.')
        temporary = path.with_suffix('.html.new')
        temporary.write_bytes(result)
        temporary.replace(path)
    manifest = {
        'build': '2.0.0-spatial-details',
        'runtime': 'Luna-Line.html',
        'bytes': path.stat().st_size,
        'sourceSHA256': sha256(path.read_bytes()),
        'baseSHA256': BASE,
        'singleFileRuntime': True,
        'operationCount': 30,
        'partId': 'TA2026-00009-T04',
        'finishedDimensionsMM': [597, 715, 19],
        'constructionAndOperations': 'Explicit demo assumptions; no actual machine measurements.',
        'localInteractionRun': {'status': 'PASS', 'checks': 46, 'renderer': 'canvas2d', 'nativeWebGPU': 'NOT_RUN in the restricted local container'},
        'nativeBrowserEvidence': '../report.json',
        'liveBrowserEvidence': '../live/report.json',
        'note': 'This build manifest is not a native GPU or live-site test result. Consult the separate browser reports.'
    }
    (HERE / 'BUILD.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    readme = ROOT / 'README.md'
    content = readme.read_text(encoding='utf-8')
    marker = '## Spatial detail upgrade / Räumliche Details (v2)'
    if marker not in content:
        content += '''

## Spatial detail upgrade / Räumliche Details (v2)

### English

The original continuous six-station journey is preserved. Click the tracked front
or a floating dimension to pause and inspect it. The four inspection tabs show
30 selectable process steps, orthographic dimension drawings, material layers,
and the limits of verification. Width, height, thickness and station-specific
dimensions remain anchored to the model while the camera moves.

Controls: **1–6** stations; **Space** play/pause; **D** inspect; **M** dimensions;
**X** explode layers; **R** reset view; **Escape** close inspection; **C** CEO hours;
**G** full line; **F** fullscreen. In inspection, drag to orbit and scroll to zoom.
Front, back, top and station-context views are available. The layer and door-angle
sliders alter the actual rendered geometry. SVG and JSON exports are real downloads.

The finished front remains 597 × 715 × 19 mm with grain seed 409. Additional
veneer/core layers, hinges, process targets and checks are explicitly marked as
demo assumptions, not verified manufacturing instructions or live measurements.
No machines, order booking or customer systems are connected.

The v2 interaction run passed 46 checks using Canvas2D in the restricted local
container. Native WebGPU and live Pages results are recorded separately in
`qa/report.json` and `qa/live/report.json`; do not treat the historical v1 Mac
result or the build manifest as a new Mac hardware benchmark. The CI renderer's
actual adapter is included in those reports. QA files are development evidence,
not runtime dependencies. Pages still serves exactly one self-contained HTML.

### Deutsch

Die ursprüngliche Reise bleibt erhalten. Klicken Sie auf die Front oder ein
schwebendes Maß: Die Fahrt pausiert und Sie sehen Arbeitsschritte, Maße, Aufbau
und Prüfung. 30 Arbeitsschritte sind einzeln anwählbar. Drehen, Zoomen, Rückseite,
Draufsicht und die aufgetrennten Materialschichten zeigen die Bauteildetails.
Die Tür lässt sich in der passenden Station öffnen. Maßzeichnung als SVG und
Bauteildaten als JSON lassen sich direkt exportieren.

**D** öffnet die Details, **M** schaltet die Maße, **X** trennt die Schichten,
**R** setzt die Ansicht zurück und **Esc** schließt die Details. **1–6** und
**Leertaste** bedienen weiterhin die Reise. Der Schieberegler unten springt
an eine beliebige Stelle der 60-Sekunden-Fahrt.

Modellmaße, errechnete Sollwerte und fehlende reale Prüfnachweise sind getrennt.
Die eingeblendeten Maße folgen dem Demo-Modell live, nicht einer angeschlossenen
Messmaschine. Der Prüfbereich erfindet keine abgeschlossenen Prüfungen.

LINE proves the build; WAWI still books the hours.
'''
        readme.write_text(content, encoding='utf-8')
    print(json.dumps({'status': 'MATERIALIZED', 'sha256': TARGET, 'bytes': path.stat().st_size}))

if __name__ == '__main__':
    main()
