#!/bin/sh
# Kullanım: npm run build:deb  (önce dist/TurkTV-linux-x64 oluşur, sonra .deb paketlenir)
set -e
S=dist/TurkTV-linux-x64; D=dist/deb; rm -rf "$D"
mkdir -p "$D/opt" "$D/usr/bin" "$D/usr/share/applications" "$D/usr/share/icons/hicolor/256x256/apps" "$D/DEBIAN"
find "$S/locales" -type f ! -name 'en-US.pak' ! -name 'tr.pak' -delete
cp -r "$S" "$D/opt/turk-tv" && mv "$D/opt/turk-tv/TurkTV" "$D/opt/turk-tv/turk-tv"
printf '#!/bin/sh\nexec /opt/turk-tv/turk-tv --no-sandbox "$@"\n' > "$D/usr/bin/turk-tv"
cp icon.png "$D/usr/share/icons/hicolor/256x256/apps/turk-tv.png"
cp packaging/turk-tv.desktop "$D/usr/share/applications/"
cp packaging/control "$D/DEBIAN/control"
chmod 755 "$D/usr/bin/turk-tv" "$D/opt/turk-tv/turk-tv"; chmod -R go-w "$D"; chmod -R a+rX "$D"
dpkg-deb --root-owner-group -Zxz -b "$D" dist/turk-tv_1.0.0_amd64.deb
