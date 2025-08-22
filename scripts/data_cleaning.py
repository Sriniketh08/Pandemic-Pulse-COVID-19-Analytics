
from pathlib import Path
import pandas as pd
import requests

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
RAW_CSV = DATA_DIR / "owid-covid-data.csv"
CLEAN_CSV = DATA_DIR / "covid_cleaned.csv"
OWID_URL = "https://covid.ourworldindata.org/data/owid-covid-data.csv"

def download():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not RAW_CSV.exists():
        print("Downloading dataset...")
        resp = requests.get(OWID_URL, timeout=60)
        resp.raise_for_status()
        RAW_CSV.write_bytes(resp.content)
        print(f"Saved to {RAW_CSV}")

def clean():
    print("Cleaning dataset...")
    usecols = ["location","date","total_cases","new_cases","total_deaths","new_deaths",
               "total_vaccinations","new_vaccinations","people_vaccinated","people_fully_vaccinated",
               "population","continent"]
    df = pd.read_csv(RAW_CSV, usecols=usecols, parse_dates=["date"])

    # Keep countries only (drop aggregates like 'World')
    df = df[df["continent"].notna()].copy()

    # Forward-fill cumulative metrics within each country
    df = df.sort_values(["location","date"])
    cum_cols = ["total_cases","total_deaths","total_vaccinations","people_vaccinated","people_fully_vaccinated"]
    df[cum_cols] = df.groupby("location")[cum_cols].ffill()

    df.to_csv(CLEAN_CSV, index=False)
    print(f"Wrote cleaned CSV to {CLEAN_CSV}")

if __name__ == "__main__":
    download()
    clean()
