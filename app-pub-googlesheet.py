import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Google Sheet → DataFrame", layout="wide")
st.title("Google Sheet → DataFrame")

# ---- Secrets & connection ----
# Put your Sheet URL in .streamlit/secrets.toml as:
# GOOGLURL = "https://docs.google.com/spreadsheets/d/XXXXX/edit#gid=0"
if "GOOGLURL" not in st.secrets:
    st.error("Missing `GOOGLURL` in secrets. Add it to `.streamlit/secrets.toml` or Streamlit Cloud → Settings → Secrets.")
    st.stop()

SHEET_URL = st.secrets["GOOGLURL"]

# Create a connection object (provided by streamlit_gsheets)
conn = st.connection("gsheets", type=GSheetsConnection)

# ---- Optional: pick a worksheet by name (leave blank for the first sheet) ----
worksheet = st.text_input("Worksheet name (optional)", value="")

@st.cache_data(show_spinner=False, ttl=300)
def read_sheet(url: str, sheet_name: str | None) -> pd.DataFrame:
    # If sheet_name is empty, let the connector load the first/default sheet
    if sheet_name and sheet_name.strip():
        return conn.read(spreadsheet=url, worksheet=sheet_name.strip())
    return conn.read(spreadsheet=url)

# ---- Load + display ----
try:
    df = read_sheet(SHEET_URL, worksheet or None)
    if df is None or df.empty:
        st.warning("The sheet is empty or the worksheet name didn’t match. Check your data and worksheet name.")
    else:
        st.success("Loaded Google Sheet ✅")
        st.dataframe(df, use_container_width=True)
        with st.expander("Preview (head)"):
            st.write(df.head())
except Exception as e:
    st.error(f"Error reading Google Sheet: {e}")
