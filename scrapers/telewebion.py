#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telewebion IPTV Generator
این اسکریپت لینک‌های زنده شبکه‌های IRIB را از سرور Telewebion می‌گیرد
و یک فایل M3U استاندارد می‌سازد.
"""
import requests
import sys
import os
from datetime import datetime, timezone

STREAM_URL_TEMPLATE = "https://ncdn.telewebion.com/{ch}/live/playlist.m3u8"
LOGO_URL_TEMPLATE = "https://static.televebion.net/web/content_images/channel_images/thumbs/new/240/v4/{ch}.png"

CHANNELS = [
    ("IRIB1.ir@HD",    "شبکه ۱ - یک",          "tv1"),
    ("IRIB2.ir@HD",    "شبکه ۲ - دو",          "tv2"),
    ("IRIB3.ir@HD",    "شبکه ۳ - سه",          "tv3"),
    ("IRIB4.ir@HD",    "شبکه ۴ - چهار",        "tv4"),
    ("IRIB5.ir@HD",    "شبکه ۵ - تهران",       "tv5"),
    ("IRIBVarzesh.ir", "شبکه ورزش",            "varzesh"),
    ("IRIBKhabar.ir",  "شبکه خبر",             "irinn"),
    ("IRIBNamayesh.ir","شبکه نمایش",           "namayesh"),
    ("IRIBPooya.ir",   "شبکه پویا",            "pooya"),
    ("IRIBNasim.ir",   "شبکه نسیم",            "nasim"),
    ("IRIBOmid.ir",    "شبکه امید",            "omid"),
    ("IRIBIfilm.ir",   "آی‌فیلم",              "ifilm"),
    ("IRIBMostanad.ir","مستند",                "mostanad"),
    ("IRIBQuran.ir",   "قرآن",                 "quran"),
    ("IRIBSalamat.ir", "سلامت",                "salamat"),
    ("IRIBAmoozesh.ir","آموزش",                "amoozesh"),
    ("IRIBJamejam.ir", "جام جم",               "jamejam"),
    ("IRIBBazar.ir",   "بازار",                "bazar"),
    ("IRIBOfogh.ir",   "افق",                  "ofogh"),
    ("IRIBIranKala.ir","ایران کالا",           "irankala"),
    ("IRIBShoma.ir",   "شما",                  "shoma"),
    ("IRIBTamasha.ir", "تماشا",                "tamasha"),
    ("IRIBNavar.ir",   "نوار",                 "navar"),
]

GROUP_NAME = "IRIB"
OUTPUT_FILE = "playlists/irib.m3u"
TEST_TIMEOUT = 10


def test_stream(url):
    try:
        r = requests.head(url, timeout=TEST_TIMEOUT, allow_redirects=True)
        return r.status_code == 200
    except Exception:
        return False


def generate_playlist():
    print("Starting IRIB playlist generation from Telewebion")
    print("=" * 60)

    lines = ["#EXTM3U"]
    working = 0
    broken = []

    for tvg_id, display_name, ch_code in CHANNELS:
        stream_url = STREAM_URL_TEMPLATE.format(ch=ch_code)
        logo_url = LOGO_URL_TEMPLATE.format(ch=ch_code)

        print(f"  Testing {display_name} ", end="", flush=True)
        if test_stream(stream_url):
            print("OK")
            extinf = (
                f'#EXTINF:-1 tvg-id="{tvg_id}" '
                f'tvg-logo="{logo_url}" '
                f'group-title="{GROUP_NAME}",{display_name}'
            )
            lines.append(extinf)
            lines.append(stream_url)
            working += 1
        else:
            print("FAILED")
            broken.append(display_name)

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print("=" * 60)
    print(f"Working channels: {working}")
    print(f"Broken channels: {len(broken)}")
    if broken:
        print(f"Broken list: {', '.join(broken)}")
    print(f"Output file: {OUTPUT_FILE}")
    print(f"Time: {datetime.now(timezone.utc).isoformat()}")

    return working


if __name__ == "__main__":
    count = generate_playlist()
    sys.exit(0)
