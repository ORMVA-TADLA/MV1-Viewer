import pandas as pd
import os


def xlsx_to_csv_remove_and_rename_columns(
    input_xlsx, output_csv, columns_to_remove, columns_to_rename
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

        # 1. Remove the specified columns
        # errors='ignore' prevents the script from crashing if you type a column
        # name that doesn't actually exist in the file.
        if columns_to_remove:
            df = df.drop(columns=columns_to_remove, errors="ignore")
            print(f"Removed columns: {columns_to_remove}")

        # 2. Rename the specified columns
        if columns_to_rename:
            df = df.rename(columns=columns_to_rename)
            print("Renamed columns based on your mapping.")

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
    # Make sure the spelling and capitalization match your Excel file exactly!
    cols_to_drop = [
        "N°",
        "AGR",
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
    ]

    # 3. Add the columns you want to rename here
    # Use the format: {"Old_Name": "New_Name"}
    cols_to_rename = {
        "mleagr": "Matricule",
        "CodeClient": "Code Client",
        "CodeParcelle": "Code Parcelle",
        "refsec": "Secondaire",
        "refter": "Tertiaire",
        "dur": "Durée",
        "dato2": "Date départ",
        "heureo2": "Heure départ",
        "datf2": "Date Fin",
        "heuref2": "Heure Fin",
        "debit": "Débit",
        "niveau": "Niveau",
        "OrdreTaxa": "Ordre Taxa",
    }

    # Run the function with both lists
    xlsx_to_csv_remove_and_rename_columns(
        input_file, output_file, cols_to_drop, cols_to_rename
    )
