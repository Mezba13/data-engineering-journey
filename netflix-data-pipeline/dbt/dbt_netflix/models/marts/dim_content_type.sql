-- dim_content_type.sql
SELECT DISTINCT
    type as content_type,
    {{content_category('type')}} as content_category
FROM {{ ref('stg_netflix') }}