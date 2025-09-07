import pandas as pd
import streamlit as st

st.set_page_config(page_title="CSV from URL Viewer", page_icon="🌐", layout="wide")

st.title("🌐 CSV from URL Viewer")
st.caption("Enter a URL to a CSV file and display it interactively.")

# Input field for CSV URL
csv_url = st.text_input("https://raw.githubusercontent.com/StevRocket/streamlit-test/refs/heads/master/course_map.csv")

# Options
sep = st.selectbox("Delimiter", options=[",", ";", "\t", "|"], index=0)
encoding = st.selectbox("Encoding", options=["utf-8", "utf-8-sig", "latin-1", "cp1252"], index=0)
header_row = st.checkbox("First row is header", value=True)

# Load CSV if URL is provided
if csv_url:
    try:
        header = 0 if header_row else None
        df = pd.read_csv(csv_url, sep=sep, encoding=encoding, header=header)
        st.success("CSV loaded successfully ✅")

        # Show dataset info
        with st.expander("Dataset Info", expanded=False):
            st.write(f"**Rows:** {len(df):,}")
            st.write(f"**Columns:** {df.shape[1]:,}")
            st.write("**Column types:**")
            st.write(df.dtypes.astype(str))

        # Display the table with filtering options
        st.subheader("Table Preview")
        q = st.text_input("Filter rows (case-insensitive contains search)")
        max_rows = st.slider("Max rows to display", min_value=10, max_value=2000, value=100, step=10)

        view_df = df
        if q:
            q_lower = q.lower()
            mask = view_df.astype(str).apply(lambda col: col.str.lower().str.contains(q_lower, na=False))
            view_df = view_df[mask.any(axis=1)]

        st.dataframe(view_df.head(max_rows), use_container_width=True)

        # Download filtered data
        csv_bytes = view_df.to_csv(index=False).encode(encoding)
        st.download_button(
            label="Download filtered CSV",
            data=csv_bytes,
            file_name="filtered_view.csv",
            mime="text/csv",
        )
    except Exception as e:
        st.error(f"Failed to load CSV: {e}")
else:
    st.info("Enter a valid CSV URL above to begin.")
