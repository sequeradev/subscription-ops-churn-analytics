from pathlib import Path
import pandas as pd

DATA_PATH = Path("data/processed/subscriptions_clean.csv")

def main():
    df = pd.read_csv(DATA_PATH, parse_dates=["signup_date"])

    print("=== GLOBAL KPIs ===")
    print(f"Churn rate: {df['churn_num'].mean():.2%}")
    print(f"Avg tenure (months): {df['tenure_months'].mean():.1f}")
    print(f"Avg weekly usage (hours): {df['avg_weekly_usage_hours'].mean():.1f}")
    print(f"Avg support tickets: {df['support_tickets'].mean():.2f}")
    print(f"Payment failure rate: {(df['payment_failures'] > 0).mean():.2%}")

    print("\n=== OPERATIONAL SIGNALS ===")

    signals = {
        "Inactive >14 days": (df["last_login_days_ago"] > 14).mean(),
        "Low usage (<3h/week)": (df["avg_weekly_usage_hours"] < 3).mean(),
        "High support (>=5 tickets)": (df["support_tickets"] >= 5).mean(),
        "Payment issues (>=1 failure)": (df["payment_failures"] >= 1).mean(),
    }

    for k, v in signals.items():
        print(f"{k}: {v:.2%}")

    print("\n=== CHURN BY SIGNAL ===")
    for signal, mask in {
        "Inactive >14 days": df["last_login_days_ago"] > 14,
        "Low usage (<3h/week)": df["avg_weekly_usage_hours"] < 3,
        "High support (>=5 tickets)": df["support_tickets"] >= 5,
        "Payment issues": df["payment_failures"] >= 1,
    }.items():
        churn_rate = df.loc[mask, "churn_num"].mean()
        print(f"{signal}: {churn_rate:.2%}")

if __name__ == "__main__":
    main()
