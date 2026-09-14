# LUNA LINE — visual acceptance

**Local PASS / Pages PASS.** Review date: 14 September 2026.

The seven required desktop PNGs are real Chrome captures at **1920 × 1080**, rendered by native WebGPU on the connected Mac. Observed adapter: `apple / metal-3`. The reviewer inspected image proxies generated from the captured PNGs: a six-station contact sheet, the evening composition and the full-line view. These reduced-size, compressed review proxies are not substitutes for the full-resolution evidence committed here. Text identity and all six station states were also checked in the running browser. No screenshots were drawn or substituted for the application.

## Rubric

| Gate | Result | Observed evidence |
| --- | --- | --- |
| Reads as one journey, not six disconnected models | PASS | One continuous workshop floor, a blue route continuing to the home, one full-line composition, one camera/part timeline. |
| The evening door is recognisably the cut part | PASS | Same proportions, oak material/UV signature, tracked corner marks and persistent T04 identity; the same moving door mesh reaches the kitchen slot. |
| Workshop differs from home in light and colour | PASS | Cool grey/blue production hall versus warm oak/plaster kitchen, evening blue window and under-cabinet light. |
| Waste at the saw is visible | PASS | Separate offcut island, slivers and waste bin beside the stock aperture and tracked cut front; 12 % is labelled as demo nesting. |
| Evening kitchen works as a trade-fair LED-wall composition | PASS | Wide warm scene, strong 20:47 title, kitchen frontage, ambient under-cabinet lighting, no competing application panels. This is a visual composition assessment, not a physical LED-wall hardware test. |
| Part number readable once per shot | PASS | One world-anchored inscription with leader, fixed TA2026-00009 / T04 / 597×715×19 identity; no repeated ID cards. |
| EDV Hausleitner / LUNA LINE quiet and present | PASS | Small corner identity and exact required footer, with no competing navigation header. |
| No website header, chat bubble or calendar grid | PASS | Scene, restrained narrative type, world inscription and thin station ticks only. |

## Required captures

| File | Scene |
| --- | --- |
| [01-lager.png](01-lager.png) | Oak panel rack, Eiche 19, panel dimensions |
| [02-cut.png](02-cut.png) | Saw, cut front and visible waste |
| [03-edge.png](03-edge.png) | Edgebander, long-side ABS and front |
| [04-press.png](04-press.png) | 600 mm carcass and block clamps |
| [05-crate.png](05-crate.png) | Crate on van silhouette and physical stairs |
| [06-evening.png](06-evening.png) | Berger kitchen, same front, 20:47 and Montage Freitag 08:00 |
| [07-full-line.png](07-full-line.png) | Wide connected production-to-home model; all six ticks visible |

Additional captures: [Canvas2D fallback](08-fallback.png), [mobile](09-mobile.png). These are additional engineering checks, not replacements for the desktop WebGPU evidence.

## Automated execution

[Local report](report.json): **21/21 PASS**, including native WebGPU, all stations, keys, pause, CEO off by default, storage, zero external runtime requests, full playback, fallback movement, mobile fit and zero uncaught browser errors.

Measured full playback: **60.016 wall-clock seconds**. Final application time: 60 seconds; renderer remained WebGPU; final station was Abend; playback stopped.

[Live report](live/report.json): **16/16 PASS**, with real Pages captures [02-cut.png](live/02-cut.png) and [06-evening.png](live/06-evening.png).

## Live integrity

Pages: https://martin-hausleitner.github.io/Luna-Line/

Observed HTTP status: **200**. Response length: **51,483 bytes**. Served HTML is byte-for-byte equal to canonical `Luna-Line.html`:

```text
SHA-256 dcddf69b5be159d7025c7aa1118da8c51cf0570ed0281971b338dbe40d49846c
```

Both live shots are also byte-for-byte identical to their visually reviewed local counterparts:

```text
02-cut.png     a67f263a4b45f7349dfa315678cb10f1e0321af5141aedca582b09ab7151b290
06-evening.png 44538da7ce47e868d777677a084d555d6199ded1f0ff44667cbbcb26f2d5e10b
```

The sandbox browser's navigation policy prevented localhost visual testing there. The full served-origin and live tests therefore ran on the connected Mac, not in a fabricated sandbox browser session. Two early Canvas2D correction iterations preceded final native captures; no native/live visual fix loop was required.

This is a demonstration of the digital thread, not proof of actual production completion, measured workshop hours, stock or delivery commitments. All business values remain explicit demo fixtures.

**LINE proves the build; WAWI still books the hours.**
