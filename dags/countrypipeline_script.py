import requests
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
import mysql.connector

# Extraction
def extract_countries_data():
    url = "https://restcountries.com/v3.1/all?fields=name,area,population,region,capital,continent"
    response = requests.get(url)
    if response.status_code == 200:
        countries = response.json()
        print("Sample JSON (first country):", countries[0])  # Debug JSON
    else:
        raise Exception(f"API request failed with status {response.status_code}")
    return pd.json_normalize(countries)

# Load
load_dotenv("C:/Users/hp/Documents/Countries Worldwide Info/.env")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = "127.0.0.1:3307"  # Hardcode temporarily
def load_to_mysql(df):
    try:
        print("Starting load_to_mysql...")
        df.to_csv(r"C:\Users\hp\Documents\Countries Worldwide Info\cleaned_countriesdata.csv", index=False)
        print("CSV saved successfully.")
        conn = mysql.connector.connect(
            host="127.0.0.1",
            port=3307,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )
        cursor = conn.cursor()
        print("MySQL connector connection successful.")

        # Drop table if exists
        cursor.execute("DROP TABLE IF EXISTS cleancountries")

        # Create table
        create_table_query = """
        CREATE TABLE cleancountries (
            Country VARCHAR(255),
            Continent VARCHAR(255),
            Area FLOAT,
            Population BIGINT,
            `Capital City` VARCHAR(255)
        )
        """
        cursor.execute(create_table_query)
        print("Table cleancountries created.")

        # Insert data
        insert_query = """
        INSERT INTO cleancountries (Country, Continent, Area, Population, `Capital City`)
        VALUES (%s, %s, %s, %s, %s)
        """
        for _, row in df.iterrows():
            values = (
                row['Country'],
                row['Continent'],
                row['Area'],
                row['Population'],
                row['Capital City'] if pd.notnull(row['Capital City']) else None
            )
            cursor.execute(insert_query, values)
        conn.commit()
        print("✅ Data successfully uploaded to MySQL.")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error loading data to MySQL: {e}")
        raise

# Run pipeline
def run_pipeline():
    print("Starting pipeline...")
    df = extract_countries_data()
    print("Raw DataFrame columns:", df.columns.tolist())
    df['capital'] = df['capital'].apply(lambda x: x[0] if isinstance(x, list) and x else None)
    try:
        df = df[['name.common', 'region', 'area', 'population', 'capital']]
    except KeyError as e:
        print(f"Column selection failed: {e}")
        raise
    
    df.dropna(inplace=True)
    df = df[(df['area'] > 0) & (df['population'] > 0)]
    df.columns = ['Country', 'Continent', 'Area', 'Population', 'Capital City']
    print("Transformed DataFrame:\n", df.head())
    print("Pipeline data processed:", df.shape)
    df.to_csv(r"C:\Users\hp\Documents\Countries Worldwide Info\cleaned_countriesdata.csv", index=False)
    load_to_mysql(df)

if __name__ == "__main__":
    run_pipeline()

