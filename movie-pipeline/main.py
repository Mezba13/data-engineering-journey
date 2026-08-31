import sys
from pathlib import Path

sys.path.insert(0,str(Path(__file__).parent/"src"))

from extract import load_csv_to_postgres, verify
from transform import read_bronze, clean_data, load_silver, validate_silver
from dimensions import build_dimensions
from facts import build_fact_table, verify_star_schema


CSV_PATH = r"C:\Users\Lenovo\Desktop\data-engineering-journey\netflix_titles.csv"

def run_pipeline():
    #Bronze
    load_csv_to_postgres(CSV_PATH)
    verify()



    #Silver

    df=read_bronze()
    df_clean=clean_data(df)
    load_silver(df_clean)
    validate_silver()


    #Gold

    build_dimensions()
    build_fact_table()
    verify_star_schema()


if __name__ == "__main__":
    run_pipeline()


