# Omega

Launcher and download page of **Omega** (working title).

**Download:** https://bigtester8498-dev.github.io/OmegaProject/

The launcher (Windows 10/11, one exe, nothing to install):

- installs the game and updates it, downloading only the parts that changed;
- checks and repairs the game files;
- manages mods: enable, disable, load order, a whole group of mods with one box;
- has a mod catalogue: install, update and remove mods;
- updates itself.

Put `OmegaLauncher.exe` into an empty folder of its own and run it. The game is installed beside it.

## Building

```
dotnet build launcher/OmegaLauncher.sln -c Release
dotnet test launcher/OmegaLauncher.sln -c Release
```

The tests need Python on PATH. `docs/LAUNCHER.md` describes the site files and publishing (`tools/publish.py`).
