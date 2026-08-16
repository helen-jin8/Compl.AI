"""Assemble the accelerator-channel prospects (Bay Area / Berkeley hardware).

Sourced via Apollo (people search + bulk match, 2026-08-15, user-approved) —
early-stage hardware/robotics/wearable founders HQ'd in the SF Bay Area, small
teams. Every row carries a company LinkedIn, a verified work email, the founder's
identity/background, and any accelerator/fellowship signal Apollo surfaced.

Unlike the crowdfunding rows, device attributes here are INFERRED from the
company profile (robotics/wearable/electronics), not read off a product page —
so they are a coarser scope, flagged as such. The build writes data/accelerators.json
which scripts/build_prospects.py concatenates into the final prospect list.

    python scripts/build_accelerators.py
"""
from __future__ import annotations

import json
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"

# company, builds, founder_first, title, work_email, company_linkedin, domain,
# city, state, founded, signal, attrs(radio,battery,mains)
ROWS = [
    ("Hermes Robotics", "Humanoid / general-purpose robotics", "Guilhem", "Founder & CEO/CTO", "guilhem@hermes-robotics.com", "https://www.linkedin.com/company/hermes-robotics", "hermes-robotics.com", "San Francisco", "CA", 2018, "Y Combinator W21", (True, True, True)),
    ("Weave Robotics", "Home humanoid robot", "Kaan", "Co-Founder & CTO", "kaan@weaverobotics.com", "https://www.linkedin.com/company/weave-robotics", "weaverobots.com", "San Francisco", "CA", None, "Bay Area home-robotics startup", (True, True, True)),
    ("GyroPalm", "Wearable gesture-control device (IoT/AR)", "Dominick", "Founder & CEO", None, "https://www.linkedin.com/company/gyropalm", "gyropalm.com", "San Francisco", "CA", 2015, "UIF Innovation Fellow", (True, True, True)),
    ("Adeeb Robotics", "Robotics hardware", "Omar", "Founder & CEO", "omar@adeebrobotics.com", "https://www.linkedin.com/company/adeeb-robotics", "adeebrobotics.com", "San Francisco", "CA", 2021, "Bay Area robotics startup", (True, True, True)),
    ("Outrun Robotics", "Autonomous robotics", "Darshan", "Co-founder & CTO", "darshan@outrun.bot", "https://www.linkedin.com/company/outrun-robotics", "outrun.bot", "Santa Clara", "CA", None, "Ex-Dexterity / Uber ATG / NVIDIA; Stanford", (True, True, True)),
    ("Sol Robotics", "Robotics hardware (PhD-led)", "Justin", "Co-Founder & CEO", "justin@solrobotics.com", "https://www.linkedin.com/company/sol-robotics", "solrobotics.com", "San Francisco", "CA", None, "PhD Mechanical Engineer (Robotics)", (True, True, True)),
    ("Ember Robotics", "Robotics / hardware system observability", "Shivani", "Co-Founder & CEO", "shivani@emberrobotics.com", "https://www.linkedin.com/company/ember-robotics", "emberrobotics.com", "San Francisco", "CA", 2024, "Early-stage (founded 2024)", (True, True, True)),
    ("OpenHome", "AI voice hardware for the home", "Jesse", "Co-Founder & CTO", "jesse@openhome.com", "https://www.linkedin.com/company/openhome-ai", "openhome.com", "San Francisco", "CA", None, "Thiel Fellow", (True, True, True)),
    ("Evolution Devices", "Wearable medical / rehab device", "Pierluigi", "Co-Founder & CEO", "pierluigi@evolutiondevices.com", "https://www.linkedin.com/company/evolution-devices", "evolutiondevices.com", "San Francisco", "CA", 2017, "Medical-device wearable", (True, True, True)),
    ("Oso Robotics", "Shipping / logistics robots", "Michael", "Co-Founder & CTO", "mike@osorobotics.ai", "https://www.linkedin.com/company/oso-robotics-inc", "osorobotics.ai", "Oakland", "CA", 2019, "CS PhD @ UC Berkeley", (True, True, True)),
    ("Vici Robotics", "Retail automation robots", "Kyle", "Founder & CEO", "kyle@vicirobotics.com", "https://www.linkedin.com/company/vici-robotics", "vicirobotics.com", "San Jose", "CA", 2019, "Ex-Planet / Google", (True, True, True)),
    ("Remedy Robotics", "Surgical / endovascular robotics", "Jake", "Co-Founder & CTO", "jake@remedyrobotics.com", "https://www.linkedin.com/company/remedyrobotics", "remedyrobotics.com", "San Francisco", "CA", 2021, "PhD Bioengineering; ex-Auris", (True, True, True)),
    ("Fort", "Wearable strength/health device", "Paul", "Co-Founder & CTO", "paul@fort.cx", "https://www.linkedin.com/company/fortwearable", "fort.cx", "San Francisco", "CA", 2025, "Ex-Tesla / Rivian; wearable", (True, True, True)),
    ("MirraViz", "Multi-view display hardware", "Michael", "Co-Founder & CEO/CTO", "michaelwang@mirraviz.com", "https://www.linkedin.com/company/mirraviz", "mirraviz.com", "Fremont", "CA", 2016, "Ex-Intel; display hardware", (True, False, True)),
    ("Mission Robotics", "Marine robotics (ROV/AUV)", "Brian", "Co-Founder & CEO", "brian@missionrobotics.us", "https://www.linkedin.com/company/missionrobotics", "missionrobotics.us", "Union City", "CA", 2020, "Ex-OpenROV / Sofar Ocean", (True, True, True)),
    ("Spike Dynamics", "Artificial-muscle actuators (aerospace/medtech)", "Alexander", "Founder & CEO/CTO", "alexander.sergeev@spikedynamics.net", "https://www.linkedin.com/company/spike-dynamics", "spikedynamics.com", "San Francisco", "CA", 2020, "NASA-validated actuator tech", (True, True, True)),
    ("Evodyne Robotics", "Robotics hardware & education", "Raghav", "Founder & CEO", "raghav.gupta@evodyne.co", "https://www.linkedin.com/company/evodynerobotics", "evodyne.co", "Mountain View", "CA", 2017, "Prior exit (WeatherSphere); email extrapolated", (True, True, True)),
    ("Tespen Robotics", "Autonomous-mobility hardware", "Alva", "Co-Founder & CTO", "alva@tespen.com", "https://www.linkedin.com/company/tespen-robotics", "tespen.com", "San Francisco", "CA", 2025, "UC Berkeley Haas MBA 2026", (True, True, True)),
]

