{% macro content_category(type) %}
    case
        when {{type}}='Movie' then 'Film Content'
        when {{type}}='TV Show' then 'Series Content'
        else 'Unknown'
    end
{% endmacro %}