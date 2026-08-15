import pandas as pd
import logging
import sys
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("pipeline.log"),
        logging.StreamHandler()
    ]
)

#1,Load the CSV file
def load_csv(file_path):
    logging.info(f"Loading CSV file from {file_path}...")
    try:
        df=pd.read_csv(file_path)
        logging.info(f"file {file_path} successfully loaded with {len(df)} rows")
        return df
    except FileNotFoundError:
        logging.error(f"Load Error: This file {file_path} not found.")
        return None
    except Exception as e:
        logging.error(f"Load Error: An unexpected error occurred while loading the file: {e}")
        return None

# 2. CLEAN
def clean_data(df):
    logging.info(
        f"CLEAN START: Starting with {len(df)} rows"
    )
    df_clean=df.copy()

    df_clean=df_clean.dropna(subset=['title'])
    df_clean['country']=df_clean['country'].fillna('Unknown')
    df_clean['date_added']=df_clean['date_added'].fillna('Not Available')
    logging.info(
        f"CLEAN END: Finished with {len(df_clean)} rows"
    )
    return df_clean

# 3. ANALYZE / TRANSFORM
def analyze_data(df):
    logging.info(f"Analysis start with {len(df)} rows")

    movies_after_2015=df[(df['type']=='Movie') & (df['release_year']>2015)].copy()
    logging.info(
        f"Movies after 2015: {len(movies_after_2015)}"
    )
     # Movies vs TV Shows
    logging.info("Calculating Movies vs TV Shows")

    content_type = df["type"].value_counts()

    # Top countries
    logging.info("Calculating top 5 countries")

    top_countries = (
        df["country"]
        .value_counts()
        .head(5)
    )

    # Content by release year
    logging.info("Calculating content by release year")

    content_by_year = (
        df["release_year"]
        .value_counts()
        .sort_index(ascending=False)
        .head(10)
    )

    logging.info(
        f"TRANSFORM END: Analysis completed"
    )

    return {
        "movies_after_2015": movies_after_2015,
        "content_type": content_type,
        "top_countries": top_countries,
        "content_by_year": content_by_year
    }

# 4. EXPORT

def export(df,analysis):
    logging.info(
        f"EXPORT START: Preparing to export {len(df)} rows"
    )
     # Validate before exporting
    if len(df) == 0:

        logging.warning(
            "EXPORT WARNING: Cleaned DataFrame has 0 rows. "
            "No files will be written."
        )

        return

    # Output folder
    output_dir = Path.cwd()

    # Save cleaned data
    clean_file = output_dir / "clean_netflix.csv"
  

    try:
        df.to_csv(clean_file,index=False
                  )
        logging.info(f"Cleaned data exported to {clean_file}")

          # Summary report
        summary_file = output_dir / "netflix_summary.txt"

        with open(
            summary_file,
            "w",
            encoding="utf-8"
        ) as f:

            f.write("NETFLIX DATA CLEANING REPORT\n")
            f.write("=" * 40 + "\n")

            f.write(
                f"Total rows loaded: {len(df)}\n"
            )

            f.write(
                f"Rows after cleaning: {len(df)}\n"
            )

            f.write(
                f"Movies after 2015: "
                f"{len(analysis['movies_after_2015'])}\n"
            )

            f.write(
                f"TV Shows: "
                f"{analysis['content_type'].get('TV Show', 0)}\n"
            )

            f.write(
                f"Movies: "
                f"{analysis['content_type'].get('Movie', 0)}\n"
            )

            f.write("\nTop 5 Countries:\n")
            f.write(
                analysis["top_countries"].to_string()
            )

            f.write("\n\nContent by Release Year:\n")
            f.write(
                analysis["content_by_year"].to_string()
            )

        logging.info(
            f"Saved summary report to {summary_file}"
        )

        logging.info(
            f"EXPORT END: Successfully exported {len(df)} rows"
        )

    except Exception as e:
        logging.error(
            f"EXPORT ERROR: An unexpected error occurred while exporting: {e}"
        )


#Main

if __name__== "__main__":
    logging.info("========== PIPELINE START ==========")

    file_path=sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\Lenovo\Desktop\data-engineering-journey\week1-day3\netflix_titles.csv"
    df=load_csv(file_path)

    if df is None:

        logging.error(
            "PIPELINE STOPPED: Data could not be loaded."
        )

        sys.exit(1)
     # --------------------------------------------------------
    # CLEAN
    # --------------------------------------------------------

    df_clean = clean_data(df)

    # --------------------------------------------------------
    # ANALYZE
    # --------------------------------------------------------

    analysis = analyze_data(df_clean)

    # --------------------------------------------------------
    # EXPORT
    # --------------------------------------------------------

    export(
        df_clean,
        analysis
    )

    logging.info("========== PIPELINE END ==========")
