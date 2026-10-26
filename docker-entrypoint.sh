#!/bin/bash
set -e

# Если дисплея нет (обычный случай в Docker) — поднимаем виртуальный и
# отдаём его через noVNC, чтобы можно было залогиниться в браузере.
if [ -z "$DISPLAY" ]; then
  export DISPLAY=:99
  Xvfb "$DISPLAY" -screen 0 1366x900x24 -nolisten tcp &
  for _ in $(seq 1 50); do
    [ -e /tmp/.X11-unix/X99 ] && break
    sleep 0.1
  done
  x11vnc -display "$DISPLAY" -forever -shared -nopw -localhost -rfbport 5900 -quiet &
  websockify --web=/usr/share/novnc 6080 127.0.0.1:5900 >/dev/null 2>&1 &
  echo "Браузер для входа в аккаунт: http://localhost:6080/vnc.html?autoconnect=true&resize=scale"
fi

# после жёсткого завершения контейнера в профиле остаются замки Chrome,
# а профиль использует только этот контейнер
if [ -n "$CHROME_PROFILE_DIR" ]; then
  mkdir -p "$CHROME_PROFILE_DIR"
  rm -f "$CHROME_PROFILE_DIR"/SingletonLock \
        "$CHROME_PROFILE_DIR"/SingletonCookie \
        "$CHROME_PROFILE_DIR"/SingletonSocket
fi

exec "$@"
