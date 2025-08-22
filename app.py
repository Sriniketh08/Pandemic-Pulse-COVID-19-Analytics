
import streamlit as st
import pandas as pd
import plotly.express as px
import duckdb
from pathlib import Path
import requests

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
RAW_CSV = DATA_DIR / "owid-covid-data.csv"
CLEAN_CSV = DATA_DIR / "covid_cleaned.csv"

OWID_URL = "https://covid.ourworldindata.org/data/owid-covid-data.csv"

def download_if_missing():
    if not RAW_CSV.exists():
        st.info("Downloading dataset from Our World in Data...")
        resp = requests.get(OWID_URL, timeout=60)
        resp.raise_for_status()
        RAW_CSV.write_bytes(resp.content)
        st.success(f"Downloaded to {RAW_CSV}")

@st.cache_data(show_spinner=False)
def load_data(clean: bool = True):
    download_if_missing()
    # Prefer cleaned data if present
    if clean and CLEAN_CSV.exists():
        df = pd.read_csv(CLEAN_CSV, parse_dates=["date"])
    else:
        usecols = ["location","date","total_cases","new_cases","total_deaths","new_deaths",
                   "total_vaccinations","new_vaccinations","people_vaccinated","people_fully_vaccinated",
                   "population","continent"]
        df = pd.read_csv(RAW_CSV, usecols=usecols, parse_dates=["date"])
    # Basic cleaning
    df = df[df["continent"].notna()]  # keep countries only
    df = df.sort_values(["location","date"]).reset_index(drop=True)
    return df

st.set_page_config(page_title="COVID-19 Analytics", layout="wide")
st.title("🦠 COVID-19 Data Analytics Dashboard")
st.caption("Data: Our World in Data — auto-downloaded on first run.")

df = load_data()

# Sidebar controls
countries = sorted(df["location"].unique().tolist())
sel_countries = st.sidebar.multiselect("Select countries", countries, default=["United States","India","Brazil"][:3])
date_min, date_max = df["date"].min(), df["date"].max()
sel_dates = st.sidebar.date_input("Date range", (date_min, date_max), min_value=date_min, max_value=date_max)

if isinstance(sel_dates, tuple):
    start_date, end_date = pd.to_datetime(sel_dates[0]), pd.to_datetime(sel_dates[1])
else:
    start_date, end_date = date_min, date_max

mask = (df["location"].isin(sel_countries)) & (df["date"].between(start_date, end_date))
view = df.loc[mask].copy()

# KPIs (latest snapshot across selected countries)
latest = (view.sort_values("date")
             .groupby("location", as_index=False)
             .tail(1))

total_cases = latest["total_cases"].sum(min_count=1)
total_deaths = latest["total_deaths"].sum(min_count=1)
total_vax = latest["people_fully_vaccinated"].sum(min_count=1)

k1, k2, k3 = st.columns(3)
k1.metric("Total Cases (selected)", f"{int(total_cases):,}" if pd.notna(total_cases) else "N/A")
k2.metric("Total Deaths (selected)", f"{int(total_deaths):,}" if pd.notna(total_deaths) else "N/A")
k3.metric("Fully Vaccinated (selected)", f"{int(total_vax):,}" if pd.notna(total_vax) else "N/A")

# Charts
c1, c2 = st.columns(2)

with c1:
    fig_cases = px.line(view, x="date", y="total_cases", color="location", title="Total Cases Over Time")
    st.plotly_chart(fig_cases, use_container_width=True)

with c2:
    fig_vax = px.line(view, x="date", y="people_fully_vaccinated", color="location", title="Fully Vaccinated Over Time")
    st.plotly_chart(fig_vax, use_container_width=True)

st.subheader("Top Countries (Latest Snapshot)")
metric = st.selectbox("Metric", ["total_cases", "total_deaths", "people_fully_vaccinated"], index=0)
topn = st.slider("Top N", min_value=5, max_value=25, value=10, step=1)

# Compute latest snapshot per country
latest_all = (df.sort_values("date")
                .groupby("location", as_index=False)
                .tail(1))
latest_all = latest_all[latest_all["continent"].notna()]

# Bar chart
top_table = latest_all.nlargest(topn, metric)[["location", metric]]
fig_bar = px.bar(top_table, x=metric, y="location", orientation="h", title=f"Top {topn} by {metric}")
st.plotly_chart(fig_bar, use_container_width=True)

# SQL Examples via DuckDB
st.subheader("SQL on CSV via DuckDB")
sql_default = f"""
-- Example: Top 10 countries by cases per million (latest)
WITH latest AS (
  SELECT * FROM read_csv_auto('{RAW_CSV.as_posix()}')
  WHERE continent IS NOT NULL
  QUALIFY ROW_NUMBER() OVER (PARTITION BY location ORDER BY date DESC) = 1
)
SELECT location, total_cases, total_deaths
FROM latest
ORDER BY total_cases DESC
LIMIT 10;
"""

user_sql = st.text_area("Run SQL (DuckDB)", sql_default, height=200)
if st.button("Execute SQL"):
    try:
        con = duckdb.connect(database=':memory:')
        res = con.execute(user_sql).df()
        st.dataframe(res, use_container_width=True)
    except Exception as e:
        st.error(str(e))
