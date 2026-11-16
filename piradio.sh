#!/bin/bash
# Start, stop or restart the PiRadio window on the touchscreen.
# Usage: piradio.sh [start|stop|restart]   (no argument = start)

# Lets it work from SSH as well as from the Pi's own terminal.
export XDG_RUNTIME_DIR=${XDG_RUNTIME_DIR:-/run/user/$(id -u)}
export WAYLAND_DISPLAY=${WAYLAND_DISPLAY:-wayland-0}

profile=$HOME/.config/piradio-chromium

running() { pgrep -f -- "--user-data-dir=$profile" >/dev/null; }

stop() {
  running && pkill -f -- "--user-data-dir=$profile"
  while running; do sleep 0.5; done
}

start() {
  if running; then
    echo "PiRadio is already running"
    return
  fi
  rm -f "$profile"/Singleton*   # stale locks from an unclean shutdown
  wlr-randr --output HDMI-A-2 --mode 720x480
  setsid nohup chromium --app=http://localhost:8000 \
    --user-data-dir="$profile" --ozone-platform=wayland \
    --password-store=basic --noerrdialogs --disable-infobars \
    >/dev/null 2>&1 &
  echo "PiRadio started"
}

case "${1:-start}" in
  start)   start ;;
  stop)    stop; echo "PiRadio stopped" ;;
  restart) stop; start ;;
  *)       echo "Usage: piradio.sh [start|stop|restart]"; exit 1 ;;
esac
