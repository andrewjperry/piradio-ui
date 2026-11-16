# piradio-ui

The station-grid web page from [musicbox-ui](https://github.com/andrewjperry/musicbox-ui), adapted for a Raspberry Pi 4 with a small touchscreen, running Mopidy.

- `index.html` is the page. It talks to Mopidy over its JSON-RPC WebSocket and defaults to the host it was served from (`location.hostname:6680`). It adds a **Shuffle My Music** tile and a Next button for local music.
- `piradio.sh [start|stop|restart]` opens the page as a full-screen app window on the touchscreen (Chromium on Wayland). Copy it to `~/bin`.
- `make-shuffle-playlist.py` writes the "Shuffle My Music" playlist from `~/Music`. Run with no flag for a dry run, or `sudo python3 make-shuffle-playlist.py --write`.

Serve the page with `python3 -m http.server 8000` in its folder, and add the page's address to `allowed_origins` in the `[http]` section of `/etc/mopidy/mopidy.conf`.
