import pandas as pd

def check_data_quality(file_path):
    df = pd.read_csv(file_path)

    print("=" * 50)
    print("DATA QUALITY REPORT")
    print("=" * 50)

    print("\nRows and Columns:")
    print(df.shape)

    print("\nData Types:")
    print(df.dtypes)

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nDuplicate Rows:")
    print(df.duplicated().sum())

    print("\nSummary Statistics:")
    print(df.describe(include='all'))

    print("\nPotential Outliers (IQR Method):")

    numeric = df.select_dtypes(include='number')

    for col in numeric.columns:
        Q1 = numeric[col].quantile(0.25)
        Q3 = numeric[col].quantile(0.75)
        IQR = Q3 - Q1

        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        outliers = numeric[(numeric[col] < lower) | (numeric[col] > upper)]

        print(f"{col}: {len(outliers)} outliers")

check_data_quality("data.csv")