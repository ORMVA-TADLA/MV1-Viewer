import pandas as pd
import os


def xlsx_to_csv_remove_and_rename_columns(
    input_xlsx, output_csv, columns_to_remove, columns_to_rename, agriculteur_xlsx=None
):
    """
    Converts an Excel (.xlsx) file to a CSV (.csv) file, removes specified columns,
    and renames (remaps) specific columns.
    """
    try:
        # Check if the input file exists
        if not os.path.exists(input_xlsx):
            print(f"Error: The file '{input_xlsx}' does not exist.")
            return

        print(f"Reading '{input_xlsx}'...")

        # Read the Excel file
        df = pd.read_excel(input_xlsx)

        # 1. Combining Dates and Hours
        # Pair the date column with its corresponding hour column
        date_hour_pairs = [("dato2", "heureo2"), ("datf2", "heuref2")]

        for date_col, hour_col in date_hour_pairs:
            if date_col in df.columns and hour_col in df.columns:
                # Convert the date column to a base datetime object
                base_date = pd.to_datetime(df[date_col], errors="coerce")

                # Convert the hour column to a numeric value, then turn it into a TimeDelta (hours)
                hours_to_add = pd.to_timedelta(
                    pd.to_numeric(df[hour_col], errors="coerce"), unit="h"
                )

                # Add the hours to the base date and format it
                df[date_col] = (base_date + hours_to_add).dt.strftime("%Y-%m-%d %H")
                print(f"Combined '{date_col}' and '{hour_col}' into a full datetime.")

            elif date_col in df.columns:
                # Fallback just in case the hour column is missing from the file
                df[date_col] = pd.to_datetime(
                    df[date_col], errors="coerce"
                ).dt.strftime("%Y-%m-%d")
                print(
                    f"Warning: '{hour_col}' missing. Converted '{date_col}' to date only."
                )

        # 2. Remove the specified columns
        if columns_to_remove:
            df = df.drop(columns=columns_to_remove, errors="ignore")
            print(f"Removed columns: {columns_to_remove}")

        # 3. Rename the specified columns
        if columns_to_rename:
            df = df.rename(columns=columns_to_rename)
            print("Renamed columns based on your mapping.")

        # 4. Map Agriculteur Data
        if agriculteur_xlsx and os.path.exists(agriculteur_xlsx):
            agr_df = pd.read_excel(agriculteur_xlsx, usecols=["CodeClient", "npagr"])
            agr_map = dict(zip(agr_df["CodeClient"], agr_df["npagr"]))
            code_client_col = columns_to_rename.get("CodeClient", "CodeClient")
            df["Full Name"] = df[code_client_col].map(agr_map)
            print("Added 'Full Name' column from AGRICULTEUR.xlsx.")
        elif agriculteur_xlsx:
            print(
                f"Warning: AGRICULTEUR file '{agriculteur_xlsx}' not found. Skipping 'full name' column."
            )

        # 5. Reorder Columns
        cols = list(df.columns)

        # A. Existing logic: Put 'Full Name' right after 'Code Parcelle'
        if "Code Parcelle" in cols and "Full Name" in cols:
            cols.remove("Full Name")
            code_parcelle_idx = cols.index("Code Parcelle")
            cols.insert(code_parcelle_idx + 1, "Full Name")

        # B. New logic: Move 'Secondaire' and 'Tertiaire' to the front
        # Safely check which of these columns actually exist in the file
        front_cols = [c for c in ["Secondaire", "Tertiaire"] if c in cols]

        # Remove them from their current positions in the list
        for c in front_cols:
            cols.remove(c)

        # Combine the front columns with the rest of the columns
        cols = front_cols + cols

        # C. Apply the new order to the DataFrame
        df = df[cols]

        # Convert and save to CSV
        df.to_csv(output_csv, index=False)

        print(f"Success! File converted and saved as '{output_csv}'.")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    # 1. Update these file paths to match your actual files
    input_file = "MV1.xlsx"
    output_file = "MV1.csv"

    # 2. Add the exact names of the columns you want to remove inside this list
    cols_to_drop = [
        "N°",
        "AGR",
        "CDA",
        "numtrd",
        "typem",
        "Trimestre",
        "Annee",
        "detreg",
        "modul",
        "ord",
        "rep",
        "RefR",
        "codepar",
        "heureo2",
        "heuref2",
    ]

    # 3. Add the columns you want to rename here
    cols_to_rename = {
        "mleagr": "Matricule",
        "CodeClient": "Code Client",
        "CodeParcelle": "Code Parcelle",
        "refsec": "Secondaire",
        "refter": "Tertiaire",
        "dur": "Durée",
        "dato2": "Date départ",
        "heureo2": "Heure départ",  # You can move this to cols_to_drop if you no longer need it as a standalone column!
        "datf2": "Date Fin",
        "heuref2": "Heure Fin",  # Same here, drop if redundant now.
        "debit": "Débit",
        "niveau": "Niveau",
        "OrdreTaxa": "Ordre Taxa",
    }

    # 4. Specify the path to the 'Agriculteur.xlsx' file if needed
    agriculteur_file = "AGRICULTEUR.xlsx"

    # Run the function
    xlsx_to_csv_remove_and_rename_columns(
        input_file, output_file, cols_to_drop, cols_to_rename, agriculteur_file
    )
