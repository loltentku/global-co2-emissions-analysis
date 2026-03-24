import sqlite3
import pandas as pd

conn = sqlite3.connect('co2_emissions.db')

q1 = pd.read_sql_query("""
    SELECT country, ROUND(co2, 2) AS co2_million_tonnes
    FROM emissions WHERE year = 2024
    ORDER BY co2 DESC LIMIT 10
""", conn)

q2 = pd.read_sql_query("""
    SELECT country, ROUND(SUM(co2), 2) AS total_co2
    FROM emissions GROUP BY country
    ORDER BY total_co2 DESC LIMIT 10
""", conn)

q3 = pd.read_sql_query("""
    SELECT (year / 10) * 10 AS decade,
           ROUND(SUM(co2), 2) AS total_co2
    FROM emissions GROUP BY decade ORDER BY decade
""", conn)

q4 = pd.read_sql_query("""
    SELECT country,
           ROUND(MAX(CASE WHEN year = 2014 THEN co2 END), 2) AS co2_2014,
           ROUND(MAX(CASE WHEN year = 2024 THEN co2 END), 2) AS co2_2024,
           ROUND(MAX(CASE WHEN year = 2024 THEN co2 END) -
                 MAX(CASE WHEN year = 2014 THEN co2 END), 2) AS change
    FROM emissions WHERE year IN (2014, 2024)
    GROUP BY country
    HAVING co2_2014 IS NOT NULL AND co2_2024 IS NOT NULL
    ORDER BY change ASC LIMIT 10
""", conn)

conn.close()
