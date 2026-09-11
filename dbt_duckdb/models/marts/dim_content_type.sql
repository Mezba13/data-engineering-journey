SELECT DISTINCT
    type as content_type,
    CASE 
        WHEN type = 'Movie' THEN 'Film Content'
        ELSE 'Series Content'
    END as content_category
FROM {{ ref('stg_netflix') }}