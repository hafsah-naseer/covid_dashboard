# Interactive COVID-19 Data Trend Analyzer

Project submitted by: Hafsah Naseer , Maryam Qasim
                    2520100            2520086
Submitted to: mr. Mustajab

## Project Overview
This project is a modular web application that integrates large-dataset handling, moving window analysis, and dynamic data visualization into an interactive interface. The application processes the official Our World in Data (OWID) COVID-19 dataset using **Pandas**, generates advanced data visualizations using **Matplotlib**, and exposes them via a robust **Flask** web framework. 

This software strictly complies with rigorous production standards: it requires Python 3.10+, utilizes explicit modular programming practices, runs within a fully isolated virtual environment with pinned tracking, and implements layered custom exception handlers to safeguard runtime stability.

---

## Data Source
* **Dataset Used:** Our World in Data (OWID) COVID-19 Dataset  
* **Source URL:** [https://github.com/owid/covid-19-data/tree/master/public/data](https://github.com/owid/covid-19-data/tree/master/public/data)  
* **Data Persistence:** The raw CSV file (`owid-covid-data.csv`) must be downloaded from the source tracking URL above and committed to the local root workspace repository directory to track file I/O constraints successfully.

---

## Technical Stack & Constraints
- **Language:** Python 3.10+
- **Data Engineering:** Pandas (Structural list screening, temporal indexing, sorting, and window-based rolling aggregations)
- **Graphics Pipeline:** Matplotlib (In-memory `Agg` multi-series drawing backend, Base64 transmission streams)
- **Web Interface:** Flask (Jinja2 dynamic templating, HTTP POST parameter parsing)

---

## Modular File Structure
The project splits UI routing, analysis, error tracking, and input data across isolated Python execution scopes:

```text
covid_dashboard/
│
├── app.py                  # Main Flask server orchestration layer & route definitions
├── data_processing.py      # Pandas logic: file ingestion, data cleaning, & 7-day rolling calculations
├── visualization.py        # Matplotlib visualization engine & Base64 stream serialization
├── exceptions.py           # Custom application-specific error exception architectures
├── owid-covid-data.csv     # Local persistent raw dataset (must be present to run)
├── requirements.txt        # Pinned project dependencies with exact version boundaries
├── README.md               # Application deployment documentation and context
└── templates/
    ├── index.html          # Front-end dynamic form analyzer and line chart page
    └── compare.html        # Front-end static maximum deaths comparative layout
