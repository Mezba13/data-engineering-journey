-- stg_netflix.sql
-- Clean staging model on top of your clean_silver table

SELECT
    show_id,
    title,
    type,
    director,
    "cast" as cast_members,
    country,
    date_added,
    year_added,
    release_year,
    rating,
    duration,
    duration_value,
    duration_unit,
    listed_in,
    description
FROM clean_silver