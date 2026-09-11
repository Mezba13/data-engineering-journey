SELECT
    show_id,
    title,
    type,
    country,
    release_year,
    rating,
    TRY_CAST(SPLIT_PART(duration, ' ', 1) AS INTEGER) as duration_minutes
FROM {{ ref('stg_netflix') }}