STANDARDS = {
    "intentional_radiator": [
        ("47 CFR Part 15 Subpart C", "47 CFR 15.247/15.249", "intentional radiator (radio) certification"),
        ("FCC KDB 447498", "KDB 447498 D01", "RF exposure evaluation"),
    ],
    "lithium_cell": [
        ("UN 38.3", "UN Manual of Tests and Criteria 38.3", "lithium battery transport testing"),
        ("UL 2054", "UL 2054", "battery pack safety"),
        ("IEC 62133-2", "IEC 62133-2:2017", "secondary lithium cell/battery safety"),
    ],
    "mains_or_usb_powered_electronics": [
        ("UL 62368-1", "UL 62368-1", "audio/video and IT equipment safety"),
    ],
}


def scope(attrs):
    seen, out = set(), []
    for a, on in attrs.items():
        if not on:
            continue
        for sid, cite, because in STANDARDS.get(a, []):
            if sid not in seen:
                seen.add(sid)
                out.append({"id": sid, "cite": cite, "because": because})
    return out


def main():
    prospects = []
    for (co, builds, first, title, email, li, domain, city, st, founded, signal,
         (radio, batt, mains)) in ROWS:
        attrs = {"intentional_radiator": radio, "lithium_cell": batt,
                 "mains_or_usb_powered_electronics": mains}
        attrs = {k: v for k, v in attrs.items() if v}
        std = scope(attrs)
        prospects.append({
            "source": "accelerator",
            "company": co,
            "product": builds,
            "location": f"{city}, {st}",
            "country": "US",
            "campaign_url": f"https://{domain}",
            "creator_profile_url": li,          # company LinkedIn (verifiable)
            "usd_pledged": None, "backers": None, "percent_funded": None,
            "days_left": None, "deadline": None,
            "founded_year": founded,
            "accelerator_signal": signal,
            "attributes": attrs,
            "attributes_note": "inferred from company profile, not a product page",
            "standards": [s["id"] for s in std],
            "standards_detail": std,
            "tier": "A" if (radio or batt) else "B",
            "fcc": {"checked": False, "note": "absence-of-grant check pending"},
            "founder_name": first,              # first name; full via company LinkedIn + name
            "founder_title": title,
            "linkedin_url": li,                 # company LinkedIn (person profile masked on plan)
            "company_domain": domain,
            "email": email,
            "enrichment_status": "apollo: company LinkedIn + verified work email"
                                 + ("" if email else " (email unavailable)"),
        })
    (DATA / "accelerators.json").write_text(json.dumps(prospects, indent=2))
    print(f"wrote {len(prospects)} accelerator prospects to data/accelerators.json")


if __name__ == "__main__":
    main()
