import pandas as pd

df = pd.read_csv('emission.csv')

#Check data quality
print(df.shape)
print(df.dtypes)
print(df.head())
print(df.isnull().sum())

print("\n=== iso_code ที่เป็น empty string ===")
print(df[df['iso_code'].str.strip() == '']['country'].unique())

print("\n=== Missing Values (%) ===")
missing_pct = (df.isnull().sum() / len(df) * 100).round(2)
print(missing_pct)

print("\n=== จำนวนประเทศ และช่วงปี ===")
print(f"จำนวนประเทศ: {df['country'].nunique()}")
print(f"ปี: {df['year'].min()} - {df['year'].max()}")

df = df.drop(columns=['consumption_co2'])
df = df.dropna(subset=['co2'])
fill_cols = ['coal_co2', 'oil_co2', 'gas_co2', 'cement_co2']
df[fill_cols] = df[fill_cols].fillna(0)

#Check cleaned data
print("=== หลัง Clean ===")
print(f"Shape: {df.shape}")
print(df.isnull().sum())
print(df.head())

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# Top 10 ประเทศที่ปล่อย CO2 สูงสุด (ปี 2024)
top10 = (df[df['year'] == 2024]
         .nlargest(10, 'co2')[['country', 'co2']]
         .reset_index(drop=True))

print("=== Top 10 Emitters (2024) ===")
print(top10)

fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(top10['country'][::-1], top10['co2'][::-1], color='steelblue')
ax.set_xlabel('CO2 (million tonnes)')
ax.set_title('Top 10 CO2 Emitters in 2024')
plt.tight_layout()
plt.show()

#เส้นแนวโน้ม (trend) ของการปล่อย CO₂ ทั่วโลกตามเวลา
global_trend = df.groupby('year')['co2'].sum().reset_index()

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(global_trend['year'], global_trend['co2'], color='crimson', linewidth=2)
ax.set_xlabel('Year')
ax.set_ylabel('CO2 (million tonnes)')
ax.set_title('Global CO2 Emissions 1950–2024')
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
plt.tight_layout()
plt.show()

#เปรียบเทียบ Top 5 ประเทศตลอด 1950-2024 
top5_countries = (df[df['year'] == 2024]
                  .nlargest(5, 'co2')['country'].tolist())

top5_trend = df[df['country'].isin(top5_countries)]

fig, ax = plt.subplots(figsize=(12, 6))
for country in top5_countries:
    data = top5_trend[top5_trend['country'] == country]
    ax.plot(data['year'], data['co2'], linewidth=2, label=country)

ax.set_xlabel('Year')
ax.set_ylabel('CO2 (million tonnes)')
ax.set_title('CO2 Emissions Trend: Top 5 Countries (1950–2024)')
ax.legend()
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
plt.tight_layout()
plt.show()

#สัดส่วน Energy Source ของโลก (2024)
sources = ['coal_co2', 'oil_co2', 'gas_co2', 'cement_co2']
source_totals = df[df['year'] == 2024][sources].sum()

fig, ax = plt.subplots(figsize=(7, 7))
ax.pie(source_totals, labels=['Coal', 'Oil', 'Gas', 'Cement'],
       autopct='%1.1f%%', startangle=140,
       colors=['#2c3e50', '#e74c3c', '#f39c12', '#95a5a6'])
ax.set_title('Global CO2 by Energy Source (2024)')
plt.tight_layout()
plt.show()
