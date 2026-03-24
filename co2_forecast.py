import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import sqlite3
from sklearn.linear_model import LinearRegression

# === โหลดข้อมูลจาก database ===
conn = sqlite3.connect('co2_emissions.db')
df = pd.read_sql_query("SELECT * FROM emissions", conn)
conn.close()

# === Global CO2 รายปี ===
global_co2 = df.groupby('year')['co2'].sum().reset_index()
global_co2.columns = ['year', 'total_co2']

# === Train Model ===
X = global_co2['year'].values.reshape(-1, 1)
y = global_co2['total_co2'].values

model = LinearRegression()
model.fit(X, y)


future_years = np.arange(2025, 2045).reshape(-1, 1)
predictions = model.predict(future_years)

future_df = pd.DataFrame({
    'year': future_years.flatten(),
    'predicted_co2': predictions.round(2)
})

print("=== Predicted Global CO2 (2025–2044) ===")
print(future_df)

# === Plot ===
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(global_co2['year'], global_co2['total_co2'],
        color='steelblue', linewidth=2, label='Historical')
ax.plot(future_df['year'], future_df['predicted_co2'],
        color='crimson', linewidth=2, linestyle='--', label='Predicted')
ax.axvline(x=2024, color='gray', linestyle=':', linewidth=1)
ax.set_xlabel('Year')
ax.set_ylabel('CO2 (million tonnes)')
ax.set_title('Global CO2 Emissions: Historical + 20-Year Forecast')
ax.legend()
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
plt.tight_layout()
plt.show()