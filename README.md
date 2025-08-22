# COVID-19 Data Analytics Dashboard

End-to-end, portfolio-ready data analytics project:
- **Data**: Our World in Data COVID-19 dataset (auto-downloaded).
- **Stack**: Python (Pandas, NumPy), Plotly, Streamlit, DuckDB (SQL on files).
- **Outputs**: Interactive dashboard + EDA notebook + SQL examples.

## ✨ Features
- Auto-downloads latest dataset if missing (`owid-covid-data.csv`).
- Clean & transform with reusable `scripts/data_cleaning.py`.
- Run **SQL** directly on CSV/Parquet via DuckDB.
- Interactive **Streamlit** dashboard for trends & comparisons.

## 📦 Project Structure
```
covid-analytics-portfolio/
├─ app.py
├─ README.md
├─ requirements.txt
├─ .gitignore
├─ scripts/
│  ├─ data_cleaning.py
│  └─ sql_queries.sql
├─ notebooks/
│  └─ eda.ipynb
├─ data/
│  └─ (auto-downloaded) owid-covid-data.csv
└─ images/
   └─ (place screenshots for README)
```

## 🚀 Quickstart
```bash
# 1) Create & activate a venv (recommended)
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# 2) Install dependencies
pip install -r requirements.txt

# 3) (Optional) Clean & cache data
python scripts/data_cleaning.py

# 4) Run the dashboard
streamlit run app.py
```

## 📊 What you can show in your portfolio
- EDA notebook with insights and clean visuals.
- A polished, interactive dashboard (Streamlit).
- SQL queries to answer analytical questions with DuckDB.
- Clear documentation (this README) + screenshots in `/images`.

## 🧪 Example Questions Answered
- Which countries have the highest total cases & deaths?
- How do vaccinations relate to case trends?
- What are the time trends for specific countries?
- Which countries have the highest cases/deaths per million?

## 📝 Notes
- The CSV is large; consider **not** committing it. The app auto-downloads it if missing.
- Add screenshots of your dashboard to `/images` and embed them here.
- MIT License—use freely.
