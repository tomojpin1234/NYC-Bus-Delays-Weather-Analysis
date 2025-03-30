-- models/marts/mart_boro_delay_status.sql

SELECT
  Boro,
  CASE
    WHEN How_Long_Delayed IS NULL OR TRIM(How_Long_Delayed) = '' THEN 'No Delay'
    ELSE 'Delayed'
  END AS delay_status,
  COUNT(*) AS num_trips
FROM {{ ref('stg_bus_weather_raw') }}
WHERE Boro IS NOT NULL AND TRIM(Boro) != ''
GROUP BY Boro, delay_status