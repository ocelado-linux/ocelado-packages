# Ocelado Linux packages

Packaging sources of [Ocelado Linux](https://github.com/ocelado-linux), a
SteamOS-like openSUSE Tumbleweed for handhelds (Steam Deck, AOKZOE/OneXPlayer)
and desktop PCs. One folder per package of the OBS project
[home:Luthenis:ogc-handheld](https://build.opensuse.org/project/show/home:Luthenis:ogc-handheld).

| Package | What it is |
|---|---|
| `ocelado-release` | Branding (os-release, logo, wallpaper, GRUB theme), system setup, presets, kernel selection, GRUB default kernel |
| `ocelado-plasma-fixes` | Plasma session fixes (kde-baloo ordering cycle); `ocelado-baloo-off` |
| `patterns-ogc-handheld` | Patterns for each edition (base, KDE, Game Mode, Desktop, Desktop Minimal, Deck, AOKZOE) |
| `ocelado-agama` | Agama installer products and branding |
| `ocelado-installer` | Installer ISO (branch of openSUSE:Factory/agama-installer) |
| `deckifier` | Game Mode / Desktop Mode switching; sources in [ocelado-linux/deckifier](https://github.com/ocelado-linux/deckifier) |
| `kernel-ogc`, `kernel-tkg` | OGC and linux-tkg (BORE) kernels |
| `plymouth-theme-ibm` | Default boot splash |
| `jupiter-hw-support`, `steam-jupiter-bootstrap` | Steam Deck support |
| `ogc-handheld-image` | KIWI disk image (build disabled, replaced by the installer) |

Notes:

- `kernel-ogc`, `kernel-tkg`, `jupiter-hw-support`, `steam-jupiter-bootstrap`:
  versions and sources are updated on OBS by
  [ogc-kernel-updater-obs](https://github.com/ocelado-linux/ogc-kernel-updater-obs);
  OBS has the current values.
- Large or generated sources (kernel tarballs, the OBS signing key) are not
  stored here.
- Each package keeps its own `License:`; third-party content (e.g. the IBM
  Plymouth theme, GPL-3.0) keeps its license. Ocelado's own files: MIT.
