
import os
import pandas as pd
import urllib.parse
from sqlalchemy import create_engine, text

# 1. Read the Excel file
df = pd.read_excel(
    "input_files/3_SAP_Material Consumption Raw Data.XLSX"
)

# 2. Remove duplicate rows
df = df.drop_duplicates()

# 3. Drop unnecessary columns
df = df.drop(
    columns=[
        "Purchase order",
        "Bill of Lading",
        "Supplier",
        "Order",
        "Cost Center"
    ],
    errors="ignore"
)

print("Cleaned data:")
print(df)

# 4. Azure SQL Server connection settings
server = "qcells-team3.database.windows.net"
database = os.getenv("AZURE_SQL_DATABASE")
username = "team3"
password = os.getenv("AZURE_SQL_PASSWORD")

if not database or not password:
    raise ValueError(
        "Set AZURE_SQL_DATABASE and AZURE_SQL_PASSWORD "
        "environment variables before running."
    )

# 5. Build the SQL Server connection
connection_string = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    f"SERVER=tcp:{server},1433;"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password};"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

params = urllib.parse.quote_plus(connection_string)

engine = create_engine(
    f"mssql+pyodbc:///?odbc_connect={params}"
)

# 6. Test the connection and upload the data
try:
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT DB_NAME()")
        )
        print("Connected to database:", result.scalar())

    df.to_sql(
        name="MaterialConsumption",
        con=engine,
        if_exists="append",
        index=False,
        chunksize=1000,
        method="multi"
    )

    print("Data uploaded successfully!")

except Exception as e:
    print("Database operation failed:", e)

finally:
    engine.dispose()
