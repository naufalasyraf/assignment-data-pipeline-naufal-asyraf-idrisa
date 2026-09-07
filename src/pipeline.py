import pandas as pd

DATA_PATH = "data/raw/automobileEDA_dirty_training.csv"
PROCESSED_DATA_PATH = "data/processed/automobileEDA_processed.csv"

COLS_TO_CLEAN = [
    "make", "aspiration", "num-of-doors", "body-style",
    "drive-wheels", "engine-location", "engine-type",
    "num-of-cylinders", "fuel-system", "horsepower-binned",
]

COLS_TO_IMPUTE = ["stroke", "horsepower", "price"]

def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df
 
 
def inspect_data(df: pd.DataFrame) -> None:
    print("1. LIMA BARIS PERTAMA DATASET")
    print(df.head())
 
    print("2. JUMLAH BARIS DAN KOLOM")
    j_baris, j_kolom = df.shape
    print(f"Jumlah baris  : {j_baris}")
    print(f"Jumlah kolom  : {j_kolom}\n")
 
    print("3. NAMA SETIAP KOLOM")
    for i, col in enumerate(df.columns, start=1):
        print(f"{i}. {col}")

    print() 

    print("4. TIPE DATA SETIAP KOLOM")
    print(df.dtypes)
    print() 

    print("5. JUMLAH MISSING VALUES PER KOLOM")
    missing = df.isnull().sum()
    missing = missing[missing > 0].sort_values(ascending=False)
    if missing.empty:
        print("Tidak ada missing values yang terdeteksi.")
    else:
        print(missing)

    print() 
 
    print("6. JUMLAH DUPLICATE RECORDS")
    j_duplikat = df.duplicated().sum()
    print(f"Jumlah baris duplikat: {j_duplikat}")
    print() 
    
    print("7. NILAI UNIK PADA KOLOM KATEGORIKAL")
    categorical_cols = df.select_dtypes(include=["object", "str"]).columns
    if len(categorical_cols) == 0:
        print("Tidak ditemukan kolom kategorikal (tipe object).")
    else:
        for col in categorical_cols:
            unique_vals = df[col].unique()
            print(f"\nKolom '{col}' ({df[col].nunique()} nilai unik):")
            print(unique_vals)

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df_original = df.copy()

    shape_before = df.shape
    missing_before = df.isnull().sum()
    missing_before = missing_before[missing_before > 0]
    duplicates_before = df.duplicated().sum()

    print("SEBELUM CLEANING")
    print(f"Jumlah data (baris, kolom): {shape_before}")
    print(f"Total missing values      : {missing_before.sum()}")
    print(f"Jumlah baris duplikat     : {duplicates_before}\n")

    df = df.drop_duplicates()

    for col in COLS_TO_CLEAN:
        if col in df.columns:
            df[col] = df[col].str.strip().str.lower()

    for col in COLS_TO_IMPUTE:
        if col in df.columns and df[col].isnull().any():
            df[col] = df[col].fillna(df[col].median())

    for col in ["num-of-doors", "make"]:
        if col in df.columns and df[col].isnull().any():
            df[col] = df[col].fillna(df[col].mode(dropna=True)[0])

    df["transaction_date"] = pd.to_datetime(
        df["transaction_date"], format="mixed", errors="coerce", dayfirst=True
    )

    noise_mask = (df["price"] <= 0) | (df["horsepower"] <= 0)
    if noise_mask.sum() > 0:
        print(f"Ditemukan {noise_mask.sum()} baris nilai tidak wajar, dihapus.")
        df = df[~noise_mask]

    # if "horsepower-binned" in df.columns:
    #     missing_mask = df["horsepower-binned"].isnull()

    #     df.loc[missing_mask, "horsepower-binned"] = (
    #         df.loc[missing_mask, "horsepower"]
    #         .apply(get_horsepower_bin)
    #     )

    shape_after = df.shape
    missing_after = df.isnull().sum()
    missing_after = missing_after[missing_after > 0]

    print("\nSESUDAH CLEANING")
    print(f"Jumlah data (baris, kolom): {shape_after}")
    print(f"Total missing values      : {missing_after.sum()}")
    print(f"Jumlah baris yang dihapus : {shape_before[0] - shape_after[0]}")

    print("\nKolom yang di cleaning:")
    clean_cols = COLS_TO_CLEAN + COLS_TO_IMPUTE + ["transaction_date"]
    for col in clean_cols:
        if col in df.columns and col in df_original.columns:
            common_idx = df.index.intersection(df_original.index)
            before_vals = df_original.loc[common_idx, col].astype(str)
            after_vals = df.loc[common_idx, col].astype(str)
            if not before_vals.equals(after_vals):
                print(f"- {col}")

    return df

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    min_hp = df["horsepower"].min()
    max_hp = df["horsepower"].max()

    df["horsepower_scaled"] = ((df["horsepower"] - min_hp) / (max_hp - min_hp))

    make_frequency = df["make"].value_counts()
    df["make_freq"] = df["make"].map(make_frequency)

    one_hot_columns = [
        "body-style",
        "drive-wheels",
        "aspiration",
        "engine-type",
        "engine-location",
        "fuel-system"
    ]

    df = pd.get_dummies(df, columns=one_hot_columns, dtype=int)

    print("\nHorsepower:")
    print(df[["horsepower", "horsepower_scaled"]].head())

    print("\nMake:")
    print(df[["make", "make_freq"]].head())

    print("\nBody Style:")
    print(df.filter(like="body-style_").head())

    return df
    
def save_data(df: pd.DataFrame, path: str) -> None:
    df.to_csv(path, index=False)
    print(f"\nDataset hasil pipeline disimpan di: {path}")

 
def main():
    df = load_data(DATA_PATH)
    inspect_data(df)

    df_clean = clean_data(df)
    df_transformed = transform_data(df_clean)

    save_data(df_transformed, PROCESSED_DATA_PATH)
    
 
if __name__ == "__main__":
    main()