# netflix_cleaner.py
import pandas as pd
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# --- 1. LOAD ---
logging.info("Loading netflix_titles.csv...")
df = pd.read_csv(r'C:\Users\Lenovo\Desktop\data-engineering-journey\week1-day3\netflix_titles.csv')
logging.info(f"Loaded {len(df)} rows")

# --- 2. EXPLORE ---
print("\n=== First 5 Rows ===")
print(df.head())

print("\n=== Shape ===")
print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")

print("\n=== Missing Values ===")
print(df.isnull().sum())

# --- 3. CLEAN ---
# Drop rows where title is missing
df_clean = df.dropna(subset=['title']).copy()

# Fill missing country with 'Unknown'
df_clean['country'] = df_clean['country'].fillna('Unknown')

# Fill missing date_added with 'Not Available'
df_clean['date_added'] = df_clean['date_added'].fillna('Not Available')

logging.info(f"After cleaning: {len(df_clean)} rows")

# --- 4. TRANSFORM ---
# Filter: Movies released after 2015
movies_after_2015 = df_clean[
    (df_clean['type'] == 'Movie') & 
    (df_clean['release_year'] > 2015)
].copy()

# --- 5. ANALYZE ---
print("\n=== Movies vs TV Shows ===")
print(df_clean['type'].value_counts())

print("\n=== Top 5 Countries ===")
print(df_clean['country'].value_counts().head())

print("\n=== Content by Release Year (Top 10) ===")
print(df_clean['release_year'].value_counts().sort_index(ascending=False).head(10))

# --- 6. EXPORT ---
# Save cleaned data
df_clean.to_csv(r'C:\Users\Lenovo\Desktop\data-engineering-journey\week1-day3\clean_netflix.csv', index=False)

# Save summary report
with open(r'C:\Users\Lenovo\Desktop\data-engineering-journey\week1-day3\netflix_summary.txt', 'w') as f:
    f.write("NETFLIX DATA CLEANING REPORT\n")
    f.write("=" * 40 + "\n")
    f.write(f"Total rows loaded: {len(df)}\n")
    f.write(f"Rows after cleaning: {len(df_clean)}\n")
    f.write(f"Movies after 2015: {len(movies_after_2015)}\n")
    f.write(f"TV Shows: {len(df_clean[df_clean['type'] == 'TV Show'])}\n")
    f.write(f"Movies: {len(df_clean[df_clean['type'] == 'Movie'])}\n")
    f.write("\nTop 5 Countries:\n")
    f.write(df_clean['country'].value_counts().head().to_string())

logging.info("Saved clean_netflix.csv and netflix_summary.txt")
print("\n=== Done! Check your week1-day3 folder ===")