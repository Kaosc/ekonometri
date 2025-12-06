import pandas as pd
from datetime import datetime, timedelta

df = pd.read_excel("merged.xlsx")

assets = ["BTC", "ETH", "MANA", "DJI", "NQZ25", "SPVIXETR", "XAG", "XAU", "XU100"]

date_cols = {asset: f"{asset} - Date" for asset in assets}
price_cols = {asset: f"{asset} - Price" for asset in assets}

for col in date_cols.values():
    df[col] = pd.to_datetime(df[col], format="%d.%m.%Y", errors="coerce")

rows = []

start = datetime(2025, 12, 6)
end = datetime(2022, 1, 1)

current = start
while current >= end:

    valid = True
    prices_today = []

    for asset in assets:
        match = df[df[date_cols[asset]] == current]

        if match.empty:
            valid = False
            break

        price_value = match[price_cols[asset]].values[0]
        prices_today.append(price_value)

    if valid:
        rows.append([current.strftime("%d.%m.%Y")] + prices_today)

    current -= timedelta(days=1)

header = ["Date"] + [f"{asset} - Price" for asset in assets]
final_df = pd.DataFrame(rows, columns=header)

final_df.to_csv("final_cleaned_assets.csv", index=False, encoding="utf-8-sig")