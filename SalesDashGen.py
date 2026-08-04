import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("sales.csv")

print("Total Sales:", df["Sales"].sum())
print("Average Sale:", df["Sales"].mean())
print("Highest Sale:", df["Sales"].max())

sales_by_region = df.groupby("Region")["Sales"].sum()

plt.figure(figsize=(8,5))
sales_by_region.plot(kind="bar")
plt.title("Sales by Region")
plt.ylabel("Sales")
plt.tight_layout()
plt.show()

sales_by_product = df.groupby("Product")["Sales"].sum()

plt.figure(figsize=(6,6))
sales_by_product.plot(kind="pie", autopct="%1.1f%%")
plt.ylabel("")
plt.title("Sales by Product")
plt.show()