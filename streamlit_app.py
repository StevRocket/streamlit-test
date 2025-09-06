import io
import requests
import pandas as pd
import streamlit as st

# -------- Settings from Streamlit secrets --------
TOKEN  = st.secrets["GITHUB_TOKEN"]
OWNER  = st.secrets["DATA_OWNER"]
REPO   = st.secrets["DATA_REPO"]
BRANCH = st.secrets.get("DATA_BRANCH", "main")
PREFIX = st.secrets.get("DATA_PREFIX", "").strip("/")
RAW_BASE = "https://raw.githubusercontent.com"
BASE = "https://github.com"

def _build_raw_url(path_in_repo: str) -> str:
    """Build the raw.githubusercontent.com URL for a file in the private repo."""
    clean = path_in_repo.strip("/")
    if PREFIX:
        clean = f"{PREFIX}/{clean}"
    return f"{BASE}/{OWNER}/{REPO}/blob/{BRANCH}/{PREFIX}/{clean}"

@st.cache_data(show_spinner=False, ttl=3600)
def load_private_csv(path_in_repo: str) -> pd.DataFrame:
    """Download and load a private CSV file from GitHub using a token."""
    url = _build_raw_url(path_in_repo)
    r = requests.get(url, headers={"Authorization": f"token {TOKEN}"}, timeout=30)
    if r.status_code == 404:
        raise FileNotFoundError(f"Not found in private repo: {path_in_repo}")
    r.raise_for_status()
    return pd.read_csv(io.StringIO(r.text))

# -------- Streamlit App --------
st.title("Private CSV Loader")

try:
    df = load_private_csv("course_map.csv")  # 👈 change filename as needed
    st.success("CSV file loaded successfully ✅")
    st.dataframe(df)  # display the dataframe
except Exception as e:
    st.error(f"Error loading CSV: {e}")
