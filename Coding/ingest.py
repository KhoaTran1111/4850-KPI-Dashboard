import os
import pandas as pd

# Define input directory
INPUT_DATA = "./Data Files"

def load_mes_data():
    # Load MES_EQP Operation Rate Raw Data
    file_path = os.path.join(INPUT_DATA, "1_MES_EQP Operation Rate Raw Data.xlsx")
    xls = pd.ExcelFile(file_path)
    dfs = {sheet: pd.read_excel(file_path, sheet_name=sheet) for sheet in xls.sheet_names}
    return dfs

def load_sap_production():
    # Load SAP Production Volume Raw Data + PV
    file_path = os.path.join(INPUT_DATA, "2_SAP_Prodution Volume Raw Data+PV.xlsx")
    rd_df = pd.read_excel(file_path, sheet_name="2) SAP RD (0801)")
    
    # Define Qcells grade
    rd_df['Product_Status'] = rd_df['Qgrade'].apply(
        lambda x: 'Good' if x in ['G01', 'G02'] else ('Defect' if x == 'C Grade' else 'Other')
    )
    return rd_df
