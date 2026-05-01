import streamlit as st
import pandas as pd
from datetime import date, datetime, timedelta
import io

st.set_page_config(
    page_title="ScholarshipHunter Pro — Hassan Iqbal",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
html, body, [class*="css"] { font-family: 'Sora', sans-serif !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0.5rem !important; max-width: 1400px; }

/* ── AUTHOR STRIP ── */
.author-strip {
    background: linear-gradient(90deg, #0a1628 0%, #0d2d6b 50%, #0a1628 100%);
    border-bottom: 1px solid rgba(30,109,229,0.4);
    padding: 10px 32px;
    display: flex; align-items: center; justify-content: space-between;
    flex-wrap: wrap; gap: 8px;
}
.author-name {
    font-size: 0.92em; font-weight: 700;
    background: linear-gradient(90deg, #63b3ed, #a78bfa);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    letter-spacing: 0.3px;
}
.author-detail { font-size: 0.78em; color: rgba(255,255,255,0.5); }
.author-badge {
    background: rgba(30,109,229,0.2); border: 1px solid rgba(30,109,229,0.4);
    color: #63b3ed; padding: 3px 12px; border-radius: 20px; font-size: 0.75em; font-weight: 600;
}

/* ── HERO ── */
.hero {
    background: linear-gradient(135deg, #040d1f 0%, #071533 40%, #0a2050 70%, #0d2d6b 100%);
    border: 1px solid rgba(30,109,229,0.3); border-radius: 18px;
    padding: 32px 40px; margin-bottom: 20px; position: relative; overflow: hidden;
}
.hero::before {
    content:''; position:absolute; top:-60px; right:-60px;
    width:300px; height:300px;
    background:radial-gradient(circle,rgba(30,109,229,0.15) 0%,transparent 70%); border-radius:50%;
}
.hero h1 {
    font-size:2em; font-weight:800; margin:0 0 6px;
    background:linear-gradient(90deg,#ffffff,#63b3ed);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; letter-spacing:-0.5px;
}
.hero p { color:rgba(255,255,255,0.65); margin:0; font-size:0.95em; font-weight:300; }
.hero .badges { margin-top:14px; display:flex; flex-wrap:wrap; gap:8px; }
.hero .hbadge {
    background:rgba(30,109,229,0.2); border:1px solid rgba(30,109,229,0.4);
    color:#63b3ed; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:500;
}

/* ── SEARCH BAR ── */
.search-wrap {
    background: linear-gradient(145deg,#0f1e35,#131929);
    border:1px solid rgba(30,109,229,0.25); border-radius:14px;
    padding:18px 22px; margin-bottom:18px;
}
.search-wrap h4 { color:#63b3ed; margin:0 0 10px; font-size:0.95em; font-weight:600; }

/* ── STAT CARDS ── */
.stat-row { display:flex; gap:10px; flex-wrap:wrap; margin-bottom:18px; }
.stat-card {
    flex:1; min-width:100px;
    background:linear-gradient(145deg,#131929,#0f1e35);
    border:1px solid rgba(30,109,229,0.2); border-radius:12px; padding:12px 14px; text-align:center;
}
.stat-num { font-size:1.9em; font-weight:800; color:#63b3ed; font-family:'JetBrains Mono',monospace; }
.stat-label { font-size:0.7em; color:rgba(255,255,255,0.5); margin-top:3px; text-transform:uppercase; letter-spacing:0.5px; }

/* ── SCHOLARSHIP CARDS ── */
.sch-card {
    background:linear-gradient(145deg,#111827,#0f1e35);
    border:1px solid rgba(255,255,255,0.08); border-radius:14px;
    padding:18px 22px; margin-bottom:12px;
}
.sch-card.hidden-gem {
    border-left:4px solid #f97316;
    background:linear-gradient(145deg,#1a1008,#111827);
}
.sch-card.rtp-type {
    border-left:4px solid #34d399;
    background:linear-gradient(145deg,#081a10,#111827);
}
.sch-card h3 { font-size:1.02em; font-weight:700; color:#e8edf5; margin:0 0 8px; }
.sch-meta { display:flex; justify-content:space-between; flex-wrap:wrap; gap:8px; margin-bottom:10px; }
.deadline-urgent { color:#f87171; font-weight:700; font-size:0.87em; }
.deadline-warn   { color:#fbbf24; font-weight:600; font-size:0.87em; }
.deadline-ok     { color:#34d399; font-weight:600; font-size:0.87em; }
.deadline-roll   { color:#9ca3af; font-style:italic; font-size:0.87em; }

/* ── BADGES ── */
.badge { display:inline-block; padding:3px 9px; border-radius:20px; font-size:0.72em; font-weight:600; margin:2px 2px 2px 0; }
.b-region   { background:rgba(30,109,229,0.2);  color:#63b3ed;  border:1px solid rgba(30,109,229,0.3); }
.b-field    { background:rgba(52,211,153,0.15); color:#34d399;  border:1px solid rgba(52,211,153,0.25); }
.b-degree   { background:rgba(167,139,250,0.15);color:#a78bfa;  border:1px solid rgba(167,139,250,0.25); }
.b-lang     { background:rgba(251,191,36,0.15); color:#fbbf24;  border:1px solid rgba(251,191,36,0.25); }
.b-hidden   { background:rgba(249,115,22,0.15); color:#f97316;  border:1px solid rgba(249,115,22,0.3); }
.b-funded   { background:rgba(52,211,153,0.12); color:#6ee7b7;  border:1px solid rgba(52,211,153,0.2); }
.b-partial  { background:rgba(251,191,36,0.12); color:#fde68a;  border:1px solid rgba(251,191,36,0.2); }
.b-hec      { background:rgba(99,102,241,0.15); color:#a5b4fc;  border:1px solid rgba(99,102,241,0.25); }
.b-schengen { background:rgba(14,165,233,0.15); color:#38bdf8;  border:1px solid rgba(14,165,233,0.25); }
.b-waiver   { background:rgba(52,211,153,0.1);  color:#6ee7b7;  border:1px solid rgba(52,211,153,0.2); }
.b-rtp      { background:rgba(52,211,153,0.2);  color:#34d399;  border:1px solid rgba(52,211,153,0.4); font-weight:700; }

.coverage-box {
    background:rgba(30,109,229,0.08); border-left:3px solid rgba(30,109,229,0.5);
    border-radius:0 8px 8px 0; padding:7px 12px; margin:9px 0;
    font-size:0.86em; color:#93c5fd;
}
.insight-box {
    background:rgba(255,255,255,0.04); border-radius:8px;
    padding:7px 12px; margin:7px 0; font-size:0.84em; color:rgba(255,255,255,0.6);
    border:1px solid rgba(255,255,255,0.07);
}
.link-apply {
    display:inline-block; background:linear-gradient(135deg,#1e6de5,#1a5cd4);
    color:white !important; text-decoration:none !important;
    padding:7px 16px; border-radius:8px; font-size:0.84em; font-weight:600;
    margin-right:8px; margin-top:7px; border:1px solid rgba(255,255,255,0.1);
}
.link-portal {
    display:inline-block; background:rgba(255,255,255,0.07);
    color:rgba(255,255,255,0.7) !important; text-decoration:none !important;
    padding:7px 16px; border-radius:8px; font-size:0.84em; font-weight:500;
    margin-top:7px; border:1px solid rgba(255,255,255,0.1);
}
.cal-wrap { overflow-x:auto; border-radius:12px; border:1px solid rgba(255,255,255,0.08); }
table.cal { width:100%; border-collapse:collapse; font-size:0.83em; }
table.cal th { background:#0d2d6b; color:#63b3ed; padding:10px 13px; text-align:left; white-space:nowrap; }
table.cal td { padding:8px 13px; border-bottom:1px solid rgba(255,255,255,0.05); color:#cbd5e1; }
table.cal tr.urgent td { background:rgba(249,115,22,0.07); }
table.cal tr.warn   td { background:rgba(251,191,36,0.06); }
table.cal tr.ok     td { background:rgba(52,211,153,0.04); }
[data-testid="stSidebar"] {
    background:linear-gradient(180deg,#0b0f1a 0%,#0d1529 100%) !important;
    border-right:1px solid rgba(30,109,229,0.2) !important;
}
.section-head {
    font-size:1.05em; font-weight:700; color:#63b3ed;
    margin:16px 0 10px; padding-bottom:7px;
    border-bottom:1px solid rgba(30,109,229,0.2);
}
.divider { border:none; border-top:1px solid rgba(255,255,255,0.06); margin:10px 0; }
.no-results { text-align:center; padding:44px 24px; color:rgba(255,255,255,0.4); }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════
# DATABASE
# ══════════════════════════════════════════════════════════════════════════
@st.cache_data
def build_database():
    today = date.today()
    def project(dm, dd, om, od):
        for yr in range(0, 3):
            try:
                dl = date(today.year + yr, dm, dd)
                if dl > today + timedelta(days=14):
                    op = date(today.year + yr, om, od)
                    if op >= dl:
                        op = date(today.year + yr - 1, om, od)
                    sess = f"Fall {dl.year}" if dl.month <= 4 else (f"Winter {dl.year}/{dl.year+1}" if dl.month <= 8 else f"Fall {dl.year+1}")
                    return str(dl), str(op), sess
            except ValueError:
                pass
        return "Rolling", "Year-round", "Rolling"

    T = [
        # ══ EUROPE ══
        dict(name="DAAD Research Grants", country="Germany", region="Europe", schengen=True,
             fields=["Biotechnology","Food Science","Civil Engineering","Computer Science","Biology","Chemistry","Agriculture"],
             program_type="Both", degree_level=["MS","PhD","Postdoc"],
             language_req=["IELTS","TOEFL"], ielts_min=6.0, toefl_min=80,
             fully_funded=True, hidden=False, hec_route=False, ielts_waiver=False, rtp=False,
             coverage="Tuition + ~€934/month + travel + health insurance",
             dm=10, dd=15, om=8, od=1,
             apply_link="https://www.daad.de/en/study-and-research-in-germany/scholarships/",
             portal="https://www.daad.de/en/",
             notes="One of the largest programs globally. Research & coursework available. Apply well before deadline."),
        dict(name="Heinrich Böll Foundation (Germany)", country="Germany", region="Europe", schengen=True,
             fields=["Biotechnology","Computer Science","Environmental Science","Civil Engineering"],
             program_type="Both", degree_level=["MS","PhD"],
             language_req=["IELTS","TOEFL","German B1+"], ielts_min=6.0, toefl_min=80,
             fully_funded=True, hidden=True, hec_route=False, ielts_waiver=False, rtp=False,
             coverage="€934/month (MS) · €1,200/month (PhD) + travel + health",
             dm=3, dd=1, om=1, od=15,
             apply_link="https://www.boell.de/en/the-foundation/scholarships",
             portal="https://www.boell.de/en/",
             notes="HIDDEN GEM. Two rounds per year: March & September. Very few Pakistanis apply."),
        dict(name="Erasmus Mundus Joint Masters", country="Multi-country EU", region="Europe", schengen=True,
             fields=["Biotechnology","Food Science","Computer Science","Civil Engineering","Environmental Science","Bioinformatics"],
             program_type="Coursework", degree_level=["MS"],
             language_req=["IELTS","TOEFL"], ielts_min=6.5, toefl_min=90,
             fully_funded=True, hidden=False, hec_route=False, ielts_waiver=False, rtp=False,
             coverage="€1,400/month + tuition + travel + installation allowance",
             dm=1, dd=15, om=10, od=1,
             apply_link="https://www.eacea.ec.europa.eu/scholarships/erasmus-mundus-catalogue_en",
             portal="https://erasmus-plus.ec.europa.eu/",
             notes="Study in 2-3 EU countries. Highly prestigious. 100+ programmes. Check catalogue for Biotech/Food options."),
        dict(name="Swedish Institute Scholarships (SISGP)", country="Sweden", region="Europe", schengen=True,
             fields=["Biotechnology","Computer Science","Environmental Science","Food Science","Public Health"],
             program_type="Coursework", degree_level=["MS"],
             language_req=["IELTS","TOEFL","PTE"], ielts_min=6.5, toefl_min=90,
             fully_funded=True, hidden=False, hec_route=False, ielts_waiver=False, rtp=False,
             coverage="SEK 11,000/month + tuition + travel + insurance",
             dm=2, dd=10, om=11, od=1,
             apply_link="https://si.se/en/apply/scholarships/swedish-institute-scholarships-for-global-professionals/",
             portal="https://si.se/en/",
             notes="Leadership-focused. Strong for professionals with work experience. Active community engagement valued."),
        dict(name="Swiss Government Excellence Scholarships", country="Switzerland", region="Europe", schengen=True,
             fields=["Biotechnology","Food Science","Chemistry","Biology","Computer Science","Civil Engineering"],
             program_type="Research", degree_level=["PhD","Postdoc","Research"],
             language_req=["IELTS","TOEFL","No minimum stated"], ielts_min=0, toefl_min=0,
             fully_funded=True, hidden=True, hec_route=True, ielts_waiver=True, rtp=False,
             coverage="CHF 1,920/month + tuition + health insurance + housing supplement",
             dm=11, dd=15, om=9, od=1,
             apply_link="https://www.sbfi.admin.ch/sbfi/en/home/education/scholarships-and-grants/swiss-government-excellence-scholarships.html",
             portal="https://www.sbfi.admin.ch/sbfi/en/",
             notes="HIDDEN GEM. Via HEC Pakistan. No IELTS minimum. ETH Zurich & EPFL eligible. Very low competition from Pakistan."),
        dict(name="Eiffel Excellence Scholarship (France)", country="France", region="Europe", schengen=True,
             fields=["Biotechnology","Food Science","Civil Engineering","Computer Science","Economics"],
             program_type="Coursework", degree_level=["MS","PhD"],
             language_req=["IELTS","TOEFL"], ielts_min=6.5, toefl_min=90,
             fully_funded=True, hidden=True, hec_route=False, ielts_waiver=False, rtp=False,
             coverage="€1,181/month (MS) · €1,400/month (PhD) + airfare + cultural activities",
             dm=1, dd=8, om=10, od=1,
             apply_link="https://www.campusfrance.org/en/eiffel-excellence-scholarship-program",
             portal="https://www.campusfrance.org/en/",
             notes="HIDDEN. Nominated by French universities — contact target university first, they nominate you."),
        dict(name="Stipendium Hungaricum (Hungary)", country="Hungary", region="Europe", schengen=True,
             fields=["Biotechnology","Computer Science","Civil Engineering","Agriculture","Food Science","Medicine"],
             program_type="Both", degree_level=["BS","MS","PhD"],
             language_req=["IELTS","TOEFL","No minimum for some"], ielts_min=5.5, toefl_min=72,
             fully_funded=True, hidden=False, hec_route=True, ielts_waiver=False, rtp=False,
             coverage="Tuition + HUF 43,700/month (PhD) + dormitory + health insurance",
             dm=1, dd=15, om=11, od=1,
             apply_link="https://stipendiumhungaricum.hu/apply/",
             portal="https://stipendiumhungaricum.hu/",
             notes="Apply via HEC Pakistan. Low IELTS (5.5 minimum). Growing English programmes in Biotech & Food Science."),
        dict(name="Italian Government Scholarships (MAECI)", country="Italy", region="Europe", schengen=True,
             fields=["Biotechnology","Food Science","Civil Engineering","Agriculture","Design"],
             program_type="Both", degree_level=["MS","PhD","Research"],
             language_req=["IELTS","TOEFL","Italian (some)"], ielts_min=0, toefl_min=0,
             fully_funded=True, hidden=True, hec_route=False, ielts_waiver=True, rtp=False,
             coverage="€900/month + tuition waiver + health insurance",
             dm=6, dd=3, om=3, od=1,
             apply_link="https://studyinitaly.esteri.it/en/home",
             portal="https://studyinitaly.esteri.it/en/",
             notes="HIDDEN. Very few Pakistanis apply. English STEM programmes widely available. No IELTS minimum."),
        dict(name="Norwegian Government Quota Scholarship", country="Norway", region="Europe", schengen=True,
             fields=["Biotechnology","Environmental Science","Computer Science","Food Science","Civil Engineering"],
             program_type="Both", degree_level=["MS","PhD"],
             language_req=["IELTS","TOEFL"], ielts_min=6.0, toefl_min=80,
             fully_funded=True, hidden=True, hec_route=False, ielts_waiver=False, rtp=False,
             coverage="Full tuition + NOK ~16,000/month + housing allowance + travel",
             dm=12, dd=1, om=9, od=1,
             apply_link="https://www.hkdir.no/en/funding-for-international-students/quota-scheme",
             portal="https://www.hkdir.no/en/",
             notes="HIDDEN GEM. Very few Pakistanis know this. Apply directly to Norwegian universities. NMBU top for Food/Biotech."),
        dict(name="Holland Scholarship (Netherlands)", country="Netherlands", region="Europe", schengen=True,
             fields=["Biotechnology","Food Science","Agriculture","Computer Science","Civil Engineering"],
             program_type="Coursework", degree_level=["BS","MS"],
             language_req=["IELTS","TOEFL","Cambridge"], ielts_min=6.0, toefl_min=80,
             fully_funded=False, hidden=True, hec_route=False, ielts_waiver=False, rtp=False,
             coverage="€5,000 one-time grant (stackable with TU Delft/Wageningen departmental grants)",
             dm=2, dd=1, om=11, od=1,
             apply_link="https://www.studyinholland.nl/scholarships/holland-scholarship",
             portal="https://www.studyinholland.nl/",
             notes="Partial but stackable. Wageningen (world #1 Food Science) and TU Delft offer additional departmental funding."),
        # ── RTP-TYPE: EUROPE ──
        dict(name="UKRI Doctoral Training Partnerships (UK)", country="UK", region="Europe", schengen=False,
             fields=["Biotechnology","Bioinformatics","Computer Science","Food Science","Environmental Science","Civil Engineering"],
             program_type="Research", degree_level=["PhD"],
             language_req=["IELTS","TOEFL"], ielts_min=6.5, toefl_min=92,
             fully_funded=True, hidden=True, hec_route=False, ielts_waiver=False, rtp=True,
             coverage="Full tuition + £19,000+/year stipend (UKRI rate, annually indexed)",
             dm=1, dd=15, om=10, od=1,
             apply_link="https://www.ukri.org/what-we-do/developing-people-and-skills/find-studentships-and-fellowships/",
             portal="https://www.ukri.org/",
             notes="RTP-TYPE. Funded through UK Research Councils via universities. Apply to DTP/CDT programmes at target university. Covers all fees + stipend automatically upon admission."),
        dict(name="NWO PhD Positions (Netherlands)", country="Netherlands", region="Europe", schengen=True,
             fields=["Biotechnology","Bioinformatics","Food Science","Environmental Science","Computer Science"],
             program_type="Research", degree_level=["PhD"],
             language_req=["IELTS","TOEFL","No minimum for some"], ielts_min=6.0, toefl_min=80,
             fully_funded=True, hidden=True, hec_route=False, ielts_waiver=False, rtp=True,
             coverage="Full salary ~€2,770/month (employee contract, not stipend) + full tuition",
             dm=3, dd=31, om=1, od=1,
             apply_link="https://www.nwo.nl/en/calls",
             portal="https://www.nwo.nl/en/",
             notes="RTP-TYPE. PhD students in Netherlands are paid as EMPLOYEES — salary not stipend. Search 'PhD vacancy' on university job boards (Wageningen, TU Delft, Utrecht). Rolling openings."),
        dict(name="FWO PhD Fellowship (Belgium)", country="Belgium", region="Europe", schengen=True,
             fields=["Biotechnology","Bioinformatics","Food Science","Computer Science","Civil Engineering","Chemistry"],
             program_type="Research", degree_level=["PhD"],
             language_req=["IELTS","TOEFL","No minimum stated"], ielts_min=0, toefl_min=0,
             fully_funded=True, hidden=True, hec_route=False, ielts_waiver=True, rtp=True,
             coverage="Full tuition + €2,400+/month salary + social security + research budget",
             dm=2, dd=1, om=11, od=1,
             apply_link="https://www.fwo.be/en/fellowships-funding/phd-fellowships/",
             portal="https://www.fwo.be/en/",
             notes="RTP-TYPE. FWO (Flanders) funds PhD researchers at Belgian universities as employees. KU Leuven, Ghent University strong for Biotech. Supervisor contact essential first."),
        dict(name="Danish Industrial PhD Programme", country="Denmark", region="Europe", schengen=True,
             fields=["Biotechnology","Food Science","Computer Science","Civil Engineering","Environmental Science","Agriculture"],
             program_type="Research", degree_level=["PhD"],
             language_req=["IELTS","TOEFL","No minimum stated"], ielts_min=0, toefl_min=0,
             fully_funded=True, hidden=True, hec_route=False, ielts_waiver=True, rtp=True,
             coverage="Full tuition + DKK ~30,000/month salary + research budget",
             dm=3, dd=15, om=12, od=1,
             apply_link="https://www.innovationsfonden.dk/en/programmes/industrial-phd",
             portal="https://www.innovationsfonden.dk/en/",
             notes="RTP-TYPE. HIDDEN. Industry-academia joint PhD. DTU (Technical University of Denmark) world-class for Food/Biotech. Paid as employee. Very few Pakistanis apply here."),
        dict(name="IRC Government of Ireland Postgraduate Scholarship", country="Ireland", region="Europe", schengen=False,
             fields=["Biotechnology","Food Science","Computer Science","Bioinformatics","Agriculture","Environmental Science"],
             program_type="Research", degree_level=["MS","PhD"],
             language_req=["IELTS","TOEFL","No minimum stated"], ielts_min=0, toefl_min=0,
             fully_funded=True, hidden=True, hec_route=False, ielts_waiver=True, rtp=True,
             coverage="Full tuition + €18,500/year stipend + €2,500 research expenses",
             dm=11, dd=15, om=9, od=1,
             apply_link="https://research.ie/funding/goipg/",
             portal="https://research.ie/",
             notes="RTP-TYPE. HIDDEN GEM. Ireland's national research council funds postgrads. UCD, Trinity College, UCC strong for Food & Biotech. Very low competition from Pakistan."),
        dict(name="OeAD Scholarships (Austria)", country="Austria", region="Europe", schengen=True,
             fields=["Biotechnology","Food Science","Computer Science","Civil Engineering","Environmental Science","Chemistry"],
             program_type="Research", degree_level=["MS","PhD","Postdoc"],
             language_req=["IELTS","TOEFL","German (some programmes)"], ielts_min=0, toefl_min=0,
             fully_funded=True, hidden=True, hec_route=False, ielts_waiver=True, rtp=False,
             coverage="€1,200–1,350/month + tuition waiver (many programmes) + health insurance",
             dm=3, dd=1, om=12, od=1,
             apply_link="https://oead.at/en/to-austria/grants-and-scholarships/",
             portal="https://oead.at/en/",
             notes="HIDDEN. Austrian government scholarship. BOKU Vienna (world-class Food & Agriculture), TU Vienna, Uni Vienna. No IELTS minimum. Very undersubscribed from Pakistan."),
        dict(name="Finnish EDUFI Fellowship", country="Finland", region="Europe", schengen=True,
             fields=["Biotechnology","Computer Science","Food Science","Environmental Science","Civil Engineering"],
             program_type="Research", degree_level=["PhD","Postdoc"],
             language_req=["IELTS","TOEFL","No requirement for some"], ielts_min=0, toefl_min=0,
             fully_funded=True, hidden=True, hec_route=False, ielts_waiver=True, rtp=True,
             coverage="€1,500/month + tuition waiver (some programmes)",
             dm=1, dd=31, om=11, od=1,
             apply_link="https://www.oph.fi/en/services/scholarships-and-grants",
             portal="https://www.oph.fi/en/",
             notes="RTP-TYPE. HIDDEN. Doctoral/postdoc research only. Aalto, Helsinki, Tampere universities. No IELTS minimum. Very undersubscribed from Pakistan."),
        # ── UK ──
        dict(name="Commonwealth Scholarships (UK)", country="UK", region="Europe", schengen=False,
             fields=["Biotechnology","Food Science","Computer Science","Civil Engineering","Public Health","Agriculture"],
             program_type="Both", degree_level=["MS","PhD"],
             language_req=["IELTS","TOEFL","No minimum for some"], ielts_min=6.0, toefl_min=79,
             fully_funded=True, hidden=False, hec_route=True, ielts_waiver=False, rtp=False,
             coverage="Full tuition + £1,347+/month + airfare + thesis grant",
             dm=10, dd=23, om=8, od=1,
             apply_link="https://cscuk.fcdo.gov.uk/apply/",
             portal="https://cscuk.fcdo.gov.uk/",
             notes="Apply via HEC Pakistan. Very competitive. Strong development-impact narrative required in SOP."),
        dict(name="Chevening Scholarships (UK)", country="UK", region="Europe", schengen=False,
             fields=["Biotechnology","Food Science","Computer Science","Civil Engineering","Public Policy"],
             program_type="Coursework", degree_level=["MS"],
             language_req=["IELTS","TOEFL","PTE"], ielts_min=6.5, toefl_min=88,
             fully_funded=True, hidden=False, hec_route=False, ielts_waiver=False, rtp=False,
             coverage="Full tuition + £1,347/month + travel + visa + arrival allowance",
             dm=11, dd=5, om=8, od=6,
             apply_link="https://www.chevening.org/apply/",
             portal="https://www.chevening.org/",
             notes="Leadership-focused. 2-5 years work experience required. Choose 3 universities. Highly competitive from Pakistan."),
        dict(name="Edinburgh Global Research Scholarships", country="UK", region="Europe", schengen=False,
             fields=["Biotechnology","Food Science","Computer Science","Bioinformatics","Civil Engineering"],
             program_type="Research", degree_level=["PhD"],
             language_req=["IELTS","TOEFL","PTE"], ielts_min=6.5, toefl_min=92,
             fully_funded=True, hidden=True, hec_route=False, ielts_waiver=False, rtp=False,
             coverage="Full tuition + £15,609/year stipend",
             dm=1, dd=24, om=10, od=1,
             apply_link="https://www.ed.ac.uk/student-funding/postgraduate/international/global/research",
             portal="https://www.ed.ac.uk/",
             notes="HIDDEN. University of Edinburgh. Strong life sciences. Very few Pakistanis apply here."),
        # ══ MIDDLE EAST ══
        dict(name="KAUST Fellowship (Saudi Arabia)", country="Saudi Arabia", region="Middle East", schengen=False,
             fields=["Biotechnology","Food Science","Computer Science","Bioinformatics","Environmental Science"],
             program_type="Research", degree_level=["MS","PhD"],
             language_req=["IELTS","TOEFL"], ielts_min=6.5, toefl_min=92,
             fully_funded=True, hidden=False, hec_route=False, ielts_waiver=False, rtp=True,
             coverage="Full tuition + USD $20,000+/year stipend + housing + medical + relocation",
             dm=1, dd=15, om=9, od=1,
             apply_link="https://admissions.kaust.edu.sa/",
             portal="https://www.kaust.edu.sa/en/",
             notes="RTP-TYPE. One of the most generous packages globally. World-class research. Biotech/CS departments top-ranked."),
        dict(name="Khalifa University Scholarships (UAE)", country="UAE", region="Middle East", schengen=False,
             fields=["Biotechnology","Computer Science","Civil Engineering","Bioinformatics","AI","Energy"],
             program_type="Both", degree_level=["MS","PhD"],
             language_req=["IELTS","TOEFL"], ielts_min=6.0, toefl_min=79,
             fully_funded=True, hidden=False, hec_route=False, ielts_waiver=False, rtp=False,
             coverage="Full tuition + AED 4,800–8,000/month + housing",
             dm=2, dd=28, om=11, od=1,
             apply_link="https://www.ku.ac.ae/graduate-admissions",
             portal="https://www.ku.ac.ae/",
             notes="QS Top 200. Strong STEM research. Pakistanis well represented. MS Molecular Life Sciences available."),
        dict(name="IsDB Merit Scholarship (Islamic Development Bank)", country="Multi-country OIC", region="Middle East", schengen=False,
             fields=["Biotechnology","Food Science","Computer Science","Civil Engineering","Agriculture","Medicine","Public Health"],
             program_type="Both", degree_level=["MS","PhD"],
             language_req=["IELTS","TOEFL","No minimum stated"], ielts_min=0, toefl_min=0,
             fully_funded=True, hidden=False, hec_route=False, ielts_waiver=True, rtp=False,
             coverage="Full tuition + living allowance + travel + health insurance",
             dm=3, dd=31, om=1, od=15,
             apply_link="https://www.isdb.org/what-we-do/human-capital-development/scholarship-programmes",
             portal="https://www.isdb.org/",
             notes="For OIC member countries including Pakistan. No strict IELTS minimum. Rolling deadlines in some programmes."),
        dict(name="HBKU Graduate Scholarships (Qatar)", country="Qatar", region="Middle East", schengen=False,
             fields=["Biotechnology","Computer Science","Bioinformatics","Public Health","Food Science","Environmental Science"],
             program_type="Research", degree_level=["MS","PhD"],
             language_req=["IELTS","TOEFL"], ielts_min=6.0, toefl_min=79,
             fully_funded=True, hidden=True, hec_route=False, ielts_waiver=False, rtp=True,
             coverage="Full tuition + QAR 14,000–16,000/month + housing + health + research budget",
             dm=2, dd=1, om=10, od=1,
             apply_link="https://www.hbku.edu.qa/en/admissions",
             portal="https://www.hbku.edu.qa/en/",
             notes="RTP-TYPE. HIDDEN GEM. Qatar Foundation funded. Biomedical Research + CS tracks strong. Very generous package."),
        dict(name="KAU Scholarship (King Abdulaziz University)", country="Saudi Arabia", region="Middle East", schengen=False,
             fields=["Biotechnology","Food Science","Computer Science","Civil Engineering","Medicine","Agriculture"],
             program_type="Both", degree_level=["MS","PhD"],
             language_req=["IELTS","TOEFL","No requirement for Arabic track"], ielts_min=0, toefl_min=0,
             fully_funded=True, hidden=False, hec_route=False, ielts_waiver=True, rtp=False,
             coverage="Full tuition + SAR 2,000/month + accommodation + health",
             dm=6, dd=30, om=3, od=1,
             apply_link="https://graduateadmissions.kau.edu.sa/",
             portal="https://www.kau.edu.sa/home_english.aspx",
             notes="Rolling admissions. No IELTS for many programmes. Direct application. Friendly to Pakistani students."),
        # ══ AUSTRALIA / NZ (RTP FOCUS) ══
        dict(name="Australia RTP — ANU Research Scholarship", country="Australia", region="Australia/NZ", schengen=False,
             fields=["Biotechnology","Bioinformatics","Computer Science","Environmental Science","Food Science","Civil Engineering"],
             program_type="Research", degree_level=["MS","PhD"],
             language_req=["IELTS","TOEFL","PTE"], ielts_min=6.5, toefl_min=80,
             fully_funded=True, hidden=False, hec_route=False, ielts_waiver=False, rtp=True,
             coverage="Full tuition + AUD $32,192/year stipend (RTP rate) + relocation + health OSHC",
             dm=10, dd=31, om=7, od=1,
             apply_link="https://www.anu.edu.au/study/scholarships/find-a-scholarship/anu-research-scholarship",
             portal="https://www.anu.edu.au/",
             notes="RTP-TYPE. Australian National University. Top-20 globally. Biotech & Bioinformatics strong. Stipend auto-considered with admission. Contact supervisor FIRST."),
        dict(name="Australia RTP — University of Melbourne", country="Australia", region="Australia/NZ", schengen=False,
             fields=["Biotechnology","Bioinformatics","Food Science","Computer Science","Civil Engineering","Agriculture"],
             program_type="Research", degree_level=["MS","PhD"],
             language_req=["IELTS","TOEFL","PTE"], ielts_min=6.5, toefl_min=79,
             fully_funded=True, hidden=False, hec_route=False, ielts_waiver=False, rtp=True,
             coverage="Full tuition + AUD $32,192/year stipend + health cover OSHC",
             dm=10, dd=15, om=7, od=1,
             apply_link="https://scholarships.unimelb.edu.au/awards/graduate-research-scholarships",
             portal="https://www.unimelb.edu.au/",
             notes="RTP-TYPE. World Top-15. Graduate Research Scholarships automatically offered on admission merit. Biomedical & Food Science excellent."),
        dict(name="Australia RTP — University of Queensland", country="Australia", region="Australia/NZ", schengen=False,
             fields=["Biotechnology","Food Science","Agriculture","Bioinformatics","Environmental Science","Computer Science"],
             program_type="Research", degree_level=["PhD"],
             language_req=["IELTS","TOEFL","PTE"], ielts_min=6.5, toefl_min=87,
             fully_funded=True, hidden=False, hec_route=False, ielts_waiver=False, rtp=True,
             coverage="Full tuition + AUD $32,192/year stipend + OSHC health cover",
             dm=9, dd=30, om=6, od=1,
             apply_link="https://graduate-school.uq.edu.au/scholarships",
             portal="https://www.uq.edu.au/",
             notes="RTP-TYPE. UQ globally ranked for Agriculture & Food Science. RTP stipend auto-awarded on merit. Secure supervisor email FIRST — it dramatically increases chances."),
        dict(name="Deakin University RTP Scholarship", country="Australia", region="Australia/NZ", schengen=False,
             fields=["Biotechnology","Food Science","Computer Science","Bioinformatics","Environmental Science"],
             program_type="Research", degree_level=["PhD"],
             language_req=["IELTS","TOEFL","PTE"], ielts_min=6.5, toefl_min=79,
             fully_funded=True, hidden=True, hec_route=False, ielts_waiver=False, rtp=True,
             coverage="Full tuition + AUD $28,597/year stipend (indexed annually)",
             dm=10, dd=31, om=8, od=1,
             apply_link="https://www.deakin.edu.au/research/research-candidature/research-scholarships",
             portal="https://www.deakin.edu.au/",
             notes="RTP-TYPE. HIDDEN. Contact Food & Biotech professors at Deakin first. Scholarship auto-considered with PhD admission."),
        dict(name="Australia Awards Scholarships", country="Australia", region="Australia/NZ", schengen=False,
             fields=["Biotechnology","Food Science","Agriculture","Computer Science","Civil Engineering","Public Health","Environmental Science"],
             program_type="Coursework", degree_level=["MS"],
             language_req=["IELTS","TOEFL","PTE"], ielts_min=6.5, toefl_min=87,
             fully_funded=True, hidden=False, hec_route=False, ielts_waiver=False, rtp=False,
             coverage="Full tuition + AUD $33,000/year living allowance + travel + health",
             dm=4, dd=30, om=2, od=1,
             apply_link="https://www.dfat.gov.au/people-to-people/australia-awards/australia-awards-scholarships",
             portal="https://www.dfat.gov.au/",
             notes="Priority countries include Pakistan. Development-impact focus required in SOP. Very generous package."),
        dict(name="New Zealand NZIDRS Scholarship", country="New Zealand", region="Australia/NZ", schengen=False,
             fields=["Biotechnology","Food Science","Agriculture","Computer Science","Environmental Science","Civil Engineering"],
             program_type="Research", degree_level=["MS","PhD"],
             language_req=["IELTS","TOEFL","PTE"], ielts_min=6.5, toefl_min=90,
             fully_funded=True, hidden=False, hec_route=False, ielts_waiver=False, rtp=True,
             coverage="Full tuition + NZD $25,000/year + airfare + health",
             dm=7, dd=28, om=4, od=1,
             apply_link="https://www.education.govt.nz/our-work/scholarships/new-zealand-international-doctoral-research-scholarships/",
             portal="https://www.education.govt.nz/",
             notes="RTP-TYPE. Excellent for Food Science at Massey University. Low applicant pool from Pakistan."),
        # ══ NORTH AMERICA ══
        dict(name="Vanier Canada Graduate Scholarships", country="Canada", region="North America", schengen=False,
             fields=["Biotechnology","Food Science","Computer Science","Civil Engineering","Bioinformatics","Public Health"],
             program_type="Research", degree_level=["PhD"],
             language_req=["IELTS","TOEFL","No minimum stated"], ielts_min=0, toefl_min=0,
             fully_funded=True, hidden=False, hec_route=False, ielts_waiver=True, rtp=False,
             coverage="CAD $50,000/year for 3 years",
             dm=11, dd=1, om=8, od=1,
             apply_link="https://vanier.gc.ca/en/home-accueil.html",
             portal="https://vanier.gc.ca/en/",
             notes="Nominated by Canadian university. Secure supervisor first. One of Canada's most prestigious awards."),
        dict(name="University of Guelph Graduate Scholarships (Canada)", country="Canada", region="North America", schengen=False,
             fields=["Food Science","Agriculture","Biotechnology","Bioinformatics","Environmental Science"],
             program_type="Research", degree_level=["MS","PhD"],
             language_req=["IELTS","TOEFL"], ielts_min=6.5, toefl_min=89,
             fully_funded=True, hidden=True, hec_route=False, ielts_waiver=False, rtp=True,
             coverage="Full tuition + CAD $18,000–30,000/year (supervisor-funded)",
             dm=2, dd=15, om=11, od=1,
             apply_link="https://www.uoguelph.ca/graduatestudies/future/scholarships",
             portal="https://www.uoguelph.ca/",
             notes="RTP-TYPE. HIDDEN. World's top Food Science university. Secure supervisor first — email faculty directly. Rolling intake."),
        dict(name="Fulbright Foreign Student Program (USA)", country="USA", region="North America", schengen=False,
             fields=["Biotechnology","Food Science","Computer Science","Civil Engineering","Agriculture","Public Health","Bioinformatics"],
             program_type="Both", degree_level=["MS","PhD","Research"],
             language_req=["IELTS","TOEFL"], ielts_min=6.5, toefl_min=90,
             fully_funded=True, hidden=False, hec_route=False, ielts_waiver=False, rtp=False,
             coverage="Full tuition + monthly stipend + health + travel + J-1 visa",
             dm=10, dd=15, om=7, od=1,
             apply_link="https://www.usefp.org/fulbright-foreign-student-program/",
             portal="https://www.usefp.org/",
             notes="Apply via USEFP Pakistan. Extremely prestigious. ~200 awards/year for Pakistan from 11,000+ applicants. Exceptional GPA + leadership required."),
        # ══ ASIA ══
        dict(name="Chinese Government Scholarship (CSC)", country="China", region="Asia", schengen=False,
             fields=["Biotechnology","Food Science","Computer Science","Civil Engineering","Agriculture","Bioinformatics","Medicine"],
             program_type="Both", degree_level=["BS","MS","PhD"],
             language_req=["IELTS","TOEFL","No requirement for many"], ielts_min=0, toefl_min=0,
             fully_funded=True, hidden=False, hec_route=True, ielts_waiver=True, rtp=False,
             coverage="Full tuition + CNY 2,000–3,500/month + accommodation + comprehensive medical",
             dm=3, dd=31, om=12, od=1,
             apply_link="https://www.campuschina.org/",
             portal="https://www.campuschina.org/",
             notes="Apply via HEC or direct to universities. Many English-taught STEM programmes. Very accessible for Pakistanis."),
        dict(name="Korean Government Scholarship (KGSP)", country="South Korea", region="Asia", schengen=False,
             fields=["Biotechnology","Computer Science","Civil Engineering","Food Science","Agriculture","Engineering"],
             program_type="Both", degree_level=["MS","PhD"],
             language_req=["IELTS","TOEFL","Korean (after enrollment)"], ielts_min=5.5, toefl_min=72,
             fully_funded=True, hidden=False, hec_route=False, ielts_waiver=False, rtp=False,
             coverage="Full tuition + KRW 900,000/month + settlement + language training + airfare",
             dm=3, dd=1, om=12, od=1,
             apply_link="https://www.studyinkorea.go.kr/en/sub/gks/allnew_gks_s.do",
             portal="https://www.studyinkorea.go.kr/en/",
             notes="Embassy or University track. KAIST, POSTECH, SNU are top choices. Korean language training included."),
        dict(name="BK21 Research Fellowship (South Korea)", country="South Korea", region="Asia", schengen=False,
             fields=["Biotechnology","Bioinformatics","Computer Science","Food Science","Civil Engineering","Chemistry"],
             program_type="Research", degree_level=["MS","PhD"],
             language_req=["IELTS","TOEFL","No minimum stated"], ielts_min=0, toefl_min=0,
             fully_funded=True, hidden=True, hec_route=False, ielts_waiver=True, rtp=True,
             coverage="Full tuition + KRW 600,000–1,300,000/month stipend + research expenses",
             dm=3, dd=1, om=12, od=1,
             apply_link="https://www.bk21.nrf.re.kr/eng/",
             portal="https://www.bk21.nrf.re.kr/eng/",
             notes="RTP-TYPE. HIDDEN. Korea's flagship research training program. Awarded through supervisors at KAIST, SNU, POSTECH. Contact professor directly — they assign BK21 funding automatically."),
        dict(name="Japanese MEXT Scholarship", country="Japan", region="Asia", schengen=False,
             fields=["Biotechnology","Food Science","Computer Science","Civil Engineering","Agriculture","Bioinformatics"],
             program_type="Research", degree_level=["MS","PhD","Research"],
             language_req=["IELTS","TOEFL","No requirement for many"], ielts_min=0, toefl_min=0,
             fully_funded=True, hidden=False, hec_route=False, ielts_waiver=True, rtp=False,
             coverage="Full tuition + JPY 145,000/month + airfare + research expenses",
             dm=6, dd=1, om=3, od=1,
             apply_link="https://www.mext.go.jp/en/policy/education/highered/title02/detail02/sdetail02/1373897.htm",
             portal="https://www.mext.go.jp/en/",
             notes="Embassy track OR university recommendation. Secure professor letter FIRST for university track. No IELTS."),
        dict(name="Taiwan ICDF Scholarship", country="Taiwan", region="Asia", schengen=False,
             fields=["Biotechnology","Food Science","Agriculture","Computer Science","Civil Engineering","Environmental Science"],
             program_type="Both", degree_level=["MS","PhD"],
             language_req=["IELTS","TOEFL","No requirement for English programs"], ielts_min=0, toefl_min=0,
             fully_funded=True, hidden=True, hec_route=False, ielts_waiver=True, rtp=False,
             coverage="Full tuition + USD $670/month + housing + insurance",
             dm=3, dd=31, om=1, od=1,
             apply_link="https://www.icdf.org.tw/wSite/ct?xItem=12505&ctNode=31&mp=2",
             portal="https://www.icdf.org.tw/",
             notes="HIDDEN. Severely undersubscribed from Pakistan. English programmes at NTU, NTHU. No IELTS needed."),
        dict(name="NUS Research Scholarship (Singapore)", country="Singapore", region="Asia", schengen=False,
             fields=["Biotechnology","Computer Science","Bioinformatics","Food Science","Civil Engineering","Data Science"],
             program_type="Research", degree_level=["PhD"],
             language_req=["IELTS","TOEFL"], ielts_min=6.0, toefl_min=85,
             fully_funded=True, hidden=False, hec_route=False, ielts_waiver=False, rtp=True,
             coverage="Full tuition + SGD $2,000–2,500/month stipend",
             dm=12, dd=31, om=9, od=1,
             apply_link="https://www.nus.edu.sg/admissions/graduate/research",
             portal="https://www.nus.edu.sg/",
             notes="RTP-TYPE. Top-20 globally. Supervisor contact essential before applying. Strong Biotech and CS departments."),
        # ══ PAKISTAN ══
        dict(name="HEC Indigenous PhD Scholarship", country="Pakistan", region="Pakistan", schengen=False,
             fields=["Biotechnology","Food Science","Computer Science","Civil Engineering","Agriculture","Bioinformatics"],
             program_type="Research", degree_level=["PhD"],
             language_req=["No Requirement"], ielts_min=0, toefl_min=0,
             fully_funded=True, hidden=False, hec_route=True, ielts_waiver=True, rtp=False,
             coverage="Full tuition (Pakistani university) + PKR stipend + research grant",
             dm=6, dd=30, om=4, od=1,
             apply_link="https://www.hec.gov.pk/english/scholarships/Pages/Ph.D-Indigenous.aspx",
             portal="https://www.hec.gov.pk/",
             notes="Domestic PhD funding. Good stepping stone before applying abroad. No IELTS needed. Periodic batches."),
        dict(name="HEC Overseas Scholarship (Phase-III)", country="Pakistan → Abroad", region="Pakistan", schengen=False,
             fields=["Biotechnology","Food Science","Computer Science","Civil Engineering","Agriculture","Bioinformatics","Medicine"],
             program_type="Research", degree_level=["PhD"],
             language_req=["IELTS","TOEFL"], ielts_min=6.0, toefl_min=79,
             fully_funded=True, hidden=False, hec_route=True, ielts_waiver=False, rtp=False,
             coverage="Full tuition abroad + monthly stipend (country-based) + health + travel",
             dm=9, dd=30, om=7, od=1,
             apply_link="https://www.hec.gov.pk/english/scholarships/Pages/Overseas-Scholarship.aspx",
             portal="https://www.hec.gov.pk/",
             notes="Sends you abroad for PhD. Must secure admission at foreign university first. Check HEC for current batch."),
        dict(name="PEEF Undergraduate Scholarship (Punjab)", country="Pakistan", region="Pakistan", schengen=False,
             fields=["Biotechnology","Food Science","Computer Science","Civil Engineering","Agriculture","Medicine"],
             program_type="Coursework", degree_level=["BS"],
             language_req=["No Requirement"], ielts_min=0, toefl_min=0,
             fully_funded=True, hidden=False, hec_route=False, ielts_waiver=True, rtp=False,
             coverage="Full tuition + PKR monthly stipend (merit + need based)",
             dm=9, dd=30, om=7, od=1,
             apply_link="https://www.peef.org.pk/",
             portal="https://www.peef.org.pk/",
             notes="Punjab Educational Endowment Fund. For needy students in Punjab universities including UVAS. No IELTS required."),
    ]

    records = []
    for t in T:
        r = dict(t)
        dl, op, sess = project(t["dm"], t["dd"], t["om"], t["od"])
        r["deadline"] = dl
        r["opening_date"] = op
        r["session"] = sess
        records.append(r)
    return pd.DataFrame(records)

def days_left(s):
    try:
        return (datetime.strptime(s.split(" ")[0], "%Y-%m-%d").date() - date.today()).days
    except:
        return 9999

def deadline_badge(s):
    d = days_left(s)
    if d == 9999: return "<span class='deadline-roll'>📅 Rolling</span>"
    if d < 0:     return "<span class='deadline-urgent'>⛔ Closed — next cycle coming</span>"
    if d <= 30:   return f"<span class='deadline-urgent'>🔥 {d} days — URGENT</span>"
    if d <= 90:   return f"<span class='deadline-warn'>⚠️ {d} days left</span>"
    return f"<span class='deadline-ok'>✅ {d} days left</span>"

def render_card(r):
    cls = "hidden-gem" if r["hidden"] else ("rtp-type" if r["rtp"] else "")
    hb  = "<span class='badge b-hidden'>🕵️ HIDDEN GEM</span>" if r["hidden"] else ""
    rb  = "<span class='badge b-rtp'>🎯 RTP-TYPE</span>" if r["rtp"] else ""
    fb  = "<span class='badge b-funded'>✅ Fully Funded</span>" if r["fully_funded"] else "<span class='badge b-partial'>⚡ Partial</span>"
    hec = "<span class='badge b-hec'>🏛️ Via HEC</span>" if r["hec_route"] else ""
    sch = "<span class='badge b-schengen'>🇪🇺 Schengen</span>" if r.get("schengen") else ""
    wv  = "<span class='badge b-waiver'>📋 IELTS Waivable</span>" if r["ielts_waiver"] else ""
    fds = "".join([f"<span class='badge b-field'>{f}</span>" for f in r["fields"][:5]])
    dgs = "".join([f"<span class='badge b-degree'>{d}</span>" for d in r["degree_level"]])
    lgs = "".join([f"<span class='badge b-lang'>{l}</span>" for l in r["language_req"][:3]])
    ie  = str(r["ielts_min"]) if r["ielts_min"] > 0 else "Not required"
    tf  = str(r.get("toefl_min",0)) if r.get("toefl_min",0) > 0 else "Not required"
    return f"""
<div class='sch-card {cls}'>
  <div class='sch-meta'>
    <div>
      <h3>{r['name']} {hb} {rb}</h3>
      <span class='badge b-region'>🌍 {r['country']} · {r['region']}</span>
      {fb} {hec} {sch} {wv}
    </div>
    <div style='text-align:right;min-width:175px'>
      {deadline_badge(r['deadline'])}<br>
      <span style='color:rgba(255,255,255,0.45);font-size:0.81em'>🗓️ Opens: {r['opening_date']}</span><br>
      <span style='color:#63b3ed;font-size:0.81em;font-weight:600'>📆 {r['session']}</span>
    </div>
  </div>
  <hr class='divider'>
  <div style='margin:4px 0'><b style='color:rgba(255,255,255,0.45);font-size:0.78em'>FIELDS</b><br>{fds}</div>
  <div style='margin:5px 0'><b style='color:rgba(255,255,255,0.45);font-size:0.78em'>DEGREE · TYPE</b><br>{dgs} <span class='badge b-degree'>{r['program_type']}</span></div>
  <div style='margin:5px 0'><b style='color:rgba(255,255,255,0.45);font-size:0.78em'>LANGUAGE</b><br>{lgs}
    <span style='color:rgba(255,255,255,0.38);font-size:0.79em'>&nbsp; Min IELTS: <b style='color:#fbbf24'>{ie}</b> &nbsp;|&nbsp; Min TOEFL: <b style='color:#fbbf24'>{tf}</b></span>
  </div>
  <div class='coverage-box'>💰 {r['coverage']}</div>
  <div class='insight-box'>💡 {r['notes']}</div>
  <div>
    <a class='link-apply' href='{r['apply_link']}' target='_blank'>🔗 Apply Now</a>
    <a class='link-portal' href='{r['portal']}' target='_blank'>🏛️ Official Portal</a>
  </div>
</div>"""

# ══ LOAD ══
df_all = build_database()

# ══ AUTHOR STRIP ══
st.markdown("""
<div class='author-strip'>
  <div>
    <div class='author-name'>👨‍🔬 Hassan Iqbal</div>
    <div class='author-detail'>Biotechnologist · UVAS Lahore · Batch 2022–2026</div>
  </div>
  <div style='display:flex;gap:8px;flex-wrap:wrap;align-items:center'>
    <span class='author-badge'>🎓 Creator & Curator</span>
    <span class='author-badge'>🇵🇰 Built for Pakistani Students</span>
    <span class='author-badge'>🔬 University of Veterinary & Animal Sciences</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ══ HERO ══
st.markdown(f"""
<div class='hero'>
  <h1>🎓 ScholarshipHunter Pro</h1>
  <p>Fully Funded International Scholarships · MS · MPhil · PhD · RTP-Type Research Awards</p>
  <div class='badges'>
    <span class='hbadge'>🌍 {len(df_all)} Scholarships</span>
    <span class='hbadge'>🎯 RTP-Type Included</span>
    <span class='hbadge'>📅 Auto-Updated Deadlines</span>
    <span class='hbadge'>🕵️ Hidden Gems</span>
    <span class='hbadge'>📋 IELTS Waiver Options</span>
    <span class='hbadge'>🏛️ HEC Route Options</span>
    <span class='hbadge'>🔍 Live Search</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ══ SIDEBAR ══
with st.sidebar:
    st.markdown("### 🔍 Filter Scholarships")
    st.markdown("---")
    region_opts = ["All Regions"] + sorted(df_all["region"].unique().tolist())
    sel_region = st.multiselect("🌍 Region", region_opts, default=["All Regions"])
    field_map = {
        "🌐 All Fields": None,
        "🔬 Biotechnology & Subfields": ["Biotechnology","Bioinformatics","Molecular Biology","Biochemistry","Microbiology"],
        "🍕 Food Science & Technology": ["Food Science","Agriculture","Food Technology"],
        "🏗️ Civil Engineering": ["Civil Engineering","Environmental Science","Structural Engineering"],
        "💻 Computer Science & AI": ["Computer Science","Data Science","AI","Bioinformatics"],
        "🌿 Agriculture & Environment": ["Agriculture","Environmental Science"],
        "🩺 Public Health & Medicine": ["Public Health","Medicine","Biology"],
    }
    sel_field = st.selectbox("🔬 Field", list(field_map.keys()))
    degree_opts = ["All","MS","MPhil","PhD","BS","Postdoc","Research"]
    sel_degree = st.multiselect("🎓 Degree Level", degree_opts, default=["All"])
    sel_type = st.selectbox("📚 Program Type", ["All","Coursework","Research","Both"])
    lang_opts = ["All","IELTS","TOEFL","PTE","No Requirement"]
    sel_lang = st.multiselect("🗣️ Language", lang_opts, default=["All"])
    sel_ielts = st.slider("Max IELTS Band", 0.0, 9.0, 9.0, 0.5)
    st.markdown("---")
    st.markdown("**⚙️ Quick Filters**")
    only_funded   = st.checkbox("✅ Fully Funded Only", value=True)
    only_rtp      = st.checkbox("🎯 RTP-Type Only", value=False)
    only_hidden   = st.checkbox("🕵️ Hidden Gems Only", value=False)
    only_hec      = st.checkbox("🏛️ Via HEC Route Only", value=False)
    only_waiver   = st.checkbox("📋 IELTS Waivable Only", value=False)
    only_schengen = st.checkbox("🇪🇺 Schengen Zone Only", value=False)
    st.markdown("---")
    deadline_months = st.slider("📅 Deadline within (months)", 1, 24, 24)
    sort_by = st.selectbox("🔢 Sort By", [
        "📅 Deadline — Soonest First","🌍 Country A–Z",
        "📊 IELTS — Lowest First","🕵️ Hidden Gems First","🎯 RTP-Type First"])
    st.markdown("---")
    st.markdown(
        "<div style='font-size:0.73em;color:rgba(255,255,255,0.3);text-align:center'>"
        "By Hassan Iqbal 🇵🇰<br>UVAS Lahore · Biotechnologist 2022–2026<br>"
        "Deadlines auto-project to future dates</div>", unsafe_allow_html=True)

# ══ APPLY FILTERS ══
df = df_all.copy()
if "All Regions" not in sel_region and sel_region:
    df = df[df["region"].isin(sel_region)]
if sel_field != "🌐 All Fields":
    tgts = field_map[sel_field]
    df = df[df["fields"].apply(lambda x: any(f in x for f in tgts))]
if "All" not in sel_degree and sel_degree:
    df = df[df["degree_level"].apply(lambda x: any(d in x for d in sel_degree))]
if sel_type != "All":
    df = df[df["program_type"].isin([sel_type,"Both"])]
if "All" not in sel_lang and sel_lang:
    if "No Requirement" in sel_lang:
        df = df[df["language_req"].apply(lambda x: any("No" in l for l in x))]
    else:
        df = df[df["language_req"].apply(lambda x: any(l in x for l in sel_lang))]
if sel_ielts < 9.0:
    df = df[(df["ielts_min"] <= sel_ielts)|(df["ielts_min"]==0)]
if only_funded:   df = df[df["fully_funded"]==True]
if only_rtp:      df = df[df["rtp"]==True]
if only_hidden:   df = df[df["hidden"]==True]
if only_hec:      df = df[df["hec_route"]==True]
if only_waiver:   df = df[df["ielts_waiver"]==True]
if only_schengen: df = df[df["schengen"]==True]
max_days = deadline_months * 30
df["_days"] = df["deadline"].apply(days_left)
df = df[(df["_days"]<=max_days)|(df["_days"]==9999)]
if "Deadline" in sort_by:   df = df.sort_values("_days")
elif "Country"  in sort_by: df = df.sort_values("country")
elif "IELTS"    in sort_by: df = df.sort_values("ielts_min")
elif "Hidden"   in sort_by: df = df.sort_values("hidden", ascending=False)
elif "RTP"      in sort_by: df = df.sort_values("rtp", ascending=False)

# ══ TABS ══
tab1, tab2, tab3 = st.tabs(["🔍 Search Results", "📅 Deadline Calendar", "📊 Statistics"])

with tab1:
    # ── SEARCH BAR ──
    st.markdown("<div class='search-wrap'><h4>🔍 Quick Search — Type any keyword: country, field, university name, or scholarship</h4>", unsafe_allow_html=True)
    search_q = st.text_input("", placeholder="e.g.  Australia   Biotechnology   RTP   DAAD   No IELTS   PhD   Hidden...", label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)

    if search_q.strip():
        q = search_q.strip().lower()
        mask = df.apply(lambda row: (
            q in row["name"].lower() or
            q in row["country"].lower() or
            q in row["region"].lower() or
            q in row["coverage"].lower() or
            q in row["notes"].lower() or
            q in row["program_type"].lower() or
            any(q in f.lower() for f in row["fields"]) or
            any(q in d.lower() for d in row["degree_level"]) or
            any(q in l.lower() for l in row["language_req"]) or
            (q in ["rtp","research training"] and row["rtp"]) or
            (q in ["hidden","gem","low competition"] and row["hidden"]) or
            (q in ["hec","pakistan route"] and row["hec_route"]) or
            (q in ["no ielts","ielts waiver","waiver"] and row["ielts_waiver"])
        ), axis=1)
        df = df[mask]

    n = len(df)
    hidden_c  = int(df["hidden"].sum())  if n else 0
    rtp_c     = int(df["rtp"].sum())     if n else 0
    funded_c  = int(df["fully_funded"].sum()) if n else 0
    hec_c     = int(df["hec_route"].sum()) if n else 0
    waiver_c  = int(df["ielts_waiver"].sum()) if n else 0
    region_c  = df["region"].nunique()   if n else 0

    st.markdown(f"""
    <div class='stat-row'>
      <div class='stat-card'><div class='stat-num'>{n}</div><div class='stat-label'>Found</div></div>
      <div class='stat-card'><div class='stat-num' style='color:#34d399'>{rtp_c}</div><div class='stat-label'>RTP-Type</div></div>
      <div class='stat-card'><div class='stat-num' style='color:#f97316'>{hidden_c}</div><div class='stat-label'>Hidden Gems</div></div>
      <div class='stat-card'><div class='stat-num' style='color:#6ee7b7'>{funded_c}</div><div class='stat-label'>Fully Funded</div></div>
      <div class='stat-card'><div class='stat-num' style='color:#a5b4fc'>{hec_c}</div><div class='stat-label'>Via HEC</div></div>
      <div class='stat-card'><div class='stat-num' style='color:#fbbf24'>{waiver_c}</div><div class='stat-label'>IELTS Waiver</div></div>
      <div class='stat-card'><div class='stat-num'>{region_c}</div><div class='stat-label'>Regions</div></div>
    </div>""", unsafe_allow_html=True)

    if n > 0:
        ca, cb, _ = st.columns([1,1,4])
        with ca:
            buf = io.StringIO()
            df.drop(columns=["_days","fields","degree_level","language_req"], errors="ignore").to_csv(buf, index=False)
            st.download_button("📥 Export CSV", buf.getvalue(), "scholarships.csv","text/csv")
        with cb:
            xb = io.BytesIO()
            df.drop(columns=["_days","fields","degree_level","language_req"], errors="ignore").to_excel(xb, index=False)
            st.download_button("📊 Export Excel", xb.getvalue(),"scholarships.xlsx",
                               "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    if n == 0:
        st.markdown("<div class='no-results'>⚠️ No results match. Try a different keyword or broaden your sidebar filters.</div>", unsafe_allow_html=True)
    else:
        for _, row in df.iterrows():
            st.markdown(render_card(row), unsafe_allow_html=True)

with tab2:
    st.markdown("<div class='section-head'>📅 Deadline Calendar — All Scholarships by Urgency</div>", unsafe_allow_html=True)
    cal = df_all.copy()
    cal["_days"] = cal["deadline"].apply(days_left)
    cal = cal.sort_values("_days")
    rows = ""
    for _, r in cal.iterrows():
        d = r["_days"]
        rc = "urgent" if 0<=d<=30 else ("warn" if d<=90 else ("ok" if d<=9998 else ""))
        dt = "Rolling" if d==9999 else ("Closed" if d<0 else (f"🔥 {d}d" if d<=30 else (f"⚠️ {d}d" if d<=90 else f"✅ {d}d")))
        hid = "🕵️" if r["hidden"] else ""
        rtp = "🎯" if r["rtp"] else ""
        rows += f"""<tr class='{rc}'>
          <td>{hid}{rtp} <b>{r['name']}</b></td>
          <td>{r['country']}</td><td>{r['deadline']}</td>
          <td><b>{dt}</b></td><td>{r['opening_date']}</td><td>{r['session']}</td>
          <td>{'✅' if r['ielts_waiver'] else '❌'}</td>
          <td><a class='link-apply' href='{r['apply_link']}' target='_blank' style='padding:4px 10px;font-size:0.76em'>Apply</a></td>
        </tr>"""
    st.markdown(f"""
    <div class='cal-wrap'><table class='cal'>
      <thead><tr><th>Scholarship</th><th>Country</th><th>Deadline</th>
      <th>Days Left</th><th>Opens</th><th>Session</th><th>IELTS Waiver</th><th>Link</th></tr></thead>
      <tbody>{rows}</tbody></table></div>
    <p style='color:rgba(255,255,255,0.3);font-size:0.77em;margin-top:6px'>
    🕵️ Hidden Gem &nbsp; 🎯 RTP-Type &nbsp; 🟠 &lt;30 days · 🟡 &lt;90 days · 🟢 Upcoming</p>
    """, unsafe_allow_html=True)

with tab3:
    st.markdown("<div class='section-head'>📊 Database Overview</div>", unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
    with c1:
        rc = df_all.groupby("region").size().reset_index(name="Count").sort_values("Count",ascending=False)
        st.markdown("**🌍 By Region**"); st.dataframe(rc, hide_index=True, use_container_width=True)
    with c2:
        st.markdown("**📊 Summary**")
        summary = pd.DataFrame({"Metric":[
            "Total Scholarships","RTP-Type","Fully Funded","Hidden Gems",
            "IELTS Waivable","Via HEC Route","No IELTS Min",
            "PhD Options","MS Options","Schengen Countries"],
            "Count":[
            len(df_all), int(df_all["rtp"].sum()), int(df_all["fully_funded"].sum()),
            int(df_all["hidden"].sum()), int(df_all["ielts_waiver"].sum()),
            int(df_all["hec_route"].sum()), int((df_all["ielts_min"]==0).sum()),
            int(df_all["degree_level"].apply(lambda x:"PhD" in x).sum()),
            int(df_all["degree_level"].apply(lambda x:"MS" in x).sum()),
            int(df_all["schengen"].sum())]})
        st.dataframe(summary, hide_index=True, use_container_width=True)
    with c3:
        fc = {}
        for _, row in df_all.iterrows():
            for f in row["fields"]: fc[f] = fc.get(f,0)+1
        top_f = sorted(fc.items(), key=lambda x:-x[1])[:12]
        st.markdown("**🔬 Top Fields**")
        st.dataframe(pd.DataFrame(top_f, columns=["Field","Programmes"]), hide_index=True, use_container_width=True)
    st.markdown("---")
    st.markdown(
        "<div style='text-align:center;color:rgba(255,255,255,0.25);font-size:0.78em;padding:8px'>"
        "ScholarshipHunter Pro · Curated by <b style='color:rgba(255,255,255,0.45)'>Hassan Iqbal</b> · "
        "Biotechnologist, UVAS Lahore 2022–2026 · Built for Pakistani Students 🇵🇰"
        "</div>", unsafe_allow_html=True)
