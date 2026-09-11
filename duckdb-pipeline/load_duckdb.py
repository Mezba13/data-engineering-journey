import duckdb


CSV_PATH = r"C:\Users\Lenovo\Desktop\data-engineering-journey\netflix_titles.csv"
DB_PATH = r"C:\Users\Lenovo\Desktop\data-engineering-journey\duckdb-pipeline\netflix.duckdb"
def load():
    conn=duckdb.connect(DB_PATH)

    conn.execute(f"""
    create or replace table raw_netflix as
    select * from read_csv_auto('{CSV_PATH}')
    """)

    count=conn.execute("select count(*) from raw_netflix").fetchone()[0]
    print(f"Loaded {count} records into raw_netflix table.")

    result=conn.execute("""
    select type,count(*) as type_count
    from raw_netflix
    group by type
    """).fetchall()

    for row in result:
        print(f"{row[0]}: {row[1]}")

    schema=conn.execute("describe raw_netflix").fetchall()

    for column in schema:
        print(f"{column[0]}: {column[1]}")

    conn.close()


if __name__=="__main__":
    load()
