from pathlib import Path
import pandas as pd

DATA_PATH = Path("data/processed/subscriptions_clean.csv")
OUT_PATH = Path("data/processed/customers_at_risk.csv")

def main():
    df = pd.read_csv(DATA_PATH)

    # Señales binarias
    df["flag_low_usage"] = df["avg_weekly_usage_hours"] < 3
    df["flag_inactive"] = df["last_login_days_ago"] > 14
    df["flag_high_support"] = df["support_tickets"] >= 5
    df["flag_payment_issues"] = df["payment_failures"] >= 1

    # Risk score (reglas de negocio)
    df["risk_score"] = (
        df["flag_low_usage"].astype(int) * 3 +
        df["flag_high_support"].astype(int) * 2 +
        df["flag_inactive"].astype(int) * 1 +
        df["flag_payment_issues"].astype(int) * 1
    )

    # Segmentación de riesgo
    df["risk_segment"] = pd.cut(
        df["risk_score"],
        bins=[-1, 1, 3, 5, 10],
        labels=["Low", "Medium", "High", "Critical"]
    )

    df.to_csv(OUT_PATH, index=False)

    print(f"Archivo creado: {OUT_PATH}")
    print("\nDistribución por segmento:")
    print(df["risk_segment"].value_counts())

    print("\nChurn por segmento:")
    print(df.groupby("risk_segment")["churn_num"].mean())

if __name__ == "__main__":
    main()
