import pandas as pd
from sqlalchemy import create_engine, text

engine=create_engine("postgresql://postgres:admin@localhost:5432/netflix_db")

def build_dimensions():
    df=pd.read_sql_query("SELECT * FROM clean_silver",engine)

    with engine.connect() as conn:
        # Create the dimension tables
        conn.execute(text("DROP TABLE IF EXISTS dim_type"))
        conn.execute(text(""" CREATE TABLE dim_type (
            type_id SERIAL PRIMARY KEY,
            type_name VARCHAR(50) NOT NULL UNIQUE
            )"""))

        types=df[['type']].drop_duplicates().reset_index(drop=True)
        types.columns=['type_name']
        types.to_sql('dim_type',conn,index=False,if_exists='append')

        #Dim-Country:Use 1st Country.
        conn.execute(text("DROP TABLE IF EXISTS dim_country"))
        conn.execute(text(""" CREATE TABLE dim_country (
            country_id SERIAL PRIMARY KEY,
            country_name VARCHAR(100) NOT NULL UNIQUE
            )"""))

        countries=df["country"].str.split(",").str[0].str.strip()
        countries=countries.drop_duplicates().sort_values()
        countries=pd.DataFrame(countries)
        countries.columns=['country_name']
        countries=countries[countries['country_name'] != 'Unknown']
        countries.to_sql('dim_country',conn,index=False,if_exists='append')

        
        #dim-date:
        conn.execute(text("DROP TABLE IF EXISTS dim_date"))
        conn.execute(text(""" CREATE TABLE dim_date (
            date_id SERIAL PRIMARY KEY,
            year_added INTEGER NOT NULL UNIQUE
            )"""))
        dates=df[['year_added']].dropna().drop_duplicates().sort_values("year_added")
        dates.columns=['year_added']
        dates["year_added"]=dates["year_added"].astype(int)
        dates.to_sql('dim_date',conn,index=False,if_exists='append')

        conn.commit()


if __name__=="__main__":
    build_dimensions()