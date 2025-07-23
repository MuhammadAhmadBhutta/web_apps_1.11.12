import pandas as pd
import os

def load_data():
    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, "Sample_Superstore.xlsx")
    df = pd.read_excel(file_path, sheet_name="Orders")
    return df
