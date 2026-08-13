import pandas as pd

df=pd.read_csv(r"C:\\Users\\Lenovo\\Desktop\\data-engineering-journey\\week1-day4\\clean_netflix.csv")

# print(df.head())

# group=df.groupby(['country','type'])
# country_type_counts=group.size()


# top_10=country_type_counts.sort_values(ascending=False).head(10)
# print(top_10)

# genre_counts=df['listed_in'].str.split(',').explode().value_counts()
# print(genre_counts.head(10))

# movies=df[df['type']=='Movie']
df['duration']=df['duration'].str.replace(' min','')
df['duration']=df['duration'].str.extract(r'(\d+)').astype(float)
# # print(df[df['duration'] < 10])

rating_group=df.groupby('rating')
avg_duration_by_rating = rating_group['duration'].mean().sort_values(ascending=False)
print(avg_duration_by_rating)
# print(df['duration'].value_counts().head(10))
# print(df["duration"].head(10))
# Fix rows where duration was incorrectly placed in rating
print(df.columns)
mask = df["rating"].str.contains("min", na=False)

df.loc[mask, "duration"] = (
    df.loc[mask, "rating"]
    .str.extract(r"(\d+)", expand=False)
    .astype(float)
)

df.loc[mask, "rating"] = pd.NA

# Make sure all duration values are numeric
df["duration"] = (
    df["duration"]
    .astype("string")
    .str.extract(r"(\d+)", expand=False)
    .astype(float)
)
rating_lookup = pd.DataFrame({
    "rating": ["PG", "R", "PG-13", "G", "NC-17", "TV-MA"],
    "rating description": [
        "Parental Guidance",
        "Restricted",
        "Parents Strongly Cautioned",
        "General Audience",
        "Adults Only",
        "Mature Audience"
    ]
})

df_merged = df.merge(
    rating_lookup,
    on="rating",
    how="left"
)

print(df_merged[["title", "rating", "description"]].head(5))


pivot = pd.pivot_table(
    df,
    index="type",
    columns="rating",
    values="title",
    aggfunc="count",
    fill_value=0
)

print(pivot)