#!/usr/bin/env bash
# Copy package folders of this repository to OBS and commit them there.
#   scripts/sync-to-obs.sh [package...]     (default: every synced package)
# Only adds and updates files: files deleted here are NOT deleted on OBS
# (remove them in the OBS web UI), so OBS-only files such as the repository
# signing key are kept.
# Needs osc configured with OBS credentials. DRY_RUN=1: show, do not commit.
set -euo pipefail

OBS_PROJECT="${OBS_PROJECT:-home:Luthenis:ogc-handheld}"
OBS_API="${OBS_API:-https://api.opensuse.org}"

# Packages whose sources live here. Not synced:
#   kernel-ogc, kernel-tkg, jupiter-hw-support, steam-jupiter-bootstrap
#       updated on OBS by ocelado-linux/ogc-kernel-updater-obs
#   ocelado-installer   branch of openSUSE:Factory/agama-installer (_link)
#   ogc-handheld-image  build disabled, replaced by the installer
SYNCED="deckifier ocelado-agama ocelado-plasma-fixes ocelado-release patterns-ogc-handheld plymouth-theme-ibm"

cd "$(dirname "$0")/.."
pkgs="${*:-$SYNCED}"
msg="$(git log -1 --format='%s' 2>/dev/null || echo 'sync from GitHub')"
rev="$(git rev-parse --short HEAD 2>/dev/null || echo '?')"
msg="$msg (github.com/ocelado-linux/ocelado-packages@$rev)"

status=0
for p in $pkgs; do
    if ! grep -qw -- "$p" <<<"$SYNCED"; then
        echo "== $p: not synced from GitHub, skipped"; continue
    fi
    [ -d "$p" ] || { echo "== $p: no such folder" >&2; status=1; continue; }
    echo "== $p"
    work="$(mktemp -d)"
    osc -A "$OBS_API" checkout -o "$work/pkg" "$OBS_PROJECT" "$p" >/dev/null
    for f in "$p"/*; do
        [ -f "$f" ] || continue
        b="$(basename "$f")"
        if [ ! -e "$work/pkg/$b" ]; then
            cp "$f" "$work/pkg/$b"; (cd "$work/pkg" && osc add "$b" >/dev/null)
            echo "   new      $b"
        elif ! cmp -s "$f" "$work/pkg/$b"; then
            cp "$f" "$work/pkg/$b"
            echo "   changed  $b"
        fi
    done
    if [ -z "$(cd "$work/pkg" && osc status)" ]; then
        echo "   up to date"
    elif [ -n "${DRY_RUN:-}" ]; then
        echo "   (dry run, not committed)"
    else
        (cd "$work/pkg" && osc -A "$OBS_API" commit --noservice -m "$msg") || status=1
    fi
    rm -rf "$work"
done
exit $status
