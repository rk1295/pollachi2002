import streamlit as st
import pandas as pd

# -----------------------------------
# PAGE SETTINGS
# -----------------------------------
st.set_page_config(
    page_title="123 Pollachi AC - SIR 2002 Search",
    layout="wide"
)

# Mobile-friendly padding and font adjustments
st.markdown("""
    <style>
        .block-container { padding-top: 1rem; padding-left: 0.5rem; padding-right: 0.5rem; }
        input[type="text"] { font-size: 1.1rem; }
        button[kind="secondary"] { width: 100%; }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------
# PAGE TITLES
# -----------------------------------
st.title("🗳️ 123 பொள்ளாச்சி சட்டமன்ற தொகுதி (Pollachi Assembly Constituency)")
st.subheader("🔍 வாக்காளர் விவரம் - 2002 (Voter Details - 2002)")

# -----------------------------------
# LOAD DATA
# -----------------------------------
@st.cache_data(show_spinner=True)
def load_data():
    try:
        df = pd.read_excel("old_data.xlsx")
    except Exception as e:
        st.error(f"Excel கோப்பை ஏற்ற முடியவில்லை (Failed to load Excel file): {e}")
        return pd.DataFrame()

    df["FM_NAME_V2"] = df["FM_NAME_V2"].astype(str).str.strip()
    df["RLN_FM_NM_V2"] = df["RLN_FM_NM_V2"].astype(str).str.strip()

    return df

df = load_data()
if df.empty:
    st.stop()

# -----------------------------------
# INPUT SECTION
# -----------------------------------
st.markdown("### 📝 விவரங்களை உள்ளிடவும் (Enter Details)")

voter_name = st.text_input(
    "வாக்காளர் பெயர் (Voter's Name) – தமிழ் மட்டும் (Tamil Only)",
    placeholder="உதா: ராமு (Example: Ramu)"
)

relation_name = st.text_input(
    "தந்தை / கணவர் பெயர் (Father's / Husband's Name) – தமிழ் மட்டும் (Tamil Only)",
    placeholder="உதா: முருகேசன் (Example: Murugesan)"
)

# -----------------------------------
# SEARCH OPERATION
# -----------------------------------
if st.button("🔍 தேடு (Search)"):

    name_part = voter_name.strip()
    rname_part = relation_name.strip()

    if not name_part and not rname_part:
        st.warning("⚠️ வாக்காளர் பெயர் அல்லது தந்தை/கணவர் பெயரை உள்ளிடவும் (Please enter either Voter's Name or Father's/Husband's Name).")
        st.stop()

    results = df.copy()

    def safe_contains(series, value):
        return series.str.contains(value, case=False, na=False, regex=False)

    if name_part:
        results = results[safe_contains(results["FM_NAME_V2"], name_part)]

    if rname_part:
        results = results[safe_contains(results["RLN_FM_NM_V2"], rname_part)]

    # -----------------------------------
    # RESULTS
    # -----------------------------------
    if not results.empty:
        st.success(f"✔ {len(results)} பதிவுகள் கிடைத்தன (record(s) found).")
        st.dataframe(results, use_container_width=True)
    else:
        st.error("❌ பொருந்தும் பதிவுகள் இல்லை (No matching records found).")
