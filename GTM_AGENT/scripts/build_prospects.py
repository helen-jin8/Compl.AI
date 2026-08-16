"""Build the prospect list from sourced leads.

Two sources feed one list:
  - kickstarter : US live Technology campaigns scraped via Apify
                  (shahidirfan/Kickstarter-Scraper, run 2026-08-15). Every row is
                  independently verifiable — open `url` and the funding, backers,
                  days-left, location and creator profile are all on the page.
  - accelerator : Bay Area / Berkeley early-stage hardware startups from named
                  accelerator programs (see data/accelerators.json).

Scoping is deterministic: blurb/keywords -> device attributes -> standards, the
same rules-table idea as src/analyst.py. This produces the free-report scope that
the outbound email carries. FCC-grant status is left `unchecked` here (the live
lookup needs network); the honest caveat travels with it.

    python scripts/build_prospects.py     # writes data/prospects.json + .csv
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"

# --- Curated tier-A US hardware leads from the Kickstarter scrape ------------
# Fields copied verbatim from the Apify dataset (dataset BsOfOuRsH9vflujB7).
KICKSTARTER = [
    # company, product, url, creator_profile, location, state, usd_pledged, backers, days_left, pct_funded, deadline, blurb
    ("Mondo Robotics", "Beni All-Terrain Camera Robot", "https://www.kickstarter.com/projects/mondorobotics/beni-all-terrain-camera-robot", "https://www.kickstarter.com/profile/mondorobotics", "Palo Alto", "CA", 2866939, 4578, 22, 5733.88, "2026-09-06", "4K imaging, smart auto-following, 17.9 mph, obstacle jumping, auto-edited highlights"),
    ("Minimal Company", "Minimal Phone 2 (5G QWERTY phone)", "https://www.kickstarter.com/projects/minimalcompany/minimal-phone-2-the-modern-qwerty-phone", "https://www.kickstarter.com/profile/minimalcompany", "Los Angeles", "CA", 1184940, 1798, 25, 1184.94, "2026-09-09", "A focused 5G Android phone with a physical QWERTY keyboard and OLED display"),
    ("Lumistar", "LUMISTAR CARRY AI Basketball Trainer", "https://www.kickstarter.com/projects/1596816961/lumistar-carry-ai-quad-camera-basketball-training-partner", "https://www.kickstarter.com/profile/1596816961", "Dover", "DE", 1175953, 422, 6, 11759.53, "2026-08-21", "Quad-camera AI, 190 court tracking, gesture command, biometric analytics, 4H battery"),
    ("Unseen Reality", "URXR One Spatial Display Glasses", "https://www.kickstarter.com/projects/urxrone-glasses/urxr-one-lightweight-spatial-display-glasses", "https://www.kickstarter.com/profile/urxrone-glasses", "Mountain View", "CA", 793547, 1002, 34, 1587.09, "2026-09-18", "6DoF room-scale tracking, hand-gesture recognition, video see-through in a 93g frame"),
    ("Waydoo", "Waydoo UniRide eSUP (electric hydrofoil)", "https://www.kickstarter.com/projects/waydootech/waydoo-uniride-esup-one-modular-core-endless-ways-to-ride", "https://www.kickstarter.com/profile/waydootech", "San Diego", "CA", 581591, 179, 19, 5815.91, "2026-09-03", "Modular electric water craft powered by the next-generation UniRide core"),
    ("Litejam Guitars", "Litejam Neo RGB Guitar", "https://www.kickstarter.com/projects/litejam/litejam-neo-a1-the-worlds-first-rgb-acoustic-guitar", "https://www.kickstarter.com/profile/litejam", "San Francisco", "CA", 399669, 858, 27, 3996.69, "2026-09-11", "RGB fretboard shows chords, scales and songs; learn faster and perform anywhere"),
    ("PLX Devices", "XFoil Apex Electric Hydrofoil", "https://www.kickstarter.com/projects/plxdevices/xfoil-apex-gen-4", "https://www.kickstarter.com/profile/plxdevices", "Fremont", "CA", 164086, 30, 20, 820.43, "2026-09-04", "A production-ready full carbon fiber electric hydrofoil, engineered for control"),
    ("Iris Solar Technology", "Iris T1 Portable Solar Generator", "https://www.kickstarter.com/projects/iris-solar/iris-t1-portable-solar-power-anywhere-you-go", "https://www.kickstarter.com/profile/iris-solar", "Santa Barbara", "CA", 134172, 135, 14, 2683.44, "2026-08-29", "All-in-one portable solar generator with a built-in battery and zero cables"),
    ("CodeeBot", "CodeeBot GPT Coding Robot Kit (kids)", "https://www.kickstarter.com/projects/codeebot/codeebot-gpt-powered-screen-free-coding-block-robot-kit", "https://www.kickstarter.com/profile/codeebot", "Dover", "DE", 101522, 201, 20, 1015.22, "2026-09-04", "Screen-free coding meets brick-building fun with an AI tutor, for kids"),
    ("Woertec", "AIVU AI Recognition Glasses", "https://www.kickstarter.com/projects/816687468/aivu-1st-ai-object-recognition-privacy-waveguide-glasses", "https://www.kickstarter.com/profile/816687468", "Brighton", "CO", 93173, 231, 30, 931.73, "2026-09-14", "Privacy-first AI glasses, 45g, invisible teleprompter, navigation, open-ear audio"),
    ("NEXIV", "GFF S2-25 Portable Smart Display", "https://www.kickstarter.com/projects/1805586661/gff-s2-25-the-portable-smart-display-that-moves-with-you", "https://www.kickstarter.com/profile/1805586661", "Dover", "DE", 60366, 143, 13, 2012.20, "2026-08-28", "24.5in touchscreen, Google EDLA + L1 certified, Android 15, built-in 5H battery"),
    ("DuoSound", "DuoSound Surface Speakers", "https://www.kickstarter.com/projects/223872568/duosound-turn-everyday-surfaces-into-speakers-0", "https://www.kickstarter.com/profile/223872568", "San Francisco", "CA", 38275, 550, 4, 5888.46, "2026-08-19", "Dual 7.5W detachable speakers, TWS stereo, Bluetooth 5.4, USB-C, 8-hour playback"),
    ("Tensio", "Tensio Dual Wearable for Lifters", "https://www.kickstarter.com/projects/tensio/tensio-the-dual-wearable-for-lifters", "https://www.kickstarter.com/profile/tensio", "Cincinnati", "OH", 28611, 55, 13, 95.37, "2026-08-28", "Auto rep tracking, time under tension, L/R asymmetry, 30+ day battery, screen-free"),
    ("AIROVALT", "AIROVALT M1 Mini Air Compressor", "https://www.kickstarter.com/projects/2121229988/airovalt-m1-the-mini-air-compressor-engineered-to-move", "https://www.kickstarter.com/profile/2121229988", "Colorado Springs", "CO", 24741, 125, 14, 824.70, "2026-08-29", "4.4lb, 116 PSI max, cordless, integrated battery, smart digital display"),
    ("Pants for Birds LLC", "ADSBee Winglet ADS-B Receiver", "https://www.kickstarter.com/projects/pantsforbirds/adsbee-winglet", "https://www.kickstarter.com/profile/pantsforbirds", "Campbell", "CA", 21616, 56, 2, 24.70, "2026-08-17", "Open source ADS-B receiver for portable aircraft tracking and electronic flight bag"),
    ("Mojawa", "Purra Flow AI Coaching Headphones", "https://www.kickstarter.com/projects/mojawa/purra-flow-bone-conduction-headphones-powered-by-ai-coach", "https://www.kickstarter.com/profile/mojawa", "New York", "NY", 21597, 149, 27, 1079.85, "2026-09-11", "Real-time heart rate, 15H battery, open-ear, IP68, bone conduction, AI coach"),
    ("Weclay Inc.", "Weclay Paper Color E-Ink Canvas", "https://www.kickstarter.com/projects/weclay-paper/weclay-paper-self-updating-color-e-ink-canvas", "https://www.kickstarter.com/profile/weclay-paper", "Issaquah", "WA", 15355, 47, 26, 639.79, "2026-09-10", "A self-updating 10in color e-ink canvas with customizable apps and long battery"),
    ("Lumi", "Lumi Smart Ring (mood/stress)", "https://www.kickstarter.com/projects/lumiagent/lumi-ring-customizable-ring-for-mood-stress-and-style", "https://www.kickstarter.com/profile/lumiagent", "San Francisco", "CA", 10189, 3, 34, 101.89, "2026-09-18", "24/7 wearable ring turning daily life into emotional insight and digital identity"),
    ("Vesyn", "VESYN HALO AI ANC Headphones", "https://www.kickstarter.com/projects/vesyn/vesyn-halo-anc-ai-headphones-with-magnetic-digital-badge", "https://www.kickstarter.com/profile/vesyn", "Denver", "CO", 7906, 67, 7, 790.60, "2026-08-22", "3-mic hybrid ANC, digital display badge, ChatGPT voice assistant, 60H battery"),
    ("Globalscale Technologies Inc", "Case8 AI Cyberdeck Platform", "https://www.kickstarter.com/projects/874883570/case8", "https://www.kickstarter.com/profile/874883570", "Anaheim", "CA", 13667, 7, 14, 73.88, "2026-08-29", "A cyberdeck-inspired AI-capable gaming, automation and education platform"),
]

# blurb keyword -> device attribute
ATTR_RULES = {
    "intentional_radiator": ["wireless", "bluetooth", "wifi", "wi-fi", "5g", "radio",
                             "app control", "app-control", "tws", "ads-b", "gesture",
                             "smart", "ai coach", "chatgpt", "connected", "tracking", "receiver"],
    "lithium_cell": ["battery", "rechargeable", "portable", "cordless", "power bank",
                     "power station", "solar generator", "playback", "wearable", "ring", "cell"],
    "mains_or_usb_powered_electronics": ["usb-c", "usb", "display", "touchscreen", "screen",
                                         "speaker", "electronics", "digital", "compressor", "motor"],
    "sold_to_children": ["kids", "children", "for kids"],
    "light_emitting": ["rgb", "led", "light", "lamp", "laser", "uv"],
}

# attribute -> (standards with clause cites). Mirrors data/standards.yaml intent.
STANDARDS = {
    "intentional_radiator": [
        ("47 CFR Part 15 Subpart C", "47 CFR 15.247/15.249", "intentional radiator (radio) certification"),
        ("FCC KDB 447498", "KDB 447498 D01", "RF exposure evaluation for a body-worn/handheld radio"),
    ],
    "lithium_cell": [
        ("UN 38.3", "UN Manual of Tests and Criteria 38.3", "lithium battery transport testing"),
        ("UL 2054", "UL 2054", "household/commercial battery safety"),
        ("IEC 62133-2", "IEC 62133-2:2017", "secondary lithium cell/battery safety"),
    ],
    "mains_or_usb_powered_electronics": [
        ("UL 62368-1", "UL 62368-1", "audio/video and IT equipment safety"),
    ],
    "sold_to_children": [
        ("CPSIA", "16 CFR Part 1250 / ASTM F963", "children's product safety and testing"),
    ],
    "light_emitting": [
        ("IEC 62471", "IEC 62471", "photobiological safety of lamps and LED systems"),
    ],
}


def detect_attributes(text: str) -> dict:
    t = text.lower()
    attrs = {}
    for attr, kws in ATTR_RULES.items():
        attrs[attr] = any(k in t for k in kws)
    return attrs


def scope(attrs: dict) -> list[dict]:
    seen, out = set(), []
    for attr, on in attrs.items():
        if not on:
            continue
        for sid, cite, because in STANDARDS.get(attr, []):
            if sid in seen:
                continue
            seen.add(sid)
            out.append({"id": sid, "cite": cite, "because": because})
    return out


def tier(attrs: dict) -> str:
    if attrs.get("intentional_radiator") or attrs.get("lithium_cell"):
        # radio or battery + (assumed) no grant on file + shipping soon -> A
        return "A"
    return "B"


def build_kickstarter() -> list[dict]:
    rows = []
    for (company, product, url, prof, city, st, pledged, backers, days_left,
         pct, deadline, blurb) in KICKSTARTER:
        attrs = detect_attributes(f"{product} {blurb}")
        standards = scope(attrs)
        rows.append({
            "source": "kickstarter",
            "company": company,
            "product": product,
            "location": f"{city}, {st}",
            "country": "US",
            # verifiable campaign facts (open the URL to confirm)
            "campaign_url": url,
            "creator_profile_url": prof,
            "usd_pledged": pledged,
            "backers": backers,
            "percent_funded": pct,
            "days_left": days_left,
            "deadline": deadline,
            "blurb": blurb,
            # scoped deliverable
            "attributes": {k: v for k, v in attrs.items() if v},
            "standards": [s["id"] for s in standards],
            "standards_detail": standards,
            "tier": tier(attrs),
            "fcc": {"checked": False, "note": "absence-of-grant check pending (needs live FCC lookup)"},
            # enrichment (to fill via Apollo/Clay or web)
            "founder_name": None,
            "founder_title": None,
            "linkedin_url": None,
            "company_domain": None,
            "email": None,
            "enrichment_status": "pending",
        })
    return rows


def main():
    accel_path = DATA / "accelerators.json"
    accelerator = json.loads(accel_path.read_text()) if accel_path.exists() else []
    prospects = build_kickstarter() + accelerator

    (DATA / "prospects.json").write_text(json.dumps(prospects, indent=2))

    cols = ["source", "company", "product", "location", "country", "tier", "standards",
            "usd_pledged", "backers", "days_left", "deadline", "campaign_url",
            "creator_profile_url", "founder_name", "founder_title", "linkedin_url",
            "company_domain", "email", "enrichment_status"]
    with (DATA / "prospects.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for p in prospects:
            row = dict(p)
            row["standards"] = "; ".join(p.get("standards", []))
            w.writerow(row)

    a = sum(1 for p in prospects if p.get("tier") == "A")
    print(f"wrote {len(prospects)} prospects ({a} tier-A) to data/prospects.json + .csv")
    ks = sum(1 for p in prospects if p["source"] == "kickstarter")
    ac = len(prospects) - ks
    print(f"  kickstarter: {ks}   accelerator: {ac}")


if __name__ == "__main__":
    main()
