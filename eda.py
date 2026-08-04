import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data.csv")

print(df.head())

print("\nSummary Statistics")
print(df.describe())

print("\nCorrelation Matrix")
print(df.corr(numeric_only=True))

numeric = df.select_dtypes(include="number")

numeric.hist(figsize=(10,8))
plt.tight_layout()
plt.show()

corr = numeric.corr()

plt.figure(figsize=(8,6))
plt.imshow(corr, cmap="coolwarm")
plt.colorbar()

plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
plt.yticks(range(len(corr.columns)), corr.columns)

plt.title("Correlation Heatmap")

plt.show()