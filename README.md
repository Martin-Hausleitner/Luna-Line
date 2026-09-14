**This is proof we can build what we just showed.** LUNA LINE is the digital thread for a joinery. Not a Gantt chart. Not a chat. The same door the customer touched in the showroom is watched as a board, a part, a crate, then a quiet kitchen at 20:47. EDV Hausleitner skin. Process truth and the sold dream are one camera move.

**Keys 1–6:** Lager / Zuschnitt / Kante / Presse / Weg / Abend. **Space:** start or pause the 60-second journey. **C:** workshop hours overlay, off at startup. **G:** the complete line. **F:** fullscreen.

# LUNA LINE · Atelier / 02

[Open the live application](https://martin-hausleitner.github.io/Luna-Line/) · [Canonical single file](Luna-Line.html) · [Browser evidence](qa/atelier/) · [68 additions](qa/atelier/FEATURES.md)

## Deutsch — vom Brett zum Bleiben

Dieselbe Front, derselbe Weg: **TA2026-00009-T04 · 597 × 715 × 19 mm**. Die Eichenmaserung mit Signatur 409 und die Eckmarkierungen bleiben vom Zuschnitt bis in die Küche Berger erhalten. Ein durchgehender Kamerapfad und der blaue Bodenfaden verbinden die sechs Stationen. Die Werkstatt bleibt kühl, der erste Abend zu Hause warm.

Die Atelier-Erweiterung ergänzt 68 konkrete Funktionen und Darstellungsdetails. Der Schwerpunkt liegt auf freier Inspektion, räumlichen Hinweisen und einem nachvollziehbaren Korpus, nicht auf neuen Verwaltungsbildschirmen.

### Bedienung

| Eingabe | Wirkung |
|---|---|
| Mausrad, `+` / `−`, zwei Finger | Stufenlos zoomen, mit Nah-/Fernbegrenzung |
| Ziehen | Umkreisen |
| Rechte Maustaste oder Umschalttaste + Ziehen | Verschieben |
| Doppelklick | Front fokussieren |
| `R` | Kameraperspektive zurücksetzen |
| `I` | Inspektor mit Ansicht, Bauteil, Licht, Reise und Hilfe |
| `H` | Technisches, ruhiges oder ausgeschaltetes HUD |
| `O` / `E` / `X` | Front schwenken / Explosion / rechte Schnittansicht |
| `M` | Zwei Punkte auf tatsächlichen Oberflächen messen |
| `P` | Szene als PNG mit Teileidentität exportieren |
| `K` / Escape | Messemodus / zurück zur Bedienung |
| Pfeiltasten links/rechts | Zwei Sekunden zurück/vor |
| Zeitachse | Direkt an eine Stelle der Reise fahren |

### Der Korpus ist kein Vollblock

Der 600 × 720 × 560-mm-Demokorpus besteht aus getrennten 19-mm-Seiten, Boden und Deckel, einer einzeln schaltbaren 8-mm-Rückwand und bis zu drei Einlegeböden. Die Front schwenkt um ihre linke Scharnierachse. Die 35-mm-Töpfe, Arme und Montageplatten sind Geometrie; ebenso die Schrauben, einzelnen 32-mm-Bohrungen, Spannklötze und optionalen verstellbaren Füße.

Explosion, Schnitt und Teileisolierung verändern tatsächlich die gezeichnete Geometrie. Das gilt auch für den Inhalt der Transportkiste: Korpus, Front, Eckpolster, Gurte, Latten und abhebbarer Deckel. Kein Bild einer Kiste und kein leerer Platzhalter.

### Mehr Grafik, ohne Downloads

Gefaste Geometrie, gedrehte Metall- und Keramikprofile, Eichenporen und Astbild, prozeduraler Stein, Putz und Fischgrätparkett; detaillierte Maschinen, Rollen, Schläuche, Transporter und Treppe; Küche mit Fenster, nächtlicher Silhouette, Vorhängen, Pendelleuchten, Pflanzen, Hockern, Messingarmatur und Unterbauleuchten.

WebGPU verwendet WGSL, eine 2.048-Pixel-Schattenkarte, Mehrfachabtastung, materialabhängige Reflexe und Tonwertabbildung. Lichtwärme, Tageslicht, Unterbauleuchten, Belichtung und Oberflächenfinish lassen sich verändern. Der Canvas2D-Ersatz zeichnet die gleiche Welt als Illustration mit vereinfachter Beleuchtung; der aktive Renderer wird ausdrücklich angezeigt. Er ist kein fotorealistischer WebGPU-Nachweis.

### Was die Daten bedeuten

Alle Auftrags-, Zeit-, Ausschuss-, Montage- und Prozessangaben sind **Demonstrationswerte**, keine Live-Maschinendaten und keine Zeiterfassung. Der Stundenvergleich bleibt 4,2 / 5,0 h Soll; er bucht nichts. Die 12 % Ausschuss sind eine illustrierte Planannahme, keine Optimierungsberechnung.

Die Messfunktion schneidet echte Dreiecke des dargestellten Modells und rechnet Weltmeter in Millimeter um. Bei Explosion, Schwenkung und ABS-Vergrößerung misst sie die dargestellte Geometrie, nicht automatisch eine Fertigungszeichnung. Die angezeigten 597 × 715 × 19 mm bleiben die Sollidentität der Front. Es gibt keine CNC-Freigabe, Kollisionsgarantie, Beschlaghersteller-Zertifizierung oder WAWI-Integration.

Die optionale Leistungsanzeige zeigt **gemessene CPU-Bildaufbauzeit**, nicht erfundene GPU-Benchmarks oder Maschinensensoren. Die Rendererqualität schaltet Auflösungen, keine erfundene Hardware-Erkennung.

## English — run, architecture, evidence

`Luna-Line.html` is the only runtime file. No npm, CDN, external fonts, framework, iframe, remote model or texture request is used. All geometry, SVG icons, CSS, JavaScript and shaders are embedded. Serve the file over HTTPS or localhost for the most reproducible WebGPU execution:

```sh
python3 -m http.server 8088 --bind 127.0.0.1
# Open http://127.0.0.1:8088/Luna-Line.html
```

Opening the downloaded file directly also includes a nonblank Canvas2D path. Actual GPU and storage access depend on the browser and origin. A visible renderer indicator reports which path is running. The Pages `index.html` is the exact canonical runtime copied to the existing `gh-pages` branch, not a redirect or a second implementation.

The existing contracts are retained: `Luna.theme`, `Luna.gpu`, `Luna.cam`, `Luna.line`, `Luna.store` (`luna.line.v1`). Additional inspection state is under `Luna.detail` and `Luna.inspect`. `Luna.features` contains the 68 documented additions. Validated detail preferences and the camera bookmark use `luna.line.atelier.v2`. Both storage operations fail safely when origin storage is unavailable.

PNG export captures actual rendered pixels with the part identity and measurement labels; it is not a mock image. JSON export includes the part, settings, camera and measurements. Shared view links preserve journey time, door angle and explosion. No export sends customer data to a server.

### Reproducible browser checks

`qa/atelier/run-qa.py` uses Python Playwright for development-time testing only. The reviewed runtime passed **102/102 checks on macOS 15 with native Apple WebGPU and Chrome 152.0.7977.83** in Actions run 34833631791. Sixteen actual browser screenshots include all stations, construction details, Canvas2D and mobile. The complete journey took **60.064 wall seconds**. This is a hosted Apple machine, not a performance claim for the user's Mac. Publication promotes that exact checked artifact; live Pages is tested separately, with strict exit and report gates. The original source reconstruction workflow is manual-only and cannot publish an older build.

```sh
python3 -m pip install playwright==1.55.0
python3 -m playwright install chromium
python3 qa/atelier/run-qa.py --url http://127.0.0.1:8088/Luna-Line.html --output qa/atelier --require-webgpu
```

The reports include the observed browser version, renderer, errors, individual results, SHA-256 screenshot hashes and any unverified gates. Read the latest report rather than treating old original-version test counts as evidence for Atelier. The current-container `about:blank` run exercises Canvas2D and the interface because managed navigation is restricted; it does not prove native WebGPU or persistence.

The original craft references are Aster, AxiomCAM, Formalyth, AureonStudio, StrataForge and KestrelCAD by wieslawsoltes. This app does not embed those applications or claim their feature parity.

**LINE proves the build; WAWI still books the hours.**


The pre-Atelier spatial revision is preserved on `archive/spatial-before-atelier-20260914`. Older root-level QA describes earlier revisions; current Atelier evidence is in `qa/atelier/`. Canonical runtime: 128,011 bytes; SHA-256 `cba13c87caf3cf2cfb02567d019b4fed6cf9f2af9d56005e78b4f12042f985ec`.
