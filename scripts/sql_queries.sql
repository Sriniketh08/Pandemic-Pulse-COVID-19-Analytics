
-- DuckDB / SQL examples for analysis

-- 1) Latest snapshot per country
WITH latest AS (
  SELECT *
  FROM read_csv_auto('data/owid-covid-data.csv')
  WHERE continent IS NOT NULL
  QUALIFY ROW_NUMBER() OVER (PARTITION BY location ORDER BY date DESC) = 1
)
SELECT location, total_cases, total_deaths, people_fully_vaccinated
FROM latest
ORDER BY total_cases DESC
LIMIT 20;

-- 2) Cases and deaths time series for a country
SELECT date, total_cases, total_deaths
FROM read_csv_auto('data/owid-covid-data.csv')
WHERE location = 'India'
ORDER BY date;

-- 3) Vaccination progress vs cases
WITH latest AS (
  SELECT *
  FROM read_csv_auto('data/owid-covid-data.csv')
  WHERE continent IS NOT NULL
  QUALIFY ROW_NUMBER() OVER (PARTITION BY location ORDER BY date DESC) = 1
)
SELECT location,
       people_fully_vaccinated,
       total_cases
FROM latest
ORDER BY people_fully_vaccinated DESC
LIMIT 20;
