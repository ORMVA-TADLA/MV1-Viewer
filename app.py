import streamlit as st
import pandas as pd
import os

# Set the page layout to wide for better data viewing
st.set_page_config(page_title="MV1 Data Viewer", layout="wide")

# App Title
st.header("📊 MV1 Data Viewer", divider="rainbow", anchor=False)


# Function to load data (caches it so it doesn't reload on every interaction)
@st.cache_data
def load_data(filename):
    # 1. Define a dictionary mapping column names to their data types
    data_types = {
        "Heure départ": float,
        "Heure Fin": float,
        "Durée": float,
    }

    # 2. List your date columns here
    date_columns = ["Date départ", "Date Fin"]

    # 3. Pass both arguments to read_csv
    return pd.read_csv(filename, dtype=data_types, parse_dates=date_columns)


try:
    # Load your specific file
    df = load_data("MV1.csv")

    # --- SIDEBAR FOR FILTERS ---
    # Moving controls to the sidebar keeps the main area clean for the data
    with st.sidebar:
        st.subheader("Filter Settings")

        # Define preferred columns, but check if they actually exist in the CSV
        preferred_columns = ["Matricule", "Code Client", "Code Parcelle", "Tertiaire"]
        available_columns = [col for col in preferred_columns if col in df.columns]

        # Fallback: if none of the preferred columns exist, allow filtering by any column
        if not available_columns:
            available_columns = df.columns.tolist()

        column_to_filter = st.selectbox(
            "1. Select a column:",
            options=available_columns,
        )

        # Get unique values and use multiselect instead of a single selectbox
        unique_values = df[column_to_filter].dropna().unique()
        selected_values = st.multiselect(
            f"2. Select value(s) for {column_to_filter}:",
            options=unique_values,
            default=[],  # Default to empty (which we will treat as "show all")
        )

    # --- MAIN CONTENT AREA ---
    # Apply filtering logic
    if selected_values:
        filtered_df = df[df[column_to_filter].isin(selected_values)]
        status_message = f"Showing results for **{column_to_filter}** in ({', '.join(map(str, selected_values))})"
    else:
        filtered_df = df
        status_message = "Showing all results."

    # 1. Display summary metrics using st.metric for a polished look
    col1, col2 = st.columns(2)
    col1.metric(label="Total Records", value=df.shape[0])

    # 2. Display the dataframe
    st.write(status_message)
    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True,
        height=600,
        column_config={
            # Force these specific columns to take up more space
            "Date départ": st.column_config.DatetimeColumn(
                width=140, format="YYYY MMMM DD - HH:mm"
            ),
            "Date Fin": st.column_config.DatetimeColumn(
                width=140, format="YYYY MMMM DD - HH:mm"
            ),
        },
    )

except FileNotFoundError:
    st.error(
        "Error: Could not find 'MV1.csv'. Please ensure the file is in the same directory as this script."
    )
except Exception as e:
    st.error(f"An unexpected error occurred: {e}")
