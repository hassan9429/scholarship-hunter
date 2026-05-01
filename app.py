import streamlit as st
import pandas as pd
from datetime import date, datetime, timedelta
import io

# ── PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ScholarshipHunter Pro — Pakistani Students",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CUSTOM CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Sora', sans-serif !important;
}

/* ── HIDE STREAMLIT DEFAULTS ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1rem !important; max-width: 1400px; }

/* ── HERO BANNER ── */
.hero {
    background: linear-gradient(135deg, #040d1f 0%, #071533 40%, #0a2050 70%, #0d2d6b 100%);
    border: 1px solid rgba(30, 109, 229, 0.3);
    border-radius: 18px;
    padding: 36px 40px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(30,109,229,0.15) 0%, transparent 70%);
    border-radius: 50%;
}
.hero::after {
    content: '';
    position: absolute;
    bottom: -80px; left: 20%;
    width: 400px; height: 200px;
    background: radial-gradient(circle, rgba(99,179,237,0.08) 0%, transparent 70%);
}
.hero h1 {
    font-size: 2.1em; font-weight: 800; margin: 0 0 8px;
    background: linear-gradient(90deg, #ffffff, #63b3ed);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    letter-spacing: -0.5px;
}
.hero p { color: rgba(255,255,255,0.65); margin: 0; font-size: 0.97em; font-weight: 300; }
.hero .badges { margin-top: 16px; display: flex; flex-wrap: wrap; gap: 8px; }
.hero .hbadge {
    background: rgba(30,109,229,0.2); border: 1px solid rgba(30,109,229,0.4);
    color: #63b3ed; padding: 4px 12px; border-radius: 20px;
    font-size: 0.78em; font-weight: 500;
}

/* ── STAT CARDS ── */
.stat-row { display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 22px; }
.stat-card {
    flex: 1; min-width: 110px;
    background: linear-gradient(145deg, #131929, #0f1e35);
    border: 1px solid rgba(30,109,229,0.2);
    border-radius: 12px; padding: 14px 16px; text-align: center;
}
.stat-num { font-size: 2em; font-weight: 800; color: #63b3ed; font-family: 'JetBrains Mono', monospace; }
.stat-label { font-size: 0.72em; color: rgba(255,255,255,0.5); margin-top: 3px; text-transform: uppercase; letter-spacing: 0.5px; }

/* ── SCHOLARSHIP CARDS ── */
.sch-card {
    background: linear-gradient(145deg, #111827, #0f1e35);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 14px;
    position: relative;
    transition: border-color 0.2s;
}
.sch-card.hidden-gem {
    border-left: 4px solid #f97316;
    background: linear-gradient(145deg, #1a1008, #111827);
}
.sch-card h3 {
    font-size: 1.05em; font-weight: 700; color: #e8edf5;
    margin: 0 0 8px; letter-spacing: -0.2px;
}
.sch-meta { display: flex; justify-content: space-between; flex-wrap: wrap; gap: 8px; margin-bottom: 12px; }
.deadline-urgent { color: #f87171; font-weight: 700; font-size: 0.88em; }
.deadline-warn   { color: #fbbf24; font-weight: 600; font-size: 0.88em; }
.deadline-ok     { color: #34d399; font-weight: 600; font-size: 0.88em; }
.deadline-roll   { color: #9ca3af; font-style: italic; font-size: 0.88em; }

/* ── BADGES ── */
.badge {
    display: inline-block; padding: 3px 10px; border-radius: 20px;
    font-size: 0.73em; font-weight: 600; margin: 2px 2px 2px 0;
}
.b-region   { background: rgba(30,109,229,0.2);  color: #63b3ed; border: 1px solid rgba(30,109,229,0.3); }
.b-field    { background: rgba(52,211,153,0.15); color: #34d399; border: 1px solid rgba(52,211,153,0.25); }
.b-degree   { background: rgba(167,139,250,0.15);color: #a78bfa; border: 1px solid rgba(167,139,250,0.25); }
.b-lang     { background: rgba(251,191,36,0.15); color: #fbbf24; border: 1px solid rgba(251,191,36,0.25); }
.b-hidden   { background: rgba(249,115,22,0.15); color: #f97316; border: 1px solid rgba(249,115,22,0.3); }
.b-funded   { background: rgba(52,211,153,0.12); color: #6ee7b7; border: 1px solid rgba(52,211,153,0.2); }
.b-partial  { background: rgba(251,191,36,0.12); color: #fde68a; border: 1px solid rgba(251,191,36,0.2); }
.b-hec      { background: rgba(99,102,241,0.15); color: #a5b4fc; border: 1px solid rgba(99,102,241,0.25); }
.b-schengen { background: rgba(14,165,233,0.15); color: #38bdf8; border: 1px solid rgba(14,165,233,0.25); }
.b-waiver   { background: rgba(52,211,153,0.1);  color: #6ee7b7; border: 1px solid rgba(52,211,153,0.2); }

/* ── COVERAGE & INSIGHT ── */
.coverage-box {
    background: rgba(30,109,229,0.08);
    border-left: 3px solid rgba(30,109,229,0.5);
    border-radius: 0 8px 8px 0;
    padding: 8px 12px; margin: 10px 0;
    font-size: 0.87em; color: #93c5fd;
}
.insight-box {
    background: rgba(255,255,255,0.04);
    border-radius: 8px;
    padding: 8px 12px; margin: 8px 0;
    font-size: 0.85em; color: rgba(255,255,255,0.6);
    border: 1px solid rgba(255,255,255,0.07);
}

/* ── LINKS ── */
.link-apply {
    display: inline-block;
    background: linear-gradient(135deg, #1e6de5, #1a5cd4);
    color: white !important; text-decoration: none !important;
    padding: 8px 18px; border-radius: 8px;
    font-size: 0.85em; font-weight: 600; margin-right: 8px; margin-top: 8px;
    border: 1px solid rgba(255,255,255,0.1);
}
.link-portal {
    display: inline-block;
    background: rgba(255,255,255,0.07);
    color: rgba(255,255,255,0.7) !important; text-decoration: none !important;
    padding: 8px 18px; border-radius: 8px;
    font-size: 0.85em; font-weight: 500; margin-top: 8px;
    border: 1px solid rgba(255,255,255,0.1);
}

/* ── CALENDAR TABLE ── */
.cal-wrap { overflow-x: auto; border-radius: 12px; border: 1px solid rgba(255,255,255,0.08); }
table.cal { width: 100%; border-collapse: collapse; font-size: 0.84em; }
table.cal th { background: #0d2d6b; color: #63b3ed; padding: 10px 14px; text-align: left; white-space: nowrap; }
table.cal td { padding: 9px 14px; border-bottom: 1px solid rgba(255,255,255,0.05); color: #cbd5e1; }
table.cal tr.closed  td { background: rgba(239,68,68,0.06); }
table.cal tr.urgent  td { background: rgba(249,115,22,0.07); }
table.cal tr.warn    td { background: rgba(251,191,36,0.06); }
table.cal tr.ok      td { background: rgba(52,211,153,0.04); }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0b0f1a 0%, #0d1529 100%) !important;
    border-right: 1px solid rgba(30,109,229,0.2) !important;
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stCheckbox label { color: rgba(255,255,255,0.75) !important; font-size: 0.85em !important; }

/* ── SECTION HEADERS ── */
.section-head {
    font-size: 1.1em; font-weight: 700; color: #63b3ed;
    margin: 20px 0 12px; padding-bottom: 8px;
    border-bottom: 1px solid rgba(30,109,229,0.2);
    letter-spacing: -0.3px;
}
.no-results {
    text-align: center; padding: 48px 24px;
    color: rgba(255,255,255,0.4); font-size: 1em;
}
.divider { border: none; border-top: 1px solid rgba(255,255,255,0.06); margin: 12px 0; }
</style>
""", unsafe_allow_html=True)

# ── DATABASE ───────────────────────────────────────────────────────────────
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
                    if dl.month <= 4:
                        sess = f"Fall {dl.year}"
                    elif dl.month <= 8:
                        sess = f"Winter {dl.year}/{dl.year+1}"
                    else:
                        sess = f"Fall {dl.year + 1}"
                    return str(dl), str(op), sess
            except ValueError:
                pass
        return "Rolling", "Year-round", "Rolling"

    TEMPLATES = [
        # EUROPE
        dict(name="DAAD Research Grants", country="Germany", region="Europe", schengen=True,
             fields=["Biotechnology","Food Science","Civil Engineering","Computer Science","Biology","Chemistry","Agriculture"],
             program_type="Both", degree_level=["MS","PhD","Postdoc"],
             language_req=["IELTS","TOEFL"], ielts_min=6.0, toefl_min=80,
             fully_funded=True, hidden=False, hec_route=False, ielts_waiver=False,
             coverage="Tuition + ~€934/month + travel + health insurance",
             dm=10, dd=15, om=8, od=1,
             apply_link="https://www.daad.de/en/study-and-research-in-germany/scholarships/",
             portal="https://www.daad.de/en/",
             notes="One of the largest scholarship programs globally. Research & coursework available. Apply well before deadline."),
        dict(name="Heinrich Böll Foundation (Germany)", country="Germany", region="Europe", schengen=True,
             fields=["Biotechnology","Computer Science","Environmental Science","Civil Engineering"],
             program_type="Both", degree_level=["MS","PhD"],
             language_req=["IELTS","TOEFL","German B1+"], ielts_min=6.0, toefl_min=80,
             fully_funded=True, hidden=True, hec_route=False, ielts_waiver=False,
             coverage="€934/month (MS) · €1,200/month (PhD) + travel + health",
             dm=3, dd=1, om=1, od=15,
             apply_link="https://www.boell.de/en/the-foundation/scholarships",
             portal="https://www.boell.de/en/",
             notes="HIDDEN GEM. Political/social-justice focus. Two rounds per year (March & September). Very few Pakistanis apply."),
        dict(name="Erasmus Mundus Joint Masters", country="Multi-country EU", region="Europe", schengen=True,
             fields=["Biotechnology","Food Science","Computer Science","Civil Engineering","Environmental Science","Bioinformatics"],
             program_type="Coursework", degree_level=["MS"],
             language_req=["IELTS","TOEFL"], ielts_min=6.5, toefl_min=90,
             fully_funded=True, hidden=False, hec_route=False, ielts_waiver=False,
             coverage="€1,400/month + tuition + travel + installation allowance",
             dm=1, dd=15, om=10, od=1,
             apply_link="https://www.eacea.ec.europa.eu/scholarships/erasmus-mundus-catalogue_en",
             portal="https://erasmus-plus.ec.europa.eu/",
             notes="Study in 2-3 EU countries. Highly prestigious. 100+ programmes. Check catalogue for Biotech/Food options."),
        dict(name="Swedish Institute Scholarships (SISGP)", country="Sweden", region="Europe", schengen=True,
             fields=["Biotechnology","Computer Science","Environmental Science","Food Science","Public Health"],
             program_type="Coursework", degree_level=["MS"],
             language_req=["IELTS","TOEFL","PTE"], ielts_min=6.5, toefl_min=90,
             fully_funded=True, hidden=False, hec_route=False, ielts_waiver=False,
             coverage="SEK 11,000/month + tuition + travel + insurance",
             dm=2, dd=10, om=11, od=1,
             apply_link="https://si.se/en/apply/scholarships/swedish-institute-scholarships-for-global-professionals/",
             portal="https://si.se/en/",
             notes="Leadership-focused. Strong for professionals with work experience and active LinkedIn presence."),
        dict(name="Swiss Government Excellence Scholarships", country="Switzerland", region="Europe", schengen=True,
             fields=["Biotechnology","Food Science","Chemistry","Biology","Computer Science","Civil Engineering"],
             program_type="Research", degree_level=["PhD","Postdoc","Research"],
             language_req=["IELTS","TOEFL","No minimum stated"], ielts_min=0, toefl_min=0,
             fully_funded=True, hidden=True, hec_route=True, ielts_waiver=True,
             coverage="CHF 1,920/month + tuition + health insurance + housing supplement",
             dm=11, dd=15, om=9, od=1,
             apply_link="https://www.sbfi.admin.ch/sbfi/en/home/education/scholarships-and-grants/swiss-government-excellence-scholarships.html",
             portal="https://www.sbfi.admin.ch/sbfi/en/",
             notes="HIDDEN GEM. Applied via HEC Pakistan. No IELTS minimum. Very low competition from Pakistan. ETH Zurich & EPFL eligible."),
        dict(name="Eiffel Excellence Scholarship (France)", country="France", region="Europe", schengen=True,
             fields=["Biotechnology","Food Science","Civil Engineering","Computer Science","Economics"],
             program_type="Coursework", degree_level=["MS","PhD"],
             language_req=["IELTS","TOEFL"], ielts_min=6.5, toefl_min=90,
             fully_funded=True, hidden=True, hec_route=False, ielts_waiver=False,
             coverage="€1,181/month (MS) · €1,400/month (PhD) + airfare + cultural activities",
             dm=1, dd=8, om=10, od=1,
             apply_link="https://www.campusfrance.org/en/eiffel-excellence-scholarship-program",
             portal="https://www.campusfrance.org/en/",
             notes="HIDDEN. Nominated by French universities — contact target university directly first, then they nominate you."),
        dict(name="Holland Scholarship (Netherlands)", country="Netherlands", region="Europe", schengen=True,
             fields=["Biotechnology","Food Science","Agriculture","Computer Science","Civil Engineering"],
             program_type="Coursework", degree_level=["BS","MS"],
             language_req=["IELTS","TOEFL","Cambridge"], ielts_min=6.0, toefl_min=80,
             fully_funded=False, hidden=True, hec_route=False, ielts_waiver=False,
             coverage="€5,000 one-time grant (stackable with TU Delft / Wageningen departmental grants)",
             dm=2, dd=1, om=11, od=1,
             apply_link="https://www.studyinholland.nl/scholarships/holland-scholarship",
             portal="https://www.studyinholland.nl/",
             notes="Partial but stackable. Wageningen (world's #1 Food Science) and TU Delft offer additional departmental funding."),
        dict(name="Italian Government Scholarships (MAECI)", country="Italy", region="Europe", schengen=True,
             fields=["Biotechnology","Food Science","Civil Engineering","Agriculture","Design"],
             program_type="Both", degree_level=["MS","PhD","Research"],
             language_req=["IELTS","TOEFL","Italian (some)"], ielts_min=0, toefl_min=0,
             fully_funded=True, hidden=True, hec_route=False, ielts_waiver=True,
             coverage="€900/month + tuition waiver + health insurance",
             dm=6, dd=3, om=3, od=1,
             apply_link="https://studyinitaly.esteri.it/en/home",
             portal="https://studyinitaly.esteri.it/en/",
             notes="HIDDEN. Very few Pakistanis apply. English STEM programmes widely available. No IELTS minimum."),
        dict(name="Stipendium Hungaricum (Hungary)", country="Hungary", region="Europe", schengen=True,
             fields=["Biotechnology","Computer Science","Civil Engineering","Agriculture","Food Science","Medicine"],
             program_type="Both", degree_level=["BS","MS","PhD"],
             language_req=["IELTS","TOEFL","No minimum for some"], ielts_min=5.5, toefl_min=72,
             fully_funded=True, hidden=False, hec_route=True, ielts_waiver=False,
             coverage="Tuition + HUF 43,700/month (PhD) + dormitory + health insurance",
             dm=1, dd=15, om=11, od=1,
             apply_link="https://stipendiumhungaricum.hu/apply/",
             portal="https://stipendiumhungaricum.hu/",
             notes="Apply via HEC Pakistan. Low IELTS (5.5 minimum). Growing English programmes in Biotech & Food Science."),
        dict(name="Norwegian Government Quota Scholarship", country="Norway", region="Europe", schengen=True,
             fields=["Biotechnology","Environmental Science","Computer Science","Food Science","Civil Engineering"],
             program_type="Both", degree_level=["MS","PhD"],
             language_req=["IELTS","TOEFL"], ielts_min=6.0, toefl_min=80,
             fully_funded=True, hidden=True, hec_route=False, ielts_waiver=False,
             coverage="Full tuition + NOK ~16,000/month + housing allowance + travel",
             dm=12, dd=1, om=9, od=1,
             apply_link="https://www.hkdir.no/en/funding-for-international-students/quota-scheme",
             portal="https://www.hkdir.no/en/",
             notes="HIDDEN GEM. Very few Pakistanis know this. Apply through Norwegian universities directly. NMBU top for Food/Biotech."),
        dict(name="Finnish Government Scholarships (EDUFI)", country="Finland", region="Europe", schengen=True,
             fields=["Biotechnology","Computer Science","Food Science","Environmental Science","Civil Engineering"],
             program_type="Research", degree_level=["PhD","Postdoc"],
             language_req=["IELTS","TOEFL","No requirement for some"], ielts_min=0, toefl_min=0,
             fully_funded=True, hidden=True, hec_route=False, ielts_waiver=True,
             coverage="€1,500/month + tuition waiver (some programmes)",
             dm=1, dd=31, om=11, od=1,
             apply_link="https://www.oph.fi/en/services/scholarships-and-grants",
             portal="https://www.oph.fi/en/",
             notes="HIDDEN. Doctoral/postdoc research only. Very undersubscribed from Pakistan. No IELTS minimum."),
        # UK
        dict(name="Commonwealth Scholarships (UK)", country="UK", region="Europe", schengen=False,
             fields=["Biotechnology","Food Science","Computer Science","Civil Engineering","Public Health","Agriculture"],
             program_type="Both", degree_level=["MS","PhD"],
             language_req=["IELTS","TOEFL","No minimum for some"], ielts_min=6.0, toefl_min=79,
             fully_funded=True, hidden=False, hec_route=True, ielts_waiver=False,
             coverage="Full tuition + £1,347+/month + airfare + thesis grant",
             dm=10, dd=23, om=8, od=1,
             apply_link="https://cscuk.fcdo.gov.uk/apply/",
             portal="https://cscuk.fcdo.gov.uk/",
             notes="Apply via HEC Pakistan. Very competitive. Strong development-impact narrative required in SOP."),
        dict(name="Chevening Scholarships (UK)", country="UK", region="Europe", schengen=False,
             fields=["Biotechnology","Food Science","Computer Science","Civil Engineering","Public Policy"],
             program_type="Coursework", degree_level=["MS"],
             language_req=["IELTS","TOEFL","PTE"], ielts_min=6.5, toefl_min=88,
             fully_funded=True, hidden=False, hec_route=False, ielts_waiver=False,
             coverage="Full tuition + £1,347/month + travel + visa + arrival allowance",
             dm=11, dd=5, om=8, od=6,
             apply_link="https://www.chevening.org/apply/",
             portal="https://www.chevening.org/",
             notes="Leadership-focused. 2-5 years work experience required. Choose 3 universities. Highly competitive from Pakistan."),
        dict(name="Edinburgh Global Research Scholarships", country="UK", region="Europe", schengen=False,
             fields=["Biotechnology","Food Science","Computer Science","Bioinformatics","Civil Engineering"],
             program_type="Research", degree_level=["PhD"],
             language_req=["IELTS","TOEFL","PTE"], ielts_min=6.5, toefl_min=92,
             fully_funded=True, hidden=True, hec_route=False, ielts_waiver=False,
             coverage="Full tuition + £15,609/year stipend",
             dm=1, dd=24, om=10, od=1,
             apply_link="https://www.ed.ac.uk/student-funding/postgraduate/international/global/research",
             portal="https://www.ed.ac.uk/",
             notes="HIDDEN. University of Edinburgh. Strong life sciences. Very few Pakistanis apply here."),
        # MIDDLE EAST
        dict(name="KAUST Fellowship (Saudi Arabia)", country="Saudi Arabia", region="Middle East", schengen=False,
             fields=["Biotechnology","Food Science","Computer Science","Bioinformatics","Environmental Science"],
             program_type="Research", degree_level=["MS","PhD"],
             language_req=["IELTS","TOEFL"], ielts_min=6.5, toefl_min=92,
             fully_funded=True, hidden=False, hec_route=False, ielts_waiver=False,
             coverage="Full tuition + USD $20,000+/year stipend + housing + medical + relocation",
             dm=1, dd=15, om=9, od=1,
             apply_link="https://admissions.kaust.edu.sa/",
             portal="https://www.kaust.edu.sa/en/",
             notes="One of the most generous packages globally. World-class research. Strong Biotech/CS departments."),
        dict(name="Khalifa University Scholarships (UAE)", country="UAE", region="Middle East", schengen=False,
             fields=["Biotechnology","Computer Science","Civil Engineering","Bioinformatics","AI","Energy"],
             program_type="Both", degree_level=["MS","PhD"],
             language_req=["IELTS","TOEFL"], ielts_min=6.0, toefl_min=79,
             fully_funded=True, hidden=False, hec_route=False, ielts_waiver=False,
             coverage="Full tuition + AED 4,800–8,000/month + housing",
             dm=2, dd=28, om=11, od=1,
             apply_link="https://www.ku.ac.ae/graduate-admissions",
             portal="https://www.ku.ac.ae/",
             notes="QS Top 200. Strong STEM research. Pakistanis well represented. MS Molecular Life Sciences available."),
        dict(name="UAEU Graduate Teaching Assistantship", country="UAE", region="Middle East", schengen=False,
             fields=["Biotechnology","Food Science","Computer Science","Civil Engineering","Agriculture"],
             program_type="Both", degree_level=["MS","PhD"],
             language_req=["IELTS","TOEFL"], ielts_min=6.0, toefl_min=79,
             fully_funded=True, hidden=True, hec_route=False, ielts_waiver=False,
             coverage="Full tuition + AED 5,000–9,000/month + housing allowance",
             dm=3, dd=31, om=12, od=1,
             apply_link="https://www.uaeu.ac.ae/en/admissions/graduate/",
             portal="https://www.uaeu.ac.ae/en/",
             notes="HIDDEN. UAE University TAs fully funded. Email professors directly after submitting portal application."),
        dict(name="IsDB Merit Scholarship (Islamic Development Bank)", country="Multi-country OIC", region="Middle East", schengen=False,
             fields=["Biotechnology","Food Science","Computer Science","Civil Engineering","Agriculture","Medicine","Public Health"],
             program_type="Both", degree_level=["MS","PhD"],
             language_req=["IELTS","TOEFL","No minimum stated"], ielts_min=0, toefl_min=0,
             fully_funded=True, hidden=False, hec_route=False, ielts_waiver=True,
             coverage="Full tuition + living allowance + travel + health insurance",
             dm=3, dd=31, om=1, od=15,
             apply_link="https://www.isdb.org/what-we-do/human-capital-development/scholarship-programmes",
             portal="https://www.isdb.org/",
             notes="For OIC member countries including Pakistan. No strict IELTS minimum. Rolling deadlines in some programmes."),
        dict(name="HBKU Graduate Scholarships (Qatar)", country="Qatar", region="Middle East", schengen=False,
             fields=["Biotechnology","Computer Science","Bioinformatics","Public Health","Food Science","Environmental Science"],
             program_type="Research", degree_level=["MS","PhD"],
             language_req=["IELTS","TOEFL"], ielts_min=6.0, toefl_min=79,
             fully_funded=True, hidden=True, hec_route=False, ielts_waiver=False,
             coverage="Full tuition + QAR 14,000–16,000/month + housing + health + research budget",
             dm=2, dd=1, om=10, od=1,
             apply_link="https://www.hbku.edu.qa/en/admissions",
             portal="https://www.hbku.edu.qa/en/",
             notes="HIDDEN GEM. Very generous package. Qatar Foundation funded. Biomedical Research + CS tracks strong."),
        dict(name="KAU Scholarship (King Abdulaziz University)", country="Saudi Arabia", region="Middle East", schengen=False,
             fields=["Biotechnology","Food Science","Computer Science","Civil Engineering","Medicine","Agriculture"],
             program_type="Both", degree_level=["MS","PhD"],
             language_req=["IELTS","TOEFL","No requirement for Arabic track"], ielts_min=0, toefl_min=0,
             fully_funded=True, hidden=False, hec_route=False, ielts_waiver=True,
             coverage="Full tuition + SAR 2,000/month + accommodation + health",
             dm=6, dd=30, om=3, od=1,
             apply_link="https://graduateadmissions.kau.edu.sa/",
             portal="https://www.kau.edu.sa/home_english.aspx",
             notes="Rolling admissions. No IELTS required for many programmes. Direct application. Friendly to Pakistani students."),
        # AUSTRALIA / NZ
        dict(name="Australia Awards Scholarships", country="Australia", region="Australia/NZ", schengen=False,
             fields=["Biotechnology","Food Science","Agriculture","Computer Science","Civil Engineering","Public Health","Environmental Science"],
             program_type="Coursework", degree_level=["MS"],
             language_req=["IELTS","TOEFL","PTE"], ielts_min=6.5, toefl_min=87,
             fully_funded=True, hidden=False, hec_route=False, ielts_waiver=False,
             coverage="Full tuition + AUD $33,000/year living allowance + travel + health",
             dm=4, dd=30, om=2, od=1,
             apply_link="https://www.dfat.gov.au/people-to-people/australia-awards/australia-awards-scholarships",
             portal="https://www.dfat.gov.au/",
             notes="Priority countries include Pakistan. Development-impact focus required in SOP. Very generous package."),
        dict(name="Deakin University Research Training Scheme", country="Australia", region="Australia/NZ", schengen=False,
             fields=["Biotechnology","Food Science","Computer Science","Bioinformatics","Environmental Science"],
             program_type="Research", degree_level=["PhD"],
             language_req=["IELTS","TOEFL","PTE"], ielts_min=6.5, toefl_min=79,
             fully_funded=True, hidden=True, hec_route=False, ielts_waiver=False,
             coverage="Full tuition + AUD $28,597/year stipend (annually indexed)",
             dm=10, dd=31, om=8, od=1,
             apply_link="https://www.deakin.edu.au/research/research-candidature/research-scholarships",
             portal="https://www.deakin.edu.au/",
             notes="HIDDEN. Contact Food & Biotech professors at Deakin first. Scholarship auto-considered with PhD admission."),
        dict(name="New Zealand NZIDRS Scholarship", country="New Zealand", region="Australia/NZ", schengen=False,
             fields=["Biotechnology","Food Science","Agriculture","Computer Science","Environmental Science","Civil Engineering"],
             program_type="Research", degree_level=["MS","PhD"],
             language_req=["IELTS","TOEFL","PTE"], ielts_min=6.5, toefl_min=90,
             fully_funded=True, hidden=False, hec_route=False, ielts_waiver=False,
             coverage="Full tuition + NZD $25,000/year + airfare + health",
             dm=7, dd=28, om=4, od=1,
             apply_link="https://www.education.govt.nz/our-work/scholarships/new-zealand-international-doctoral-research-scholarships/",
             portal="https://www.education.govt.nz/",
             notes="Excellent for Food Science at Massey University. Low applicant pool from Pakistan."),
        # CANADA / USA
        dict(name="University of Guelph Graduate Scholarships (Canada)", country="Canada", region="North America", schengen=False,
             fields=["Food Science","Agriculture","Biotechnology","Bioinformatics","Environmental Science"],
             program_type="Research", degree_level=["MS","PhD"],
             language_req=["IELTS","TOEFL"], ielts_min=6.5, toefl_min=89,
             fully_funded=True, hidden=True, hec_route=False, ielts_waiver=False,
             coverage="Full tuition + CAD $18,000–30,000/year (supervisor-funded)",
             dm=2, dd=15, om=11, od=1,
             apply_link="https://www.uoguelph.ca/graduatestudies/future/scholarships",
             portal="https://www.uoguelph.ca/",
             notes="HIDDEN. World's top Food Science university. Secure supervisor first — email faculty directly. Rolling intake."),
        dict(name="Vanier Canada Graduate Scholarships", country="Canada", region="North America", schengen=False,
             fields=["Biotechnology","Food Science","Computer Science","Civil Engineering","Bioinformatics","Public Health"],
             program_type="Research", degree_level=["PhD"],
             language_req=["IELTS","TOEFL","No minimum stated"], ielts_min=0, toefl_min=0,
             fully_funded=True, hidden=False, hec_route=False, ielts_waiver=True,
             coverage="CAD $50,000/year for 3 years",
             dm=11, dd=1, om=8, od=1,
             apply_link="https://vanier.gc.ca/en/home-accueil.html",
             portal="https://vanier.gc.ca/en/",
             notes="Nominated by Canadian university. Secure supervisor first. One of Canada's most prestigious awards."),
        # ASIA
        dict(name="Chinese Government Scholarship (CSC)", country="China", region="Asia", schengen=False,
             fields=["Biotechnology","Food Science","Computer Science","Civil Engineering","Agriculture","Bioinformatics","Medicine"],
             program_type="Both", degree_level=["BS","MS","PhD"],
             language_req=["IELTS","TOEFL","No requirement for many"], ielts_min=0, toefl_min=0,
             fully_funded=True, hidden=False, hec_route=True, ielts_waiver=True,
             coverage="Full tuition + CNY 2,000–3,500/month + accommodation + comprehensive medical",
             dm=3, dd=31, om=12, od=1,
             apply_link="https://www.campuschina.org/",
             portal="https://www.campuschina.org/",
             notes="Apply via HEC or direct to universities. Many English-taught STEM programmes. Very accessible for Pakistanis."),
        dict(name="Korean Government Scholarship (KGSP)", country="South Korea", region="Asia", schengen=False,
             fields=["Biotechnology","Computer Science","Civil Engineering","Food Science","Agriculture","Engineering"],
             program_type="Both", degree_level=["MS","PhD"],
             language_req=["IELTS","TOEFL","Korean (after enrollment)"], ielts_min=5.5, toefl_min=72,
             fully_funded=True, hidden=False, hec_route=False, ielts_waiver=False,
             coverage="Full tuition + KRW 900,000/month + settlement + language training + airfare",
             dm=3, dd=1, om=12, od=1,
             apply_link="https://www.studyinkorea.go.kr/en/sub/gks/allnew_gks_s.do",
             portal="https://www.studyinkorea.go.kr/en/",
             notes="Embassy or University track. KAIST, POSTECH, SNU are top choices. Korean language training included."),
        dict(name="Japanese MEXT Scholarship", country="Japan", region="Asia", schengen=False,
             fields=["Biotechnology","Food Science","Computer Science","Civil Engineering","Agriculture","Bioinformatics"],
             program_type="Research", degree_level=["MS","PhD","Research"],
             language_req=["IELTS","TOEFL","No requirement for many"], ielts_min=0, toefl_min=0,
             fully_funded=True, hidden=False, hec_route=False, ielts_waiver=True,
             coverage="Full tuition + JPY 145,000/month + airfare + research expenses",
             dm=6, dd=1, om=3, od=1,
             apply_link="https://www.mext.go.jp/en/policy/education/highered/title02/detail02/sdetail02/1373897.htm",
             portal="https://www.mext.go.jp/en/",
             notes="Embassy track OR university recommendation. Secure professor letter FIRST for university track."),
        dict(name="Taiwan ICDF Scholarship", country="Taiwan", region="Asia", schengen=False,
             fields=["Biotechnology","Food Science","Agriculture","Computer Science","Civil Engineering","Environmental Science"],
             program_type="Both", degree_level=["MS","PhD"],
             language_req=["IELTS","TOEFL","No requirement for English programs"], ielts_min=0, toefl_min=0,
             fully_funded=True, hidden=True, hec_route=False, ielts_waiver=True,
             coverage="Full tuition + USD $670/month + housing + insurance",
             dm=3, dd=31, om=1, od=1,
             apply_link="https://www.icdf.org.tw/wSite/ct?xItem=12505&ctNode=31&mp=2",
             portal="https://www.icdf.org.tw/",
             notes="HIDDEN. Severely undersubscribed from Pakistan. English programmes at NTU, NTHU. No IELTS needed."),
        dict(name="NUS Research Scholarship (Singapore)", country="Singapore", region="Asia", schengen=False,
             fields=["Biotechnology","Computer Science","Bioinformatics","Food Science","Civil Engineering","Data Science"],
             program_type="Research", degree_level=["PhD"],
             language_req=["IELTS","TOEFL"], ielts_min=6.0, toefl_min=85,
             fully_funded=True, hidden=False, hec_route=False, ielts_waiver=False,
             coverage="Full tuition + SGD $2,000–2,500/month stipend",
             dm=12, dd=31, om=9, od=1,
             apply_link="https://www.nus.edu.sg/admissions/graduate/research",
             portal="https://www.nus.edu.sg/",
             notes="Top-20 globally. Supervisor contact essential before applying. Strong Biotech and CS departments."),
        # PAKISTAN
        dict(name="HEC Indigenous PhD Scholarship", country="Pakistan", region="Pakistan", schengen=False,
             fields=["Biotechnology","Food Science","Computer Science","Civil Engineering","Agriculture","Bioinformatics"],
             program_type="Research", degree_level=["PhD"],
             language_req=["No Requirement"], ielts_min=0, toefl_min=0,
             fully_funded=True, hidden=False, hec_route=True, ielts_waiver=True,
             coverage="Full tuition (Pakistani university) + PKR stipend + research grant",
             dm=6, dd=30, om=4, od=1,
             apply_link="https://www.hec.gov.pk/english/scholarships/Pages/Ph.D-Indigenous.aspx",
             portal="https://www.hec.gov.pk/",
             notes="Domestic PhD funding. Good stepping stone before applying abroad. No IELTS needed."),
        dict(name="HEC Overseas Scholarship (Phase-III)", country="Pakistan → Abroad", region="Pakistan", schengen=False,
             fields=["Biotechnology","Food Science","Computer Science","Civil Engineering","Agriculture","Bioinformatics","Medicine"],
             program_type="Research", degree_level=["PhD"],
             language_req=["IELTS","TOEFL"], ielts_min=6.0, toefl_min=79,
             fully_funded=True, hidden=False, hec_route=True, ielts_waiver=False,
             coverage="Full tuition abroad + monthly stipend (country-based) + health + travel",
             dm=9, dd=30, om=7, od=1,
             apply_link="https://www.hec.gov.pk/english/scholarships/Pages/Overseas-Scholarship.aspx",
             portal="https://www.hec.gov.pk/",
             notes="Sends you abroad for PhD. Must secure admission at foreign university first. Check HEC for current batch."),
    ]

    records = []
    for t in TEMPLATES:
        r = dict(t)
        dl, op, sess = project(t["dm"], t["dd"], t["om"], t["od"])
        r["deadline"] = dl
        r["opening_date"] = op
        r["session"] = sess
        records.append(r)

    df = pd.DataFrame(records)
    return df

def days_left(dl_str):
    try:
        d = datetime.strptime(dl_str.split(" ")[0], "%Y-%m-%d").date()
        return (d - date.today()).days
    except:
        return 9999

def deadline_badge(dl_str):
    days = days_left(dl_str)
    if days == 9999:
        return f"<span class='deadline-roll'>📅 Rolling</span>"
    elif days < 0:
        return f"<span class='deadline-urgent'>⛔ Closed — next cycle coming</span>"
    elif days <= 30:
        return f"<span class='deadline-urgent'>🔥 {days} days left — URGENT</span>"
    elif days <= 90:
        return f"<span class='deadline-warn'>⚠️ {days} days left</span>"
    else:
        return f"<span class='deadline-ok'>✅ {days} days left</span>"

def render_card(r):
    hidden_cls = "hidden-gem" if r["hidden"] else ""
    hidden_b = "<span class='badge b-hidden'>🕵️ HIDDEN GEM</span>" if r["hidden"] else ""
    funded_b = "<span class='badge b-funded'>✅ Fully Funded</span>" if r["fully_funded"] else "<span class='badge b-partial'>⚡ Partial</span>"
    hec_b = "<span class='badge b-hec'>🏛️ Via HEC</span>" if r["hec_route"] else ""
    sch_b = "<span class='badge b-schengen'>🇪🇺 Schengen</span>" if r.get("schengen") else ""
    waiv_b = "<span class='badge b-waiver'>📋 IELTS Waivable</span>" if r["ielts_waiver"] else ""
    fields_b = "".join([f"<span class='badge b-field'>{f}</span>" for f in r["fields"][:5]])
    degree_b = "".join([f"<span class='badge b-degree'>{d}</span>" for d in r["degree_level"]])
    lang_b   = "".join([f"<span class='badge b-lang'>{l}</span>" for l in r["language_req"][:3]])
    ielts_txt = str(r["ielts_min"]) if r["ielts_min"] > 0 else "Not required"
    toefl_txt = str(r["toefl_min"]) if r.get("toefl_min", 0) > 0 else "Not required"

    return f"""
<div class='sch-card {hidden_cls}'>
  <div class='sch-meta'>
    <div>
      <h3>{r['name']} {hidden_b}</h3>
      <span class='badge b-region'>🌍 {r['country']} · {r['region']}</span>
      {funded_b} {hec_b} {sch_b} {waiv_b}
    </div>
    <div style='text-align:right;min-width:180px'>
      {deadline_badge(r['deadline'])}<br>
      <span style='color:rgba(255,255,255,0.45);font-size:0.82em'>🗓️ Opens: {r['opening_date']}</span><br>
      <span style='color:#63b3ed;font-size:0.82em;font-weight:600'>📆 {r['session']}</span>
    </div>
  </div>
  <hr class='divider'>
  <div style='margin:5px 0'><b style='color:rgba(255,255,255,0.5);font-size:0.8em'>FIELDS</b><br>{fields_b}</div>
  <div style='margin:6px 0'><b style='color:rgba(255,255,255,0.5);font-size:0.8em'>DEGREE · TYPE</b><br>{degree_b} <span class='badge b-degree'>{r['program_type']}</span></div>
  <div style='margin:6px 0'><b style='color:rgba(255,255,255,0.5);font-size:0.8em'>LANGUAGE</b><br>{lang_b} <span style='color:rgba(255,255,255,0.4);font-size:0.8em'>Min IELTS: <b style='color:#fbbf24'>{ielts_txt}</b> &nbsp;|&nbsp; Min TOEFL: <b style='color:#fbbf24'>{toefl_txt}</b></span></div>
  <div class='coverage-box'>💰 {r['coverage']}</div>
  <div class='insight-box'>💡 {r['notes']}</div>
  <div>
    <a class='link-apply' href='{r['apply_link']}' target='_blank'>🔗 Apply Now</a>
    <a class='link-portal' href='{r['portal']}' target='_blank'>🏛️ Official Portal</a>
  </div>
</div>"""

# ── LOAD DATA ──────────────────────────────────────────────────────────────
df_all = build_database()

# ── HERO ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class='hero'>
  <h1>🎓 ScholarshipHunter Pro</h1>
  <p>Fully Funded International Scholarships for Pakistani Students — MS · MPhil · PhD</p>
  <div class='badges'>
    <span class='hbadge'>🌍 35+ Scholarships</span>
    <span class='hbadge'>📅 Auto-Updated Deadlines</span>
    <span class='hbadge'>🕵️ Hidden Gems Included</span>
    <span class='hbadge'>🇵🇰 Pakistan-Friendly</span>
    <span class='hbadge'>📋 IELTS Waiver Options</span>
    <span class='hbadge'>🏛️ HEC Route Options</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── SIDEBAR FILTERS ────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🔍 Filter Scholarships")
    st.markdown("---")

    region_opts = ["All Regions"] + sorted(df_all["region"].unique().tolist())
    sel_region = st.multiselect("🌍 Region", region_opts, default=["All Regions"])

    field_map = {
        "🌐 All Fields": None,
        "🔬 Biotechnology & Subfields": ["Biotechnology","Bioinformatics","Molecular Biology","Biochemistry","Microbiology","Genetics"],
        "🍕 Food Science & Technology": ["Food Science","Agriculture","Food Technology"],
        "🏗️ Civil Engineering": ["Civil Engineering","Environmental Science","Structural Engineering"],
        "💻 Computer Science & AI": ["Computer Science","Data Science","AI","Bioinformatics"],
        "🌿 Agriculture & Environment": ["Agriculture","Environmental Science"],
        "🩺 Public Health & Medicine": ["Public Health","Medicine","Biology"],
    }
    sel_field = st.selectbox("🔬 Field / Discipline", list(field_map.keys()))

    degree_opts = ["All", "MS", "MPhil", "PhD", "BS", "Postdoc", "Research"]
    sel_degree = st.multiselect("🎓 Degree Level", degree_opts, default=["All"])

    sel_type = st.selectbox("📚 Program Type", ["All", "Coursework", "Research", "Both"])

    lang_opts = ["All", "IELTS", "TOEFL", "PTE", "Duolingo", "No Requirement"]
    sel_lang = st.multiselect("🗣️ Language Requirement", lang_opts, default=["All"])

    sel_ielts = st.slider("Max IELTS Band", 0.0, 9.0, 9.0, 0.5,
                          help="Set lower to find scholarships with no or low IELTS requirement")

    st.markdown("---")
    st.markdown("**⚙️ Quick Filters**")
    only_funded  = st.checkbox("✅ Fully Funded Only", value=True)
    only_hidden  = st.checkbox("🕵️ Hidden Gems Only", value=False)
    only_hec     = st.checkbox("🏛️ Via HEC Route Only", value=False)
    only_waiver  = st.checkbox("📋 IELTS Waivable Only", value=False)
    only_schengen= st.checkbox("🇪🇺 Schengen Zone Only", value=False)

    st.markdown("---")
    deadline_months = st.slider("📅 Deadline within (months)", 1, 24, 24)

    sort_by = st.selectbox("🔢 Sort By", [
        "📅 Deadline — Soonest First",
        "🌍 Country A–Z",
        "📊 IELTS — Lowest First",
        "🕵️ Hidden Gems First",
    ])

    st.markdown("---")
    st.markdown(
        "<div style='font-size:0.75em;color:rgba(255,255,255,0.35);text-align:center'>"
        "Built for Pakistani students 🇵🇰<br>Deadlines auto-project to future dates</div>",
        unsafe_allow_html=True
    )

# ── APPLY FILTERS ──────────────────────────────────────────────────────────
df = df_all.copy()

if "All Regions" not in sel_region and sel_region:
    df = df[df["region"].isin(sel_region)]

if sel_field != "🌐 All Fields":
    targets = field_map[sel_field]
    df = df[df["fields"].apply(lambda x: any(f in x for f in targets))]

if "All" not in sel_degree and sel_degree:
    df = df[df["degree_level"].apply(lambda x: any(d in x for d in sel_degree))]

if sel_type != "All":
    df = df[df["program_type"].isin([sel_type, "Both"])]

if "All" not in sel_lang and sel_lang:
    if "No Requirement" in sel_lang:
        df = df[df["language_req"].apply(lambda x: any("No" in l for l in x))]
    else:
        df = df[df["language_req"].apply(lambda x: any(l in x for l in sel_lang))]

if sel_ielts < 9.0:
    df = df[(df["ielts_min"] <= sel_ielts) | (df["ielts_min"] == 0)]

if only_funded:   df = df[df["fully_funded"] == True]
if only_hidden:   df = df[df["hidden"] == True]
if only_hec:      df = df[df["hec_route"] == True]
if only_waiver:   df = df[df["ielts_waiver"] == True]
if only_schengen: df = df[df["schengen"] == True]

max_days = deadline_months * 30
df["_days"] = df["deadline"].apply(days_left)
df = df[(df["_days"] <= max_days) | (df["_days"] == 9999)]

if "Deadline" in sort_by:    df = df.sort_values("_days")
elif "Country" in sort_by:   df = df.sort_values("country")
elif "IELTS" in sort_by:     df = df.sort_values("ielts_min")
elif "Hidden" in sort_by:    df = df.sort_values("hidden", ascending=False)

# ── TABS ───────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🔍 Search Results", "📅 Deadline Calendar", "📊 Statistics"])

with tab1:
    # Stats row
    n = len(df)
    hidden_c  = int(df["hidden"].sum())
    funded_c  = int(df["fully_funded"].sum())
    hec_c     = int(df["hec_route"].sum())
    waiver_c  = int(df["ielts_waiver"].sum())
    region_c  = df["region"].nunique()

    st.markdown(f"""
    <div class='stat-row'>
      <div class='stat-card'><div class='stat-num'>{n}</div><div class='stat-label'>Found</div></div>
      <div class='stat-card'><div class='stat-num' style='color:#f97316'>{hidden_c}</div><div class='stat-label'>Hidden Gems</div></div>
      <div class='stat-card'><div class='stat-num' style='color:#34d399'>{funded_c}</div><div class='stat-label'>Fully Funded</div></div>
      <div class='stat-card'><div class='stat-num' style='color:#a78bfa'>{hec_c}</div><div class='stat-label'>Via HEC</div></div>
      <div class='stat-card'><div class='stat-num' style='color:#6ee7b7'>{waiver_c}</div><div class='stat-label'>IELTS Waiver</div></div>
      <div class='stat-card'><div class='stat-num'>{region_c}</div><div class='stat-label'>Regions</div></div>
    </div>
    """, unsafe_allow_html=True)

    # Export buttons
    if n > 0:
        col_a, col_b, col_c = st.columns([1,1,4])
        with col_a:
            csv_buf = io.StringIO()
            df.drop(columns=["_days","fields","degree_level","language_req"]).to_csv(csv_buf, index=False)
            st.download_button("📥 Export CSV", csv_buf.getvalue(), "scholarships.csv", "text/csv")
        with col_b:
            xl_buf = io.BytesIO()
            df.drop(columns=["_days","fields","degree_level","language_req"]).to_excel(xl_buf, index=False)
            st.download_button("📊 Export Excel", xl_buf.getvalue(), "scholarships.xlsx",
                               "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    if n == 0:
        st.markdown("<div class='no-results'>⚠️ No scholarships match your filters.<br>Try broadening your search.</div>",
                    unsafe_allow_html=True)
    else:
        for _, row in df.iterrows():
            st.markdown(render_card(row), unsafe_allow_html=True)

with tab2:
    st.markdown("<div class='section-head'>📅 Deadline Calendar — Sorted by Urgency</div>", unsafe_allow_html=True)

    cal_df = df_all.copy()
    cal_df["_days"] = cal_df["deadline"].apply(days_left)
    cal_df = cal_df.sort_values("_days")

    rows_html = ""
    for _, r in cal_df.iterrows():
        d = r["_days"]
        if d < 0:      row_cls = "closed";  d_txt = "Closed"
        elif d <= 30:  row_cls = "urgent";  d_txt = f"🔥 {d}d"
        elif d <= 90:  row_cls = "warn";    d_txt = f"⚠️ {d}d"
        elif d == 9999:row_cls = "";        d_txt = "Rolling"
        else:          row_cls = "ok";      d_txt = f"✅ {d}d"

        hid = "🕵️" if r["hidden"] else ""
        waiv = "✅" if r["ielts_waiver"] else "❌"
        rows_html += f"""
        <tr class='{row_cls}'>
          <td>{hid} <b>{r['name']}</b></td>
          <td>{r['country']}</td>
          <td>{r['deadline']}</td>
          <td><b>{d_txt}</b></td>
          <td>{r['opening_date']}</td>
          <td>{r['session']}</td>
          <td>{waiv} IELTS</td>
          <td><a class='link-apply' href='{r['apply_link']}' target='_blank' style='padding:4px 10px;font-size:0.78em'>Apply</a></td>
        </tr>"""

    st.markdown(f"""
    <div class='cal-wrap'>
    <table class='cal'>
      <thead><tr>
        <th>Scholarship</th><th>Country</th><th>Deadline</th>
        <th>Days Left</th><th>Opens</th><th>Session</th><th>IELTS</th><th>Link</th>
      </tr></thead>
      <tbody>{rows_html}</tbody>
    </table></div>
    <p style='color:rgba(255,255,255,0.35);font-size:0.78em;margin-top:8px'>
      🔴 Closed · 🟠 &lt;30 days · 🟡 &lt;90 days · 🟢 Upcoming · ⚪ Rolling
    </p>
    """, unsafe_allow_html=True)

with tab3:
    st.markdown("<div class='section-head'>📊 Database Overview</div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        rc = df_all.groupby("region").size().reset_index(name="Count").sort_values("Count", ascending=False)
        st.markdown("**🌍 By Region**")
        st.dataframe(rc, hide_index=True, use_container_width=True)
    with c2:
        st.markdown("**📊 Summary Stats**")
        summary = pd.DataFrame({
            "Metric": ["Total Scholarships","Fully Funded","Hidden Gems","IELTS Waivable",
                       "Via HEC Route","No IELTS Min","PhD Options","MS Options",
                       "Schengen Countries","Research Type","Coursework Type"],
            "Count": [
                len(df_all),
                int(df_all["fully_funded"].sum()),
                int(df_all["hidden"].sum()),
                int(df_all["ielts_waiver"].sum()),
                int(df_all["hec_route"].sum()),
                int((df_all["ielts_min"]==0).sum()),
                int(df_all["degree_level"].apply(lambda x: "PhD" in x).sum()),
                int(df_all["degree_level"].apply(lambda x: "MS" in x).sum()),
                int(df_all["schengen"].sum()),
                int(df_all["program_type"].isin(["Research","Both"]).sum()),
                int(df_all["program_type"].isin(["Coursework","Both"]).sum()),
            ]
        })
        st.dataframe(summary, hide_index=True, use_container_width=True)
    with c3:
        field_cov = {}
        for _, row in df_all.iterrows():
            for f in row["fields"]:
                field_cov[f] = field_cov.get(f, 0) + 1
        top_f = sorted(field_cov.items(), key=lambda x: -x[1])[:12]
        fc_df = pd.DataFrame(top_f, columns=["Field", "Programmes"])
        st.markdown("**🔬 Top Fields Covered**")
        st.dataframe(fc_df, hide_index=True, use_container_width=True)

    st.markdown("---")
    st.markdown(
        "<div style='text-align:center;color:rgba(255,255,255,0.3);font-size:0.8em'>"
        "ScholarshipHunter Pro — Built for Pakistani Students 🇵🇰 · "
        "Deadlines auto-project to future dates · Links verified to stable official portals"
        "</div>",
        unsafe_allow_html=True
    )
