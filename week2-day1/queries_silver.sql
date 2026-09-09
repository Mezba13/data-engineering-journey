-- 1. Top 5 countries by movie count
SELECT country, COUNT(*) as cnt
FROM raw_netflix
WHERE type = 'Movie' AND country != 'Unknown'
GROUP BY country
ORDER BY cnt DESC
LIMIT 5;

-- 2. Content added per year
SELECT SUBSTRING(date_added FROM '([0-9]{4})') as year_added, COUNT(*)
FROM raw_netflix
WHERE date_added IS NOT NULL AND date_added != 'Unknown'
GROUP BY year_added
ORDER BY year_added;

-- 3. Average movie duration by rating
SELECT rating, ROUND(AVG(CAST(SPLIT_PART(duration, ' ', 1) AS INTEGER)), 1) as avg_minutes
FROM raw_netflix
WHERE type = 'Movie' AND duration LIKE '%min%'
GROUP BY rating
HAVING COUNT(*) > 10
ORDER BY avg_minutes DESC;