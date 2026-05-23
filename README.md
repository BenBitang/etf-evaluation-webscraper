# ETF Evaluation Webscraper

**Get Inspire Impact Scores for all stocks in an ETF, and visualize score distribution.**

![Inspire Impact Score Distribution](visualization/score_distribution.png)

This repo provides everything you need to:

- Input a CSV of stock tickers held by any (Catholic, Vatican, or other) ETF (`input_tickers.csv`).
- Scrape Inspire Impact Scores for those tickers from inspireinsight.com with the included Python script.
- Output a results CSV (e.g., `inspire_scores_20260305.csv`), ready for further analysis or visualization.
- See and recreate a Power BI visualization of the impact score distribution (`visualization/score_distribution.png`).

---

## Quick Start

1. **Prepare your tickers:** Edit `input_tickers.csv` to your target ETF's holdings (sample provided).
2. **Run the scraper:**
   ```bash
   pip install -r requirements.txt
   playwright install
   python fetch_inspire_scores.py
   ```
   Output will be saved as a dated CSV (`inspire_scores_YYYYMMDD.csv`).
3. **Visualize:** Load the output CSV into Power BI (or Excel, etc.) using "Inspire Impact Score" for analysis. Example: see `visualization/score_distribution.png`.

---

## Files & Structure

- `input_tickers.csv` — Input: List of ETF stock tickers & names.
- `inspire_scores_*.csv` — Output: Stocks, names, and their Inspire Impact Scores.
- `fetch_inspire_scores.py` — Python3 script to scrape scores.
- `requirements.txt` — Dependencies for quick install.
- `visualization/` — Contains the Power BI (or other) score distribution image and documentation.

---

## About the Data

- **Input:** Any ETF stock list (here, a Catholic ETF, anonymized for privacy).
- **Scrape:** Inspire Impact Scores quantify "biblical compatibility" of each company, as defined on `inspireinsight.com`.
- **Output:** CSV with tickers, company names, and scores (-100 = least compatible, +100 = most compatible).

---

## Author

Data, scripting, and visualization by [BenBitang](https://github.com/BenBitang)

---

*This project is for educational and demonstration purposes only. No investment advice is given.*
