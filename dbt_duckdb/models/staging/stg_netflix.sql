SELECT
    show_id,
    title,
    type,
    director,
    "cast" as cast_members,
    country,
    date_added,
    release_year,
    rating,
    duration,
    listed_in,
    description
FROM {{ source('netflix', 'raw_netflix') }}