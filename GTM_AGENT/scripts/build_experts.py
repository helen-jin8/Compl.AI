"""Contract certification experts — the fallback for the Terac expert-review step.

If the Terac expert pool does not fill (docs/PRD.md §7.8), these are independent
FCC/UL/EMC compliance labs and consultancies that can review and sign a scoping
report, or run the actual accredited testing, on contract. Sourced + enriched via
Apollo (2026-08-15, user-approved). Every row has a verified work email or firm
phone and a LinkedIn (person where available, else company) so a teammate can
verify and reach out.

These accredited labs are also the "Authority" layer in the accuracy chain
(docs/PRD.md §8): the lab's accreditation is what is legally on the line, so a
signed review or a quote from one of these is stronger than any in-house sign-off.

    python scripts/build_experts.py     # writes data/experts.json + experts.csv
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"

# name, title, firm, website, firm_type, specialties, city, state, founded,
# person_linkedin, company_linkedin, email, phone, note
EXPERTS = [
    ("Steven Spadaro", "Owner", "Compliance Testing", "compliancetesting.com",
     "Accredited FCC/EMC test lab + FCC TCB", "FCC Part 15, EMC/EMI, wireless/SAR, ISO 17025/17065, TCB certification",
     "Mesa", "AZ", 1963, "https://www.linkedin.com/in/steven-spadaro-7291bb188",
     "https://www.linkedin.com/company/compliance-testing-llc-aka-compliancetesting-com",
     None, "+1 480-926-3100",
     "ISO-accredited FCC test lab and Telecom Certification Body — can run and grant the actual radio cert, not just review."),
    ("Shirish Sarwate", "President", "Compatible Electronics, Inc.", "celectronics.com",
     "EMC/EMI test lab (CA)", "FCC certification, EMC/EMI, RED, product safety, ISO 17025, TCB",
     "Lake Forest", "CA", 1985, None,
     "https://www.linkedin.com/company/compatible-electronics-inc.",
     "shirish@celectronics.com", "+1 818-597-0600",
     "40-year California EMC lab (also builds Com-Power EMI test gear) — deep FCC/EMC authority, in-state."),
    ("Wendy Fuster", "President", "F2 Labs", "f2labs.com",
     "NRTL EMC + product-safety test lab", "EMC, wireless radio, product safety, IP/NEMA, NRTL",
     "Damascus", "MD", 1991, "https://www.linkedin.com/in/wendy-fuster-5861912b",
     "https://www.linkedin.com/company/f2-labs", "wfuster@f2labs.com", "+1 301-253-4500",
     "Covers both halves of the scope — EMC (FCC) and product safety (UL-type) — under one accredited roof."),
    ("Mario Baraona", "President", "Atlas Compliance & Engineering", "atlasce.com",
     "Accredited EMI/EMC/FCC test lab (Bay Area)", "FCC, EMC/EMI, transmitter certification, immunity, ISO 17025",
     "San Jose", "CA", 1997, None,
     "https://www.linkedin.com/company/atlas-compliance-&-engineering",
     "mbaraona@atlasce.com", "+1 408-971-9743",
     "Bay Area (San Jose) FCC/EMC lab — local to the accelerator-channel prospects for on-site testing."),
    ("Mark Piazza", "Co-Owner / Founder", "CE Conformity Services, LLC", "ceconformity.com",
     "Independent EMC / safety consultancy", "EMC, CE/UKCA marking, machinery safety, risk assessment, IEC 60204-1",
     "Willoughby", "OH", 2019, None,
     "https://www.linkedin.com/company/ce-conformity-services-llc", "mark@ceconformity.com",
     "+1 440-207-0799",
     "Small independent consultancy (ex-Vitamix senior compliance) — flexible contract reviewer for EMC + safety."),
    ("Paul Chen", "Principal Consultant / Founder", "PC Squared Consultants", "consumerproductcompliance.com",
     "Consumer-product safety consultancy", "CPSIA, ASTM F963, children's/toy safety, UL, FCC, CPSC — ex-Walmart",
     "Bentonville", "AR", 2015, "https://www.linkedin.com/in/paul-chen-6358685",
     "https://www.linkedin.com/company/pc-squared-consultants-llc", "paul@lawlabel.com",
     "+1 479-595-8398",
     "CPSC/CPSIA expert for children's products — fits the kids-hardware leads (e.g. CodeeBot) the general lab route misses."),
    ("David Clem", "Owner / Founder", "C & C Technologies Inc.", "candctechinc.com",
     "EMC / environmental test lab", "EMC, environmental & mechanical testing, ingress protection, calibration",
     "Apex", "NC", 1995, "https://www.linkedin.com/in/david-clem-6b356627",
     "https://www.linkedin.com/company/c-&-c-technologies-inc-", "dclem@candctechinc.com",
     "+1 866-938-3782",
     "EMC plus environmental/IP testing — useful for outdoor/rugged hardware in the pipeline."),
    ("John (J.R.) Allen", "President & CEO", "Product Safety Consulting", "productsafetyinc.com",
     "Product-safety consultancy + field evaluations", "UL, CE, ETL, CSA, NRTL field evaluations, wearables/drone/smart-device safety",
     "Bensenville", "IL", None, None,
     "https://www.linkedin.com/company/product-safety-consulting", "jrallen@productsafetyinc.com",
     "+1 877-804-3066",
     "40 years in product safety and certifications — the UL/safety half of the scope, incl. on-site field evaluation."),
]


def main():
    rows = []
    for (name, title, firm, site, ftype, specialties, city, st, founded,
         p_li, c_li, email, phone, note) in EXPERTS:
        rows.append({
            "name": name, "title": title, "firm": firm,
            "website": f"https://{site}", "firm_type": ftype,
            "specialties": specialties, "location": f"{city}, {st}",
            "founded_year": founded,
            "linkedin_person": p_li, "linkedin_company": c_li,
            "email": email, "phone": phone,
            "contract_fit": note,
            "source": "apollo (2026-08-15)",
        })
    (DATA / "experts.json").write_text(json.dumps(rows, indent=2))

    cols = ["name", "title", "firm", "firm_type", "specialties", "location",
            "linkedin_person", "linkedin_company", "email", "phone", "website",
            "founded_year", "contract_fit"]
    with (DATA / "experts.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"wrote {len(rows)} contract certification experts to data/experts.json + .csv")


if __name__ == "__main__":
    main()
