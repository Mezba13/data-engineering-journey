import pandas as pd
from sqlalchemy import create_engine, text

engine=create_engine("postgresql://postgres:admin@localhost:5432/netflix_db")

def build_fact_table():
    df=pd.read_sql_query("SELECT * FROM clean_silver",engine)

    with engine.connect() as conn:
        # Create the fact table
        conn.execute(text("DROP TABLE IF EXISTS fact_titles"))
        conn.execute(text(""" CREATE TABLE fact_titles (
            fact_id SERIAL PRIMARY KEY,
            show_id VARCHAR(50),
            title text,
            type_id INTEGER,
            country_id INTEGER,
            date_id INTEGER,
            release_year INTEGER,
            duration_value INTEGER,
            rating VARCHAR(50)
            )"""))

        # Map the foreign keys
        dim_types=pd.read_sql_query("SELECT * FROM dim_type",conn)
        dim_countries=pd.read_sql_query("SELECT * FROM dim_country",conn)
        dim_dates=pd.read_sql_query("SELECT * FROM dim_date",conn)

        fact=df.copy()

        fact=fact.merge(dim_types,left_on='type',right_on='type_name',how='left')

        fact['primary_country']=fact['country'].str.split(",").str[0].str.strip()
        fact=fact.merge(dim_countries,left_on='primary_country',right_on='country_name',how='left')
        fact=fact.merge(dim_dates,left_on='year_added',right_on='year_added',how='left')

        fact_table = fact[[
            "show_id", "title", "type_id", "country_id", "date_id",
            "release_year", "duration_value", "rating"
        ]].copy()
 
        fact_table.to_sql('fact_titles',conn,index=False,if_exists='append',chunksize=1000)

        conn.commit()

def verify_star_schema():
    with engine.connect() as conn:
         for table in ["dim_type", "dim_country", "dim_date", "fact_titles"]:
            count = conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
            print(f"{table}: {count}")

if __name__ == "__main__":
    build_fact_table()
    verify_star_schema()