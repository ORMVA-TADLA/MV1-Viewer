import streamlit as st
import pandas as pd

# Set the page layout to wide for better data viewing
st.set_page_config(page_title="Data Viewer", layout="wide")

# App Title
st.title("📊 MV1 Data Viewer")


# Function to load data (caches it so it doesn't reload on every interaction)
@st.cache_data
def load_data(filename):
    return pd.read_csv(filename)


try:
    # Load your specific file
    df = load_data("MV1.csv")

    # 1. Display summary metrics
    col1, col2 = st.columns(2)
    col1.metric("Total Records", df.shape[0])

    st.divider()

    # 2. Add an interactive data table
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.divider()

    # 3. Add some basic filtering
    # the mileage column is the default filter
    st.subheader("Filter by Column")
    columns_to_filter = st.selectbox(
        "Select a column to view its unique values:",
        ["Matricule","Code Client", "Code Parcelle", "Tertiaire"],
    )

    # Get unique values for the selected column
    unique_values = df[columns_to_filter].dropna().unique()

    selected_value = st.selectbox(
        "Select a value to filter by:", ["All"] + list(unique_values)
    )

    if selected_value != "All":
        filtered_df = df[df[columns_to_filter] == selected_value]
        st.write(
            f"Showing results for **{columns_to_filter} = {selected_value}** ({len(filtered_df)} rows)"
        )
        st.dataframe(filtered_df, use_container_width=True)

except FileNotFoundError:
    st.error(
        "Error: Could not find 'MV1.csv'. Please ensure the file is in the same directory as this script."
    )
except Exception as e:
    st.error(f"An error occurred: {e}")
