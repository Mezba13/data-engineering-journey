-- fct_title_metrics.sql
SELECT
    show_id,
    title,
    type,
    country,
    release_year,
    year_added,
    duration_value,
    rating,
    (year_added - release_year) as years_before_netflix
FROM {{ ref('stg_netflix') }}