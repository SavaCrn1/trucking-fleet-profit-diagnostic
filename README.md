# Trucking Fleet Profit Diagnostic

A Python data pipeline that turns raw trip-level trucking data into a client-ready HTML diagnostic report — analyzing driver, broker, and dispatcher performance to surface where a fleet is losing profit and what to do about it.

**[View the sample report ->](https://savacrn1.github.io/trucking-fleet-profit-diagnostic/)**

## What it does

Given a spreadsheet of trip records (revenue, miles, deadhead, rate per mile, driver/broker/dispatcher assignments), the pipeline computes:

- **Driver analysis** — total revenue, average cost per mile, and average deadhead miles per driver
- **Broker analysis** — load volume, average profit, and rate per mile by broker
- **Dispatcher analysis** — profit per mile, rate per mile, and deadhead percentage by dispatcher
- **Overall fleet performance** — profit per mile, total profit, average cost per mile, and revenue run-rate
- **Action plan** — narrative recommendations based on the numbers (e.g. reassigning loads toward higher-performing dispatchers or brokers)

The results are rendered into a self-contained HTML report with interactive Chart.js bar charts — each table column can be clicked to re-sort the corresponding chart.

## How it works

1. `Py files/trucking_analysis.py` loads the source spreadsheet with pandas and aggregates it into driver, broker, dispatcher, and overall-performance summaries.
2. `Py files/report_generator.py` feeds those results into a Jinja2 template (`templates/diagnostic.html`) and writes the rendered report to `Output/diagnostic_report.html`.

## Project structure

```
Datasets/           Sample trip-level trucking data (xlsx/csv)
Py files/           Analysis and report-generation scripts
templates/          Jinja2 HTML template for the diagnostic report
Output/             Generated diagnostic_report.html
docs/               Copy of the report published via GitHub Pages
```

## Running it

```bash
pip install pandas jinja2 openpyxl
cd "Py files"
python report_generator.py
```

This regenerates `Output/diagnostic_report.html` from the dataset referenced in `trucking_analysis.py`.

## Stack

Python, pandas, Jinja2, Chart.js

---

Built by Sava Crnjak as a personal data-analysis project, January 2026.
