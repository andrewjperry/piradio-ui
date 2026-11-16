#!/usr/bin/env python3
"""Build the "Shuffle My Music" playlist for PiRadio from ~/Music.

Dry run (no changes):   python3 make-shuffle-playlist.py
Write the playlist:     sudo python3 make-shuffle-playlist.py --write

Only .mp3, .wma and .m4a files are listed. The artist comes from the top folder
(or the second folder inside "Amazon MP3"); the title comes from the file name
with its track number removed. Rerun with --write after adding albums.
"""
import os
import re
import shutil
import sys

MUSIC = os.path.expanduser(os.environ.get("MUSIC_DIR", "/home/andrew/Music"))
OUT = "/var/lib/mopidy/m3u/Shuffle My Music.m3u"
EXTS = {".mp3", ".wma", ".m4a"}
STORE_FOLDERS = {"Amazon MP3"}  # download folders that hold artist folders


def label(rel_parts):
    folders, filename = rel_parts[:-1], rel_parts[-1]
    if folders and folders[0] in STORE_FOLDERS and len(folders) > 1:
        artist = folders[1]
    elif folders:
        artist = folders[0]
    else:
        artist = ""
    title = re.sub(r"^\s*\d+[\s.\-_]+", "", os.path.splitext(filename)[0]).strip()
    return f"{artist} - {title}" if artist else title


def main():
    entries = []
    for root, dirs, files in os.walk(MUSIC):
        dirs[:] = sorted(d for d in dirs if not d.startswith("."))
        for name in sorted(files):
            if name.startswith(".") or os.path.splitext(name)[1].lower() not in EXTS:
                continue
            path = os.path.join(root, name)
            rel = os.path.relpath(path, MUSIC).split(os.sep)
            entries.append((label(rel), path))

    lines = ["#EXTM3U"]
    for text, path in entries:
        lines.append(f"#EXTINF:-1,{text}")
        lines.append(path)
    body = "\n".join(lines) + "\n"

    if "--write" not in sys.argv:
        print(f"{len(entries)} tracks found under {MUSIC} (dry run, nothing written)")
        for text, path in entries[:3] + entries[-2:]:
            print("  ", text)
        return

    tmp = OUT + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(body)
    shutil.chown(tmp, "mopidy", "audio")
    os.replace(tmp, OUT)
    print(f"Wrote {len(entries)} tracks to {OUT}")


if __name__ == "__main__":
    main()
