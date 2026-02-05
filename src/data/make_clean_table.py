from pathlib import Path
import pandas as pd

RAW_DIR = Path("data/raw")
OUT_DIR = Path("data/processed")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def main():
    csv_files = list(RAW_DIR.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError("No hay CSV en data/raw")
    csv_path = csv_files[0]

    print(f"Usando archivo: {csv_path.name}")

    df = pd.read_csv(csv_path)

    # Fecha
    df["signup_date"] = pd.to_datetime(df["signup_date"])

    # Churn numérico
    df["churn_num"] = (
        df["churn"]
        .astype("string")
        .str.strip()
        .str.lower()
        .map({"yes": 1, "no": 0})
        .astype("Int64")
    )

    # Validación
    if df["churn_num"].isna().any():
        raise ValueError("Error al mapear churn")

    # Guardar
    out_path = OUT_DIR / "subscriptions_clean.csv"
    df.to_csv(out_path, index=False)

    print(f"Archivo limpio creado en: {out_path}")
    print(f"Filas: {len(df):,}")
    print("Columnas:")
    print(list(df.columns))

if __name__ == "__main__":
    main()
