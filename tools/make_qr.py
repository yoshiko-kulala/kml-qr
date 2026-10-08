#!/usr/bin/env python3
"""KML QRリーダー用のQR画像を生成する。

依存: pip install "qrcode[pil]"
"""
import argparse
import sys
from urllib.parse import quote
from xml.sax.saxutils import escape

import qrcode
from qrcode.constants import ERROR_CORRECT_M

ICON = "https://maps.google.com/mapfiles/kml/shapes/arrow.png"


def build_kml(lat: str, lng: str, heading: str, name: str) -> str:
    # index.html の buildKml と同じ構造
    return (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<kml xmlns="http://www.opengis.net/kml/2.2"><Placemark>'
        f"<name>{escape(name, {chr(34): '&quot;', chr(39): '&apos;'})}</name>"
        f"<Style><IconStyle><heading>{heading}</heading>"
        f"<Icon><href>{ICON}</href></Icon></IconStyle></Style>"
        f"<Point><coordinates>{lng},{lat}</coordinates></Point></Placemark></kml>"
    )


def fmt(v: float) -> str:
    # WGS84 10進度、小数点以下6桁
    return f"{v:.6f}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--lat", type=float, required=True, help="緯度 (WGS84, 10進度)")
    ap.add_argument("--lng", type=float, required=True, help="経度 (WGS84, 10進度)")
    ap.add_argument("--heading", type=float, required=True, help="方位 (度, 北=0 時計回り)")
    ap.add_argument("--name", default="", help="地点名")
    ap.add_argument("--base-url", default="https://yoshiko-kulala.github.io/kml-qr/",
                    help="リーダーページのURL (--mode url で使用)")
    ap.add_argument("--mode", choices=["url", "kml"], default="url")
    ap.add_argument("-o", "--output", default="qr.png")
    a = ap.parse_args()

    if not -90 <= a.lat <= 90 or not -180 <= a.lng <= 180:
        ap.error("緯度は-90..90、経度は-180..180で指定してください")

    lat, lng = fmt(a.lat), fmt(a.lng)
    hdg = f"{a.heading:g}"
    name = a.name or f"{lat},{lng}"

    if a.mode == "url":
        base = a.base_url.split("#", 1)[0]
        text = f"{base}#lat={lat}&lng={lng}&h={hdg}"
        if a.name:
            text += f"&name={quote(a.name, safe='')}"
    else:
        text = build_kml(lat, lng, hdg, name)

    qr = qrcode.QRCode(error_correction=ERROR_CORRECT_M, box_size=8, border=4)
    qr.add_data(text.encode("utf-8"))  # バイトモードで固定（リーダー側はUTF-8で復号）
    qr.make(fit=True)
    qr.make_image(fill_color="black", back_color="white").save(a.output)

    print(f"mode={a.mode} version={qr.version} length={len(text)} chars "
          f"({len(text.encode('utf-8'))} bytes) -> {a.output}")
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
