# Omega launcher, site and publishing

Ported from the FOE Reborn launcher (`C:/Projects/FOEReborn-launcher`). The code, file formats and update
algorithm are the same; only the names differ. All game-specific names are in
`launcher/OmegaLauncher/GameInfo.cs` and follow the Names table in `CLAUDE.md`.

## Overview

`OmegaLauncher.exe` (WinForms, .NET Framework 4.8, one exe) installs the game, updates it by downloading
only the changed parts, verifies and repairs files, manages mods (Mods tab) and installs mods from the
catalogue (Catalogue tab). It updates itself.

A game build is cut into zip packs. Each file belongs to one pack. A pack is named
`<group>-<sha256 first 16>.zip`, so a pack whose files did not change keeps its name and is neither
uploaded nor downloaded again. Packs are GitHub release assets; the small JSON files are on GitHub Pages.

## Files on the site

```
site root (Pages, https://bigtester8498-dev.github.io/OmegaProject/)
  index.html, favicon.png, icon.png   download page (Russian and English)
  downloads/OmegaLauncher.exe, launcher-version.json   from the release launcher-latest
  downloads/manifest.json, version.json, notes.json    production channel (newest stable v0.x.y)
  downloads/test/...                                   testing channel (newest v0.x.y, prereleases included)
  downloads/mods/catalog.json                          mod catalogue (newest mods-YYYYMMDD-HHMMSS release)
release v0.x.y: the packs new in this release, plus manifest.json, version.json, notes.json
```

The formats of `manifest.json`, `version.json`, `notes.json`, `launcher-version.json` and `catalog.json`
are described in `C:/Projects/FOEReborn/docs/launcher/DESIGN.md`; Omega uses them unchanged
(`"game": "Omega.exe"`, `"file": "OmegaLauncher.exe"`).

## Pack rules (`tools/publish.py` RULES)

First match wins.

| Path | Pack |
|---|---|
| `Omega_Data/Managed/Omega.*` | `code` |
| `Omega_Data/Managed/` | `engine-managed` |
| `Omega_Data/` | `data` |
| `Content/<package>/` | `content-<package>` |
| `Mods/<mod>/` | `mod-<mod>` |
| anything else (exe, UnityPlayer.dll, MonoBleedingEdge, ...) | `engine` |

A code-only update downloads the `code` pack and perhaps `data`. No pack may exceed 300 MB: `publish.py`
stops and asks for a rule. Per-area splits of a big content package (sprites, music) go into RULES before
the `Content/<package>/` rule; there is a commented example. Zips are deterministic (sorted entries, fixed
timestamps, PNG/JPG/MP3/OGG stored), so the same files give the same pack.

## Files next to the launcher

```
OmegaLauncher.exe
settings.json            {"channel": "prod"|"test", "language": "ru"|"en", "baseUrl": "..."}, each optional
installed-files.json     installed version, channel and every file the launcher installed
installed-mods.json      mods installed from the catalogue (id, version, sha256, files)
game/                    the game (Omega.exe, Omega_Data/, Content/core/, Mods/)
.omega/downloads/        packs and .part files (a broken download resumes)
.omega/staging/          extracted, verified files waiting for the swap
.omega/rollback/         old files during a swap
.omega/swap.json         swap journal, present only while a swap runs
.omega/manifest-<channel>.json   the last manifest of the channel
.omega/mod-downloads/, mod-staging/, mod-backups/   the same for catalogue mods
```

An update never deletes a file it did not install. A shipped file that replaces a user file keeps the
user's copy as `<name>.bak`. A failed or interrupted update rolls back, so the previous install stays
playable. Saves and the game's settings live in `%USERPROFILE%\AppData\LocalLow\OmegaProject\Omega\`.

The download site is `GameInfo.DefaultBaseUrl`, overridden by `settings.json` `baseUrl`, overridden by
`--base-url URL`.

## Mods tab and catalogue

The Mods tab edits the `"mods"` section (`enabled`, `disabled`, `order`, `consent`) of the game's
`settings.json` in persistentDataPath; every other byte of the file stays. `ModRules.cs` is the launcher's
copy of the game's mod rules: discovery of `Content/*/package.json` (always on, never listed; the base
package is `core`) and `Mods/*/package.json` with one level of group folders, validation, version ranges,
load order, `defaultEnabled`, states with reasons in both languages, enable and disable cascades. Code mods
ask for consent per version.

`launcher/OmegaLauncher.Tests/cases/modrules-cases.json` (inputs from `tools/make_modrules_cases.py`,
answers filled by `OMEGA_FILL_CASES=1 OMEGA_FILL_ALL=1 dotnet test ... --filter FillExpected`) holds the
shared cases. The game runs a byte-identical copy in `unity/Omega/Assets/Tests/EditMode/Data/`; the launcher
test `GameRepoCopy_IsIdentical` checks the copy. Where the two disagree, the game is right.

The Catalogue tab reads `downloads/mods/catalog.json`, installs a mod with the mods it requires, checks size
and SHA-256, extracts into `.omega/mod-staging/` with path and size checks, then moves it into
`game/Mods/<id>/` (or `game/Mods/<group>/<id>/`). Game updates never touch catalogue mods.

## Publishing (`tools/publish.py`, stdlib only)

```
python tools/publish.py pack --build BUILD --out OUT --version auto --channel test \
    [--notes-ru FILE --notes-en FILE] [--prev PREV_OUT] [--launcher OmegaLauncher.exe]
python tools/publish.py mods --mods mods --out OUT_MODS [--prev PREV_OUT_MODS] [--groups tools/catalog-groups.json]
python tools/publish.py upload --out OUT [--dry-run]
python tools/publish.py version
```

- `pack` writes `OUT/site/` (Pages content) and `OUT/assets/` (only the packs `--prev` does not have).
  `--version auto` is `v` + bundleVersion of the Unity project. `--catalogue-mods` defaults to `Mods/*`: no mod ships inside
  the game.
- `mods` writes one archive per mod (`<id>-<version>-<hash16>.zip`) and `catalog.json`. Russian texts come
  from `catalog.ru.json` beside a mod's `package.json` or from `--texts tools/catalog-texts-ru.json`.
  Groups come from `--groups tools/catalog-groups.json` (both files are empty templates for now).
- `upload` creates the GitHub release (`v0.x.y`, a prerelease for `test`; or `mods-YYYYMMDD-HHMMSS`) with
  `gh` and starts `publish-pages`. The workflow `promote-release` moves a test release to production.
- `--base-url http://127.0.0.1:PORT/` makes a local test site; `tools/test_server.py` serves it with
  Range, gzip and throttling. The launcher tests use both.

Workflows in `.github/workflows/`: `launcher-build` (build, test, rolling release `launcher-latest` with
`OmegaLauncher.exe` and `launcher-version.json`), `publish-pages`, `promote-release`.

## Not done yet

- The GitHub repository `bigtester8498-dev/OmegaProject` and its Pages site do not exist; no workflow has
  run and nothing is published.
- The icon (`tools/make_icon.py`: a white Omega sign on a dark square) and the site page are placeholders.
- No pack rule splits content yet; add one when a content pack nears 300 MB.
- The mod catalogue has no groups or Russian texts (`tools/catalog-*.json` are empty).
