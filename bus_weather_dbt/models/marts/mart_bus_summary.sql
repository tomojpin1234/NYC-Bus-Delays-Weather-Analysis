-- models/marts/mart_bus_summary.sql

WITH estimated AS (
  SELECT    
    FORMAT_DATE('%Y-%m', date) AS month,
    Boro,
    -- Estimate numeric delay
    CASE
      WHEN How_Long_Delayed LIKE '1-15%' THEN 8
      WHEN How_Long_Delayed LIKE '16-30%' THEN 23
      WHEN How_Long_Delayed LIKE '31-45%' THEN 38
      WHEN How_Long_Delayed LIKE '46-60%' THEN 53
      WHEN How_Long_Delayed LIKE 'Over 60%' THEN 75
      ELSE NULL
    END AS delay_minutes,
    CAST(Number_Of_Students_On_The_Bus AS INT64) AS students,
    temperature_2m_max
  FROM {{ ref('stg_bus_weather_raw') }}
)

SELECT
  month,
  Boro,
  COUNT(*) AS total_incidents,
  AVG(students) AS avg_students,
  AVG(delay_minutes) AS avg_estimated_delay,
  AVG(temperature_2m_max) AS avg_temp
FROM estimated
WHERE Boro IS NOT NULL AND TRIM(Boro) != ''
GROUP BY month, Boro
ORDER BY month, Boro