# Arrow Overlay

This directory contains the arrow overlay for `ris-osvp-metadata-camdkit` — the navigation index and per-segment orientation pages for the Linked-Intent Development (LID) traceability chain.

## What is an arrow?

An arrow tracks the full intent chain for one domain cluster:

```
HLD → LLD → EARS specs → @spec annotations → tests → code
```

Each arrow has one orientation page (a `.md` file here) and one entry in `index.yaml`.

## Segments

| Arrow | Status | Summary |
|---|---|---|
| [protocol-envelope](protocol-envelope.md) | AUDITED | Clip model, schema machinery, primitive types |
| [camera-identity](camera-identity.md) | AUDITED | Static hardware metadata — camera, lens, tracker |
| [optical-characteristics](optical-characteristics.md) | AUDITED | Per-frame lens behavior — distortion, FIZ, Cooke |
| [spatial-tracking](spatial-tracking.md) | AUDITED | 3D position/orientation, Mo-Sys F4 protocol |
| [temporal-synchronization](temporal-synchronization.md) | AUDITED | Timecode, timestamps, PTP sync |
| [format-bridge](format-bridge.md) | AUDITED | Proprietary camera format adapters |

## How to use

- **Find a segment**: check `index.yaml` for status and `next` action.
- **Navigate to code**: each arrow doc's `## References` section links to the LLD, EARS spec file, test files, and source directories.
- **Understand gaps**: `## Work Required` in each arrow doc lists must-fix, should-fix, and nice-to-have items.
- **Check spec status**: `## Spec Coverage` tables show implemented vs. gap counts; full status is in `docs/specs/`.

## Updating

When making changes to a segment:
1. Update the relevant `@spec` annotations in source code.
2. Update the spec file (`docs/specs/{segment}-specs.md`) — change `[ ]` to `[x]` when closing a gap.
3. Update the arrow doc's `## Spec Coverage` table and `## Work Required` section.
4. Bump `audited` and `audited_sha` in `index.yaml` after verifying the change.

Run `/arrow-maintenance` to audit all segments and regenerate derived views.

## First audit

All 6 segments were bootstrapped and audited on 2026-05-16 at git SHA `de5c56e9b2bbecff1b7a89ca6ad0c6ea2cd04ebd`.
