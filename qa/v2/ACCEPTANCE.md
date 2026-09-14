# LUNA LINE v2 — LOCAL PASS / PAGES PASS

Reviewed 14 September 2026. Runtime: `Luna-Line.html`, 109,866 bytes.

SHA-256: `6307a708ce63996df3688e8b0c29f8567854b16e6a7cf7e37c3602e062162911`

## Executed gates

| Gate | Result | Evidence |
| --- | --- | --- |
| Local interaction suite | PASS, 46/46 | `qa/v2/report.json`, `qa/v2/test-browser.py` in the delivery ZIP; Canvas2D in a restricted Chromium context. No native GPU or persistent-origin claim for this suite. |
| Native macOS browser suite | PASS, 25/25 | `qa/report.json`; hosted macOS arm64, Chrome 152.0.7977.83, actual Apple WebGPU adapter; 13 screenshots. Not the user's personal Mac. |
| Complete playback | PASS | 60.185 seconds of actual elapsed time; final station 6, timeline 60, same T04 identity. |
| Illustrated fallback | PASS | Actual timer-driven moving journey, nonblank Canvas2D scene and mobile layout. |
| Live public Pages browser suite | PASS, 20/20 | `qa/live/report.json`; actual public HTTPS URL, native Apple WebGPU, six screenshots, no uncaught browser errors. |
| Public runtime integrity | PASS | Publishing workflow verified the served HTML against the exact SHA-256 above before live browser execution. |
| Screenshot integrity | PASS | Native and live screenshot bytes match their recorded hashes. Live 02, 06 and all four detail captures match the corresponding native captures. |

Native run: https://github.com/Martin-Hausleitner/Luna-Line/actions/runs/34832016269

Successful publishing and live run: https://github.com/Martin-Hausleitner/Luna-Line/actions/runs/34832378508

Successful Pages deployment: https://github.com/Martin-Hausleitner/Luna-Line/actions/runs/34832413495

The native run's browser and raster gates passed; only its original push failed because another commit advanced main. The successful publishing run recovered the exact hash-verified artifact, preserved concurrent repository changes, published it, and executed the live tests. Earlier failed Linux software-GPU experiments are not acceptance evidence.

## Visual review

The six native station captures, native rear/dimension view, and actual live `02-cut.png`, `06-evening.png` and `11-layer-detail.png` were visually inspected. Desktop captures are 1920 × 1080; mobile captures are 390 × 844.

| Visual requirement | Result |
| --- | --- |
| One connected journey and floor thread | PASS |
| Same T04 front and oak identity from saw to home | PASS |
| Cool workshop distinct from warm evening kitchen | PASS |
| Saw cutout and separate waste visible | PASS |
| Wide evening kitchen composition | PASS, stylized 3D demo, not photorealism |
| Readable part identity, world-following dimensions | PASS |
| Quiet LUNA LINE / EDV Hausleitner branding | PASS |
| No ERP masks, calendar grid, chat or module header | PASS |
| Clickable measurement/part, inspectable material layers | PASS |
| Detail labels avoid each other and the view controls in reviewed views | PASS |

## Scope and truth

One runtime file; 30 selectable operation descriptions; live model dimensions; four detail tabs; orbit/zoom; front/back/top/context views; three finishes; geometric layer separation; opening door; SVG and JSON downloads. Identity remains `TA2026-00009-T04`, 597 × 715 × 19 mm, grain seed 409.

**Live means synchronized to the model, not measured by a connected machine.** Additional construction layers, hinge geometry, targets and process descriptions are explicit demonstration assumptions. The verification tab does not fabricate measurements or completed production checks. This is not approved manufacturing or CNC data, and no hours are booked.

## Deutsch

Die aktualisierte Datei und die öffentliche Seite sind geprüft. Schwebende Maße folgen dem Bauteil; ein Klick pausiert die Reise und öffnet die Details. Die Bedienprüfung umfasst alle 30 Arbeitsschritte sowie Drehen, Zoomen, Schichttrennung, Türwinkel, Exporte und die mobile Ansicht. Modellmaße und fehlende echte Prüfnachweise bleiben getrennt.

LINE proves the build; WAWI still books the hours.
