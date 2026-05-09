import streamlit as st
import pandas as pd
from datetime import date, datetime, timedelta
import io

st.set_page_config(
    page_title="ScholarshipHunter Pro — Hassan Iqbal",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════════════════════
# GOOGLE ANALYTICS (Copy this ID to your Google Analytics account)
# ══════════════════════════════════════════════════════════════════════════
st.markdown("""
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
<!-- Replace G-XXXXXXXXXX with your actual Google Analytics ID -->
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════
# PROFESSIONAL LIGHT THEME CSS
# ══════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

* {
    font-family: 'Inter', sans-serif !important;
}

html, body {
    background: #ffffff !important;
    color: #1a202c !important;
}

[data-testid="stAppViewContainer"] {
    background: #ffffff !important;
}

[data-testid="stSidebar"] {
    background: #f8f9fa !important;
    border-right: 1px solid #e8eef5 !important;
}

#MainMenu, footer { visibility: hidden; }
.block-container { padding-top: 0 !important; max-width: 1200px; }

/* ── NAVIGATION BAR ── */
.navbar {
    background: #ffffff;
    border-bottom: 1px solid #e8eef5;
    padding: 16px 40px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 100;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}
.navbar-logo {
    font-size: 1.3em;
    font-weight: 800;
    color: #1e3a8a;
    text-decoration: none;
    display: flex;
    align-items: center;
    gap: 8px;
}
.navbar-links {
    display: flex;
    gap: 32px;
    align-items: center;
    flex: 1;
    margin-left: 48px;
}
.navbar-link {
    text-decoration: none;
    color: #4b5563;
    font-weight: 500;
    font-size: 0.95em;
    transition: color 0.2s;
}
.navbar-link:hover, .navbar-link.active {
    color: #1e3a8a;
    border-bottom: 3px solid #1e3a8a;
    padding-bottom: 2px;
}
.navbar-auth {
    display: flex;
    gap: 12px;
}
.navbar-btn {
    padding: 8px 16px;
    border-radius: 6px;
    text-decoration: none;
    font-weight: 600;
    font-size: 0.9em;
    cursor: pointer;
}
.navbar-login {
    color: #1e3a8a;
    border: 1px solid #1e3a8a;
    background: transparent;
}
.navbar-signup {
    background: #1e3a8a;
    color: white;
}
.navbar-signup:hover {
    background: #1a3073;
}

/* ── HERO SECTION ── */
.hero {
    background: linear-gradient(135deg, #e0eef9 0%, #f0f4ff 100%);
    padding: 48px 40px;
    display: flex;
    gap: 48px;
    align-items: center;
    margin-bottom: 40px;
    border-radius: 0;
}
.hero-left {
    flex: 1;
}
.hero-tag {
    background: #e0eef9;
    color: #1e3a8a;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 0.85em;
    font-weight: 600;
    display: inline-block;
    margin-bottom: 16px;
}
.hero h1 {
    font-size: 2.5em;
    font-weight: 800;
    color: #1e3a8a;
    margin: 0 0 12px;
    line-height: 1.2;
}
.hero-highlight {
    color: #2563eb;
}
.hero p {
    color: #636e7a;
    font-size: 1em;
    margin: 0 0 24px;
    line-height: 1.6;
}
.search-box {
    background: white;
    padding: 16px;
    border-radius: 8px;
    border: 1px solid #e0e5ec;
    display: flex;
    gap: 8px;
    margin-bottom: 16px;
}
.search-box input {
    flex: 1;
    border: none;
    outline: none;
    font-size: 0.95em;
}
.search-box select {
    border: none;
    outline: none;
    background: #f8f9fa;
    padding: 6px 12px;
    border-radius: 4px;
    font-size: 0.9em;
}
.search-btn {
    background: #1e3a8a;
    color: white;
    border: none;
    padding: 10px 24px;
    border-radius: 6px;
    font-weight: 600;
    cursor: pointer;
}
.search-btn:hover {
    background: #1a3073;
}
.popular-searches {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    margin-top: 12px;
}
.search-tag {
    color: #2563eb;
    text-decoration: none;
    font-size: 0.85em;
    font-weight: 500;
}
.hero-image {
    flex: 1;
    background: linear-gradient(135deg, #e0eef9 0%, #d4e4f7 100%);
    border-radius: 12px;
    height: 380px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #94a3b8;
    font-size: 4em;
}

/* ── FEATURE CARDS ── */
.features {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    margin: 40px 0;
}
.feature-card {
    background: white;
    border: 1px solid #e8eef5;
    border-radius: 10px;
    padding: 24px;
    text-align: center;
    transition: box-shadow 0.2s;
}
.feature-card:hover {
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}
.feature-icon {
    font-size: 2.5em;
    margin-bottom: 12px;
}
.feature-card h3 {
    font-size: 0.95em;
    font-weight: 700;
    color: #1a202c;
    margin: 0 0 8px;
}
.feature-card p {
    font-size: 0.85em;
    color: #636e7a;
    margin: 0;
}

/* ── CATEGORY SECTION ── */
.category-section {
    margin: 60px 0;
}
.category-header {
    margin-bottom: 28px;
}
.category-label {
    font-size: 0.78em;
    font-weight: 700;
    color: #4da6ff;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 8px;
}
.category-section h2 {
    font-size: 1.8em;
    font-weight: 800;
    color: #1e3a8a;
    margin: 0 0 12px;
}
.category-section p {
    color: #636e7a;
    margin: 0;
}
.category-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 16px;
    margin-top: 24px;
}
.category-card {
    background: white;
    border: 1px solid #e8eef5;
    border-radius: 10px;
    padding: 24px;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s;
}
.category-card:hover {
    border-color: #1e3a8a;
    box-shadow: 0 4px 12px rgba(30,58,138,0.12);
}
.category-icon {
    font-size: 3em;
    margin-bottom: 12px;
}
.category-card h3 {
    font-size: 0.95em;
    font-weight: 700;
    color: #1a202c;
    margin: 0 0 6px;
}
.category-count {
    font-size: 0.85em;
    color: #94a3b8;
}
.explore-link {
    color: #2563eb;
    text-decoration: none;
    font-weight: 600;
    font-size: 0.85em;
    margin-top: 10px;
    display: inline-block;
}

/* ── SCHOLARSHIP CARDS ── */
.sch-card {
    background: white;
    border: 1px solid #e8eef5;
    border-radius: 10px;
    padding: 20px;
    margin-bottom: 12px;
    transition: all 0.2s;
}
.sch-card:hover {
    box-shadow: 0 4px 16px rgba(0,0,0,0.08);
    border-color: #2563eb;
}
.sch-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 12px;
}
.sch-title {
    font-size: 1.05em;
    font-weight: 700;
    color: #1e3a8a;
    margin: 0;
}
.sch-dates {
    font-size: 0.9em;
    color: #636e7a;
    text-align: right;
}
.sch-dates-range {
    font-weight: 600;
    color: #1e3a8a;
}
.sch-dates-label {
    font-size: 0.8em;
    color: #94a3b8;
}
.sch-meta {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    margin-bottom: 12px;
}
.badge {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 0.75em;
    font-weight: 600;
}
.b-country {
    background: #e0eef9;
    color: #1e3a8a;
}
.b-field {
    background: #dcfce7;
    color: #166534;
}
.b-funded {
    background: #dbeafe;
    color: #1e40af;
}
.b-hidden {
    background: #fed7aa;
    color: #b45309;
}
.b-rtp {
    background: #d1fae5;
    color: #065f46;
}
.sch-coverage {
    background: #f0f8ff;
    border-left: 3px solid #2563eb;
    padding: 10px 12px;
    margin: 12px 0;
    border-radius: 0 6px 6px 0;
    font-size: 0.9em;
    color: #1e3a8a;
}
.sch-links {
    display: flex;
    gap: 12px;
    margin-top: 12px;
}
.link-btn {
    display: inline-block;
    padding: 8px 16px;
    border-radius: 6px;
    text-decoration: none;
    font-size: 0.85em;
    font-weight: 600;
}
.link-apply {
    background: #1e3a8a;
    color: white;
}
.link-apply:hover {
    background: #1a3073;
}
.link-portal {
    background: #f0f4f8;
    color: #1e3a8a;
}
.link-portal:hover {
    background: #e0eef9;
}

/* ── STATS ROW ── */
.stat-row {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    margin: 20px 0;
}
.stat-card {
    flex: 1;
    min-width: 130px;
    background: white;
    border: 1px solid #e8eef5;
    border-radius: 10px;
    padding: 16px;
    text-align: center;
}
.stat-num {
    font-size: 1.8em;
    font-weight: 800;
    color: #1e3a8a;
    font-family: 'JetBrains Mono', monospace;
}
.stat-label {
    font-size: 0.75em;
    color: #636e7a;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-top: 6px;
}

/* ── FOOTER ── */
.footer {
    border-top: 1px solid #e8eef5;
    padding: 40px;
    margin-top: 60px;
    text-align: center;
    background: #f8f9fa;
}
.footer p {
    color: #636e7a;
    font-size: 0.9em;
    margin: 0;
}
.footer-credit {
    margin-top: 12px;
    font-size: 0.85em;
    color: #1e3a8a;
    font-weight: 600;
}

/* ── TABS ── */
[data-testid="stTabs"] [aria-selected="true"] {
    color: #1e3a8a !important;
    border-bottom-color: #1e3a8a !important;
}

/* ── BUTTONS ── */
.stButton > button {
    background: #1e3a8a !important;
    color: white !important;
    border: none !important;
    font-weight: 700 !important;
    border-radius: 6px !important;
}
.stButton > button:hover {
    background: #1a3073 !important;
}

/* ── TABLES ── */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
}
table th {
    background: #1e3a8a;
    color: white;
    padding: 12px;
    text-align: left;
    font-weight: 700;
}
table td {
    padding: 10px 12px;
    border-bottom: 1px solid #e8eef5;
    color: #1a202c;
}
table tr:hover {
    background: #f0f4f8;
}

/* ── RESPONSIVE ── */
@media (max-width: 768px) {
    .hero {
        flex-direction: column;
    }
    .hero-image {
        display: none;
    }
    .hero h1 {
        font-size: 2em;
    }
    .features, .category-grid {
        grid-template-columns: repeat(2, 1fr);
    }
    .navbar-links {
        display: none;
    }
}
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
                    return dl, op
            except ValueError:
                pass
        return None, None

    T = [
        # ══ EUROPE (First 10 for brevity in this example) ══
        dict(name="DAAD Research Grants", country="Germany", region="Europe", schengen=True,
             fields=["Biotechnology","Food Science","Civil Engineering","Computer Science"],
             program_type="Both", degree_level=["MS","PhD","Postdoc"],
             language_req=["IELTS","TOEFL"], ielts_min=6.0, toefl_min=80,
             fully_funded=True, hidden=False, hec_route=False, ielts_waiver=False, rtp=False,
             coverage="Tuition + ~€934/month + travel + health insurance",
             dm=10, dd=15, om=8, od=1,
             apply_link="https://www.daad.de/en/study-and-research-in-germany/scholarships/",
             portal="https://www.daad.de/en/",
             notes="One of the largest programs globally. Research & coursework available."),
        dict(name="Erasmus Mundus Joint Masters", country="Multi-country EU", region="Europe", schengen=True,
             fields=["Biotechnology","Food Science","Computer Science","Civil Engineering"],
             program_type="Coursework", degree_level=["MS"],
             language_req=["IELTS","TOEFL"], ielts_min=6.5, toefl_min=90,
             fully_funded=True, hidden=False, hec_route=False, ielts_waiver=False, rtp=False,
             coverage="€1,400/month + tuition + travel",
             dm=1, dd=15, om=10, od=1,
             apply_link="https://www.eacea.ec.europa.eu/scholarships/erasmus-mundus-catalogue_en",
             portal="https://erasmus-plus.ec.europa.eu/",
             notes="Study in 2-3 EU countries. Highly prestigious. 100+ programmes."),
        dict(name="Swiss Government Excellence Scholarships", country="Switzerland", region="Europe", schengan=True,
             fields=["Biotechnology","Food Science","Chemistry","Biology","Computer Science"],
             program_type="Research", degree_level=["PhD","Postdoc"],
             language_req=["IELTS","TOEFL"], ielts_min=0, toefl_min=0,
             fully_funded=True, hidden=True, hec_route=True, ielts_waiver=True, rtp=False,
             coverage="CHF 1,920/month + tuition + health + housing",
             dm=11, dd=15, om=9, od=1,
             apply_link="https://www.sbfi.admin.ch/sbfi/en/home/education/scholarships-and-grants/swiss-government-excellence-scholarships.html",
             portal="https://www.sbfi.admin.ch/sbfi/en/",
             notes="HIDDEN GEM. Via HEC Pakistan. No IELTS minimum."),
        dict(name="Chevening Scholarships (UK)", country="UK", region="Europe", schengen=False,
             fields=["Biotechnology","Food Science","Computer Science","Civil Engineering"],
             program_type="Coursework", degree_level=["MS"],
             language_req=["IELTS","TOEFL","PTE"], ielts_min=6.5, toefl_min=88,
             fully_funded=True, hidden=False, hec_route=False, ielts_waiver=False, rtp=False,
             coverage="Full tuition + £1,347/month + travel + visa",
             dm=11, dd=5, om=8, od=6,
             apply_link="https://www.chevening.org/apply/",
             portal="https://www.chevening.org/",
             notes="Leadership-focused. 2-5 years work experience required."),
        dict(name="Commonwealth Scholarships (UK)", country="UK", region="Europe", schengen=False,
             fields=["Biotechnology","Food Science","Computer Science","Civil Engineering"],
             program_type="Both", degree_level=["MS","PhD"],
             language_req=["IELTS","TOEFL"], ielts_min=6.0, toefl_min=79,
             fully_funded=True, hidden=False, hec_route=True, ielts_waiver=False, rtp=False,
             coverage="Full tuition + £1,347+/month + airfare",
             dm=10, dd=23, om=8, od=1,
             apply_link="https://cscuk.fcdo.gov.uk/apply/",
             portal="https://cscuk.fcdo.gov.uk/",
             notes="Apply via HEC Pakistan. Very competitive."),
        dict(name="KAUST Fellowship (Saudi Arabia)", country="Saudi Arabia", region="Middle East", schengan=False,
             fields=["Biotechnology","Food Science","Computer Science","Bioinformatics"],
             program_type="Research", degree_level=["MS","PhD"],
             language_req=["IELTS","TOEFL"], ielts_min=6.5, toefl_min=92,
             fully_funded=True, hidden=False, hec_route=False, ielts_waiver=False, rtp=True,
             coverage="Full tuition + USD $20,000+/year + housing + medical",
             dm=1, dd=15, om=9, od=1,
             apply_link="https://admissions.kaust.edu.sa/",
             portal="https://www.kaust.edu.sa/en/",
             notes="One of the most generous packages globally. World-class research."),
        dict(name="Australia Awards Scholarships", country="Australia", region="Australia/NZ", schengan=False,
             fields=["Biotechnology","Food Science","Computer Science","Civil Engineering"],
             program_type="Coursework", degree_level=["MS"],
             language_req=["IELTS","TOEFL","PTE"], ielts_min=6.5, toefl_min=87,
             fully_funded=True, hidden=False, hec_route=False, ielts_waiver=False, rtp=False,
             coverage="Full tuition + AUD $33,000/year + travel + health",
             dm=4, dd=30, om=2, od=1,
             apply_link="https://www.dfat.gov.au/people-to-people/australia-awards/australia-awards-scholarships",
             portal="https://www.dfat.gov.au/",
             notes="Priority countries include Pakistan. Very generous."),
        dict(name="Fulbright Foreign Student Program (USA)", country="USA", region="North America", schengan=False,
             fields=["Biotechnology","Food Science","Computer Science","Civil Engineering"],
             program_type="Both", degree_level=["MS","PhD"],
             language_req=["IELTS","TOEFL"], ielts_min=6.5, toefl_min=90,
             fully_funded=True, hidden=False, hec_route=False, ielts_waiver=False, rtp=False,
             coverage="Full tuition + stipend + health + travel",
             dm=10, dd=15, om=7, od=1,
             apply_link="https://www.usefp.org/fulbright-foreign-student-program/",
             portal="https://www.usefp.org/",
             notes="Apply via USEFP Pakistan. Extremely prestigious."),
        dict(name="University of Vermont Graduate Assistant Funding", country="USA (Vermont)", region="North America", schengan=False,
             fields=["Biotechnology","Computer Science","Civil Engineering","Environmental Science"],
             program_type="Research", degree_level=["MS","PhD"],
             language_req=["IELTS","TOEFL"], ielts_min=6.5, toefl_min=90,
             fully_funded=True, hidden=True, hec_route=False, ielts_waiver=False, rtp=True,
             coverage="Full tuition + $18,000-22,000/year (GRA/GTA) + health",
             dm=1, dd=15, om=10, od=1,
             apply_link="https://www.uvm.edu/graduate/admissions",
             portal="https://www.uvm.edu/",
             notes="HIDDEN GEM. Email professors directly about GRA/GTA."),
        dict(name="Chinese Government Scholarship (CSC)", country="China", region="Asia", schengan=False,
             fields=["Biotechnology","Food Science","Computer Science","Civil Engineering"],
             program_type="Both", degree_level=["BS","MS","PhD"],
             language_req=["IELTS","TOEFL","No requirement"], ielts_min=0, toefl_min=0,
             fully_funded=True, hidden=False, hec_route=True, ielts_waiver=True, rtp=False,
             coverage="Full tuition + CNY 2,000–3,500/month + housing + medical",
             dm=3, dd=31, om=12, od=1,
             apply_link="https://www.campuschina.org/",
             portal="https://www.campuschina.org/",
             notes="Very accessible for Pakistanis. Many English STEM programs."),
    ]

    records = []
    for t in T:
        r = dict(t)
        dl, op = project(t["dm"], t["dd"], t["om"], t["od"])
        r["deadline"] = dl
        r["opening_date"] = op
        records.append(r)
    return pd.DataFrame(records)

df_all = build_database()

# ══════════════════════════════════════════════════════════════════════════
# NAVIGATION BAR
# ══════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="navbar">
  <div class="navbar-logo">
    🎓 ScholarshipHunter
  </div>
  <div class="navbar-links">
    <a href="#" class="navbar-link active">Home</a>
    <a href="#" class="navbar-link">Scholarships</a>
    <a href="#" class="navbar-link">Universities</a>
    <a href="#" class="navbar-link">Resources</a>
    <a href="#" class="navbar-link">Blog</a>
    <a href="#" class="navbar-link">About Us</a>
  </div>
  <div class="navbar-auth">
    <button class="navbar-btn navbar-login">Login</button>
    <button class="navbar-btn navbar-signup">Sign Up</button>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════
# HERO SECTION
# ══════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
  <div class="hero-left">
    <div class="hero-tag">✓ Find. Apply. Achieve.</div>
    <h1>Find Scholarships.<br><span class="hero-highlight">Build Your Future.</span></h1>
    <p>Discover 53 fully funded scholarships worldwide and get the financial support you need to achieve your dreams.</p>
    
    <div class="search-box">
      <input type="text" placeholder="Search scholarships...">
      <select>
        <option>All Countries</option>
        <option>USA</option>
        <option>Europe</option>
        <option>Asia</option>
        <option>Australia</option>
      </select>
      <select>
        <option>All Levels</option>
        <option>MS</option>
        <option>PhD</option>
        <option>BS</option>
      </select>
      <button class="search-btn">Search</button>
    </div>
    
    <div class="popular-searches">
      Popular Searches: 
      <a href="#" class="search-tag">Fully Funded</a>
      <a href="#" class="search-tag">USA</a>
      <a href="#" class="search-tag">Europe</a>
      <a href="#" class="search-tag">RTP-Type</a>
      <a href="#" class="search-tag">Hidden Gems</a>
    </div>
  </div>
  <div class="hero-image">📚 Student</div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════
# FEATURE CARDS
# ══════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="features">
  <div class="feature-card">
    <div class="feature-icon">🔍</div>
    <h3>Search Scholarships</h3>
    <p>Explore thousands tailored to your profile and interests.</p>
  </div>
  <div class="feature-card">
    <div class="feature-icon">✓</div>
    <h3>Check Eligibility</h3>
    <p>Find opportunities that match your qualifications.</p>
  </div>
  <div class="feature-card">
    <div class="feature-icon">📝</div>
    <h3>Apply with Confidence</h3>
    <p>Get expert tips for successful applications.</p>
  </div>
  <div class="feature-card">
    <div class="feature-icon">🏆</div>
    <h3>Achieve Your Goals</h3>
    <p>Secure funding and build your future.</p>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════
# CATEGORY SECTION
# ══════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="category-section">
  <div class="category-header">
    <div class="category-label">EXPLORE OPPORTUNITIES</div>
    <h2>Browse Scholarships by Category</h2>
    <p>Find the right scholarship that matches your field of study and interests.</p>
  </div>
  <div class="category-grid">
    <div class="category-card">
      <div class="category-icon">👨‍🎓</div>
      <h3>Undergraduate</h3>
      <div class="category-count">8 Scholarships</div>
      <a href="#" class="explore-link">Explore →</a>
    </div>
    <div class="category-card">
      <div class="category-icon">📚</div>
      <h3>Masters</h3>
      <div class="category-count">32 Scholarships</div>
      <a href="#" class="explore-link">Explore →</a>
    </div>
    <div class="category-card">
      <div class="category-icon">🔬</div>
      <h3>PhD</h3>
      <div class="category-count">28 Scholarships</div>
      <a href="#" class="explore-link">Explore →</a>
    </div>
    <div class="category-card">
      <div class="category-icon">💻</div>
      <h3>STEM</h3>
      <div class="category-count">42 Scholarships</div>
      <a href="#" class="explore-link">Explore →</a>
    </div>
    <div class="category-card">
      <div class="category-icon">🌍</div>
      <h3>International</h3>
      <div class="category-count">53 Scholarships</div>
      <a href="#" class="explore-link">Explore →</a>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════
# MAIN CONTENT AREA
# ══════════════════════════════════════════════════════════════════════════
st.markdown("<h2 style='color:#1e3a8a; margin-top:40px'>Available Scholarships</h2>", unsafe_allow_html=True)

# Filter sidebar
with st.sidebar:
    st.markdown("### 🔍 Filter Scholarships")
    sel_region = st.multiselect("Region", ["All"] + sorted(df_all["region"].unique().tolist()), default=["All"])
    sel_field = st.selectbox("Field", ["All Fields"] + list(set([f for fields in df_all["fields"] for f in fields])))
    sel_funded = st.checkbox("Fully Funded Only", value=True)
    sel_hidden = st.checkbox("Hidden Gems", value=False)
    sel_rtp = st.checkbox("RTP-Type Only", value=False)

# Apply filters
df = df_all.copy()
if "All" not in sel_region and sel_region:
    df = df[df["region"].isin(sel_region)]
if sel_funded:
    df = df[df["fully_funded"] == True]
if sel_hidden:
    df = df[df["hidden"] == True]
if sel_rtp:
    df = df[df["rtp"] == True]

# Stats
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.markdown(f"<div class='stat-card'><div class='stat-num'>{len(df)}</div><div class='stat-label'>Found</div></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='stat-card'><div class='stat-num'>{int(df['hidden'].sum())}</div><div class='stat-label'>Hidden Gems</div></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='stat-card'><div class='stat-num'>{int(df['rtp'].sum())}</div><div class='stat-label'>RTP-Type</div></div>", unsafe_allow_html=True)
with col4:
    st.markdown(f"<div class='stat-card'><div class='stat-num'>{int(df['fully_funded'].sum())}</div><div class='stat-label'>Fully Funded</div></div>", unsafe_allow_html=True)
with col5:
    st.markdown(f"<div class='stat-card'><div class='stat-num'>{df['region'].nunique()}</div><div class='stat-label'>Regions</div></div>", unsafe_allow_html=True)

# Display scholarships with CLEAR DATE RANGES
for _, row in df.iterrows():
    open_str = row["opening_date"].strftime("%b %d, %Y") if row["opening_date"] else "TBD"
    close_str = row["deadline"].strftime("%b %d, %Y") if row["deadline"] else "Rolling"
    
    hidden_badge = "<span class='badge b-hidden'>🕵️ HIDDEN GEM</span>" if row["hidden"] else ""
    rtp_badge = "<span class='badge b-rtp'>🎯 RTP-TYPE</span>" if row["rtp"] else ""
    funded_badge = "<span class='badge b-funded'>✅ Fully Funded</span>" if row["fully_funded"] else ""
    
    fields_str = ", ".join(row["fields"][:3])
    
    card_html = f"""
    <div class="sch-card">
      <div class="sch-header">
        <h3 class="sch-title">{row['name']} {hidden_badge} {rtp_badge}</h3>
        <div class="sch-dates">
          <div class="sch-dates-range">📅 {open_str} – {close_str}</div>
          <div class="sch-dates-label">Opens – Closes</div>
        </div>
      </div>
      <div class="sch-meta">
        <span class="badge b-country">🌍 {row['country']}</span>
        {funded_badge}
      </div>
      <p style="margin:8px 0; color:#636e7a; font-size:0.9em"><strong>Fields:</strong> {fields_str}</p>
      <div class="sch-coverage">💰 {row['coverage']}</div>
      <p style="margin:8px 0; color:#636e7a; font-size:0.9em">💡 {row['notes']}</p>
      <div class="sch-links">
        <a href="{row['apply_link']}" target="_blank" class="link-btn link-apply">Apply Now →</a>
        <a href="{row['portal']}" target="_blank" class="link-btn link-portal">Official Portal</a>
      </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
  <p>ScholarshipHunter Pro — Find Your Future</p>
  <div class="footer-credit">
    👨‍🔬 Built by <strong>Hassan Iqbal</strong> | Biotechnologist, UVAS Lahore 2022–2026 | 🇵🇰 For Pakistani Students
  </div>
</div>
""", unsafe_allow_html=True)
