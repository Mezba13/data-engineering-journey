{%snapshot snapshot_netflix_ratings%}

{{
    config(
        target_database='netflix_db',
        target_schema='snapshots',
        unique_key='show_id',
        strategy='check',
        check_cols=['rating','duration','listed_in'],
    )

}}
    SELECT * FROM {{ source('netflix_pipeline', 'clean_silver')}}

{%endsnapshot%}