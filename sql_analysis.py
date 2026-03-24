import sqlite3
import pandas as pd

conn = sqlite3.connect('co2_emissions.db')

# Top 10 ประเทศที่ปล่อย CO2 สูงสุดในปี 2024 
q1 = pd.read_sql_query("""
    SELECT country, ROUND(co2, 2) AS co2_million_tonnes
    FROM emissions
    WHERE year = 2024
    ORDER BY co2 DESC
    LIMIT 10
""", conn)
print("=== Q1: Top 10 Emitters (2024) ===")
print(q1)

# ประเทศที่ปล่อย CO2 สะสมสูงสุดตลอด 1950-2024
q2 = pd.read_sql_query("""
    SELECT country, ROUND(SUM(co2), 2) AS total_co2
    FROM emissions
    GROUP BY country
    ORDER BY total_co2 DESC
    LIMIT 10
""", conn)
print("\n=== Q2: Top 10 ประเทศ CO2 สะสม (1950–2024) ===")
print(q2)

# ทศวรรษที่โลกปล่อย CO2 เพิ่มเร็วที่สุด (1950-2024)
q3 = pd.read_sql_query("""
    SELECT (year / 10) * 10 AS decade,
           ROUND(SUM(co2), 2) AS total_co2
    FROM emissions
    GROUP BY decade
    ORDER BY decade
""", conn)
print("\n=== Q3: CO2 รายทศวรรษ ===")
print(q3)

# ประเทศที่ลด CO2 ได้มากที่สุดในช่วง 10 ปีล่าสุด (2014-2024)
q4 = pd.read_sql_query("""
    SELECT country,
           ROUND(MAX(CASE WHEN year = 2014 THEN co2 END), 2) AS co2_2014,
           ROUND(MAX(CASE WHEN year = 2024 THEN co2 END), 2) AS co2_2024,
           ROUND(MAX(CASE WHEN year = 2024 THEN co2 END) - 
                 MAX(CASE WHEN year = 2014 THEN co2 END), 2) AS change
    FROM emissions
    WHERE year IN (2014, 2024)
    GROUP BY country
    HAVING co2_2014 IS NOT NULL AND co2_2024 IS NOT NULL
    ORDER BY change ASC
    LIMIT 10
""", conn)
print("\n=== Q4: ประเทศที่ลด CO2 มากที่สุด (2014→2024) ===")
print(q4)

conn.close()