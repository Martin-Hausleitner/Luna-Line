“This is proof we can build what we just showed.” LUNA LINE is the digital thread for a joinery. Not a Gantt chart. Not a chat. The same door the customer touched in the showroom is watched as a board, a part, a crate, then a quiet kitchen at 20:47. EDV Hausleitner skin. Process truth and the sold dream are one camera move.

**Keys 1–6:** jump to Lager / Zuschnitt / Kante / Presse / Weg / Abend. **Space:** start or pause the 60-second journey. **C:** show/hide the quiet CEO hours overlay (off by default). **G:** the whole line. **F:** fullscreen. The same controls work by clicking the thin station ticks and play control.

# LUNA LINE

[Open the live journey](https://martin-hausleitner.github.io/Luna-Line/) · [Single runtime file](Luna-Line.html) · [Local QA report](qa/report.json) · [Live QA report](qa/live/report.json)

## Deutsch

„Das ist der Beweis, dass wir bauen können, was wir gerade gezeigt haben.“ LUNA LINE ist der digitale Faden für eine Tischlerei. Kein Gantt-Diagramm. Kein Chat. Dieselbe Front, die Ihre Kundschaft im Schauraum berührt hat, begleiten Sie als Platte, als Teil, in der Kiste und schließlich in der stillen Küche um 20:47 Uhr. EDV Hausleitner Gestaltung. Fertigung und Wohnversprechen sind eine Kamerafahrt.

**Tasten 1–6:** Lager, Zuschnitt, Kante, Presse, Weg, Abend direkt ansehen. **Leertaste:** die 60 Sekunden lange Reise starten oder pausieren. **C:** Werkstattstunden ein-/ausblenden; beim Öffnen immer ausgeschaltet. **G:** Gesamtlinie. **F:** Vollbild. Die dünnen Stationsmarkierungen und die Wiedergabetaste sind auch anklickbar.

Öffnen Sie `Luna-Line.html` direkt oder verwenden Sie einen lokalen Webserver. Für native WebGPU-Darstellung benötigen Sie einen Browser mit verfügbarem WebGPU-Adapter und einen geeigneten sicheren Kontext (HTTPS oder localhost). Ohne WebGPU wird dieselbe Reise als nicht leere Canvas2D-Illustration mit bewegter Markierung dargestellt. Die aktive Darstellungsart steht unten rechts. Bei ausgeblendeter Browserseite pausiert die Reise. Die zuletzt betrachtete Position wird lokal gespeichert, soweit Ihr Browser dies erlaubt.

## Run / Ausführen

No install, no npm, no CDN, no framework, no iframe, no external fonts and no runtime network calls. All geometry, materials, WGSL, styling and logic are in **one 51 KB HTML file**. Open it directly, or for the reproducible localhost route:

```sh
python3 -m http.server 8080 --bind 127.0.0.1
# Open http://localhost:8080/Luna-Line.html
```

This is an original spatial demonstration, not manufacturing control or enterprise software. All order, household, process, percentage, delivery and working-hour values are **explicit demo fixtures**, not machine receipts or live operational evidence. The 12% waste inscription is illustrative, not a claimed nesting optimisation. No hours, appointments or material movements are booked. No customer data or credentials are included.

Dies ist eine räumliche Demonstration, keine Maschinensteuerung und keine Warenwirtschaft. Auftrag, Familie Berger, Lieferwoche, 12 % Verschnitt und Werkstattstunden sind **Demodaten**, keine Live-Fertigungsnachweise. LUNA LINE bucht keine Stunden, Termine oder Warenbewegungen.

## One part, six stations

| Station | Visible scene |
| --- | --- |
| 1 · Lager | Steel rack; oak panels 2800 × 2070 × 19 mm; Eiche 19 |
| 2 · Zuschnitt | Saw, panel with cut aperture, tracked 597 × 715 × 19 mm front, separate waste island and offcuts; 12 % |
| 3 · Kante | ABS 2 mm on the long side, edgebander, spool, slow camera orbit |
| 4 · Presse | 600 mm base carcass, press and block clamps; same front |
| 5 · Weg | Protective crate, van silhouette, delivery KW 38 and physical steps on the way home |
| 6 · Abend | Berger kitchen, same oak signature and front, warm under-cabinet light, 20:47; Montage Freitag 08:00 |

The actual moving front has identity `TA2026-00009-T04`, dimensions `597 × 715 × 19 mm`, one fixed UV grain signature and a distinctive knot. The camera and part travel through one spatial model, not six scene replacements. Four subtle corner fiducials help follow the front. A blue floor inlay crosses the entire production line and the stairs. The part inscription is projected from a world anchor with a leader to the front.

## Shared contract

| Surface | Responsibility |
| --- | --- |
| `Luna.theme` | `#0078C8`, de-AT, EDV Hausleitner brand |
| `Luna.gpu` | Native WebGPU triangles, depth, 4× MSAA, shadow map, procedural oak, device-loss fallback; truthful active renderer |
| `Luna.cam` | One Catmull–Rom camera spline with inspection dwell and edge orbit |
| `Luna.line` | Part identity, immutable dimensions, fixed grain seed, station, 60-second playback |
| `Luna.store` | Versioned local position in `luna.line.v1`; failure-safe without storage |

The Canvas2D route is an illustrated software depth-buffer rasterisation of the same geometry, not a screenshot, blank canvas or imitation GPU status. It also includes a moving tracking marker. It is intentionally lower resolution than native WebGPU.

## Verification / Prüfung

`qa/run-qa.mjs` is a dependency-free browser test driver using Chrome DevTools Protocol and Node's built-in WebSocket. It requires an installed Chrome/Chromium and Node 22 or later, **only for QA**, not to run the product. Set `CHROME_PATH` when using another installation.

```sh
node qa/run-qa.mjs --full
node qa/run-qa.mjs --base=https://martin-hausleitner.github.io/Luna-Line/
```

The local run captures all six stations at **1920 × 1080**, the full line, the Canvas2D fallback and a mobile view. It exercises a real 60-second playback, station keys, pause, CEO toggle, storage and the absence of external runtime requests. The live run captures stations 2 and 6 from GitHub Pages and repeats the essential interaction checks. Reports include source hashes, screenshot hashes, browser details and observed renderer, rather than claims of universal hardware certification. See `qa/VISION.md` for the screenshot review.

For deterministic inspection, use `?station=1` through `?station=6`, `?t=42`, or `?renderer=2d&station=5`. `Luna.inspect` exposes `jump(index)`, `seek(seconds)`, `overview()` and `snapshot()` for QA. Playback does not auto-start unless explicitly requested with `?play=1` and reduced motion is not enabled.

## Publishing

The public repository is named exactly `Luna-Line`. `main` contains the single canonical runtime **Luna-Line.html**, documentation and QA. The deployment-only `gh-pages` branch contains that same runtime byte-for-byte as **index.html**, plus `.nojekyll`, so the requested Pages root opens the product without a redirect, iframe or duplicate runtime on `main`. No build tool or npm is involved.

## Craft references, not dependencies

[Aster](https://github.com/wieslawsoltes/Aster), [AxiomCAM](https://github.com/wieslawsoltes/AxiomCAM), [Formalyth](https://github.com/wieslawsoltes/Formalyth), [AureonStudio](https://github.com/wieslawsoltes/AureonStudio), [StrataForge](https://github.com/wieslawsoltes/StrataForge), [KestrelCAD](https://github.com/wieslawsoltes/KestrelCAD). These supplied references inform the craft brief only. This file does not load their applications, borrow their wordmarks or depend on their code. The scene and renderer are original.

LUNA LINE · Demo · not HOMAG · not licensed WAWI · EDV Hausleitner GmbH Linz

**LINE proves the build; WAWI still books the hours.**
