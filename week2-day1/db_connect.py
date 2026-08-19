import pandas as pd
from sqlalchemy import create_engine

engine=create_engine("postgresql://postgres:admin@localhost:5432/netflix_db")


def load_n_create(csv_path):
    df=pd.read_csv(csv_path)
    df.head(0).to_sql('netflix',engine,index=False, if_exists='replace')

    df.to_sql('netflix',engine, if_exists='append', index=False,chunksize=1000)
    print(df.dtypes)

def verify():
    count=pd.read_sql_query("SELECT COUNT(*) FROM netflix",engine)
    count=count.iloc[0,0]
    print(f"The table has {count} rows")

    result=pd.read_sql_query("SELECT type,count(*) as cnt from netflix group by type",engine)

    for row in result.itertuples(index=False):
        print(f"{row.type} : {row.cnt}")


if __name__=="__main__":
    load_n_create(r"c:\Users\Lenovo\Desktop\data-engineering-journey\netflix_titles.csv")
    verify()
