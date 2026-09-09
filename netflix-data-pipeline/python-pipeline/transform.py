import pandas as pd
from sqlalchemy import create_engine

engine= create_engine("postgresql://postgres:admin@localhost:5432/netflix_db")

def read_bronze():
    """Reading raw and unprocessed data from the bronze layer"""
    df=pd.read_sql_query("SELECT * FROM netflix",engine)
    return df

def clean_data(df):
    """Cleaning the data by removing duplicates and handling missing values"""
    clean=df.copy()

    clean=clean.dropna(subset=['title'])
    print(f"Rows removed due to null titles: {len(df)-len(clean)}")

    text_cols=['director','cast','country','rating']
    for col in text_cols:
        clean[col]=clean[col].fillna('Unknown')

    clean['date_added']=pd.to_datetime(clean['date_added'],errors='coerce')
    clean['year_added']=clean['date_added'].dt.year

    clean['release_year']=pd.to_numeric(clean['release_year'],errors='coerce')

    duration_split=clean['duration'].str.split(" ",n=1,expand=True)
    clean['duration_value']=pd.to_numeric(duration_split[0],errors='coerce')
    clean['duration_unit']=duration_split[1]

    before=len(clean)
    clean=clean.drop_duplicates(subset=["title","type"], keep='first')
    after=len(clean)
    print(f"Rows removed due to duplicates: {before - after}")

    return clean


def load_silver(df):

    df.head(0).to_sql('clean_silver',engine,index=False, if_exists='replace')

    df.to_sql('clean_silver',engine, if_exists='append', index=False,chunksize=1000)


def validate_silver():
    count=pd.read_sql_query("SELECT COUNT(*) FROM clean_silver",engine)
    print(f"The silver table has {count.iloc[0,0]} rows")

    null_titles=pd.read_sql_query("SELECT COUNT(*) FROM clean_silver WHERE title IS NULL",engine)
    print(f"The silver table has {null_titles.iloc[0,0]} rows with null titles")

    result=pd.read_sql_query("SELECT title, type, year_added, duration_value, rating  FROM clean_silver LIMIT 5",engine)

    for row in result.itertuples(index=False):
        print(f"{row.title} | {row.type} | {row.year_added} | {row.duration_value} | {row.rating}")


if __name__=="__main__":
    df=read_bronze()
    clean_df=clean_data(df)
    load_silver(clean_df)
    validate_silver()


    
