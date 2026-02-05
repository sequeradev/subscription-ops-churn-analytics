from pathlib import Path
import pandas as pd

RAW_DIR = Path("data/raw")

def find_csv() -> Path:
    csv_files = list(RAW_DIR.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError("No hay ningún .csv dentro de data/raw/")
    if len(csv_files) > 1:
        print("Aviso: hay varios CSV. Usaré el primero:")
        for f in csv_files:
            print(" -", f.name)
    return csv_files[0]

def main():
    csv_path = find_csv()
    print(f"Usando archivo: {csv_path}")

    df = pd.read_csv(csv_path)

    print("\n=== BASIC INFO ===")
    print(df.info())

    print("\n=== FIRST ROWS ===")
    print(df.head())

    print("\n=== NULL VALUES ===")
    print(df.isna().sum())

    # churn puede venir como 0/1 o texto; lo detectamos
    if "churn" not in df.columns:
        raise KeyError("No existe la columna 'churn' en el dataset.")

    print("\n=== CHURN UNIQUE VALUES ===")
    print(df["churn"].unique()[:10])

    churn_series = df["churn"]

    # Normaliza a texto python y mapea a 0/1
    churn_num = (
        churn_series.astype("string")
        .str.strip()
        .str.lower()
        .map({"yes": 1, "no": 0, "true": 1, "false": 0, "1": 1, "0": 0})
        .astype("Int64")
    )

    if churn_num.isna().any():
        bad = df.loc[churn_num.isna(), "churn"].unique()
        raise ValueError(f"Valores de churn no mapeados: {bad}")

    churn_rate = float(churn_num.mean())

    print("\n=== CHURN RATE ===")
    print(f"Churn rate: {churn_rate:.2%}")

    if "plan_type" in df.columns:
        print("\n=== CHURN BY PLAN ===")
        tmp = df.copy()
        tmp["_churn_num"] = churn_num
        print(tmp.groupby("plan_type")["_churn_num"].mean().sort_values(ascending=False))
    else:
        print("\n(No existe 'plan_type' para churn by plan)")

if __name__ == "__main__":
    main()
