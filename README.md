# 🛡️ Vulnerability Dashboard

A Python-based interactive security vulnerability dashboard built with Plotly, designed to visualize and analyze vulnerability data across severity levels, CVSS scores, categories, and remediation status.

---

## 📋 Overview

This project provides a suite of chart functions that render rich, dark-themed visualizations for cybersecurity vulnerability data. It is intended as a final year project demonstrating practical data visualization techniques applied to a real-world security context.

---

## ✨ Features

- **Risk Gauge** — Overall risk score (0–100) computed from weighted severity counts, displayed as an animated gauge.
- **Severity Bar Chart** — Distribution of vulnerabilities across Critical, High, Medium, and Low severity levels.
- **Status Donut Chart** — Breakdown of vulnerabilities by remediation status (Open, In Progress, Resolved).
- **CVSS Radar Chart** — Radar/spider visualization of the top 8 vulnerabilities by CVSS score.
- **Category Bar Chart** — Horizontal bar chart showing vulnerability counts grouped by category.

---

## 🗂️ Project Structure

```
vulnerability-dashboard/
│
├── charts.py          # Core visualization functions (Plotly figures)
├── data/              # Sample or real vulnerability datasets (CSV/JSON)
├── app.py             # (Optional) Entry point / Dash/Streamlit app
├── requirements.txt   # Python dependencies
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/vulnerability-dashboard.git
cd vulnerability-dashboard

# Install dependencies
pip install -r requirements.txt
```

### Requirements

```
plotly>=5.0.0
pandas>=1.3.0
```

---

## 📊 Usage

The main module (`charts.py`) exposes five functions, each accepting a Pandas DataFrame and returning a Plotly `Figure` object.

### Expected DataFrame Schema

| Column       | Type    | Description                                      |
|--------------|---------|--------------------------------------------------|
| `Name`       | string  | Vulnerability name or CVE identifier             |
| `Severity`   | string  | One of: `Critical`, `High`, `Medium`, `Low`      |
| `Status`     | string  | One of: `Open`, `In Progress`, `Resolved`        |
| `CVSS Score` | float   | CVSS score in range 0.0 – 10.0                   |
| `Category`   | string  | Vulnerability category (e.g., XSS, SQLi, RCE)   |

### Example

```python
import pandas as pd
from charts import risk_gauge, severity_bar, status_pie, cvss_radar, category_bar

# Load your vulnerability data
df = pd.read_csv("data/vulnerabilities.csv")

# Generate charts
fig1 = risk_gauge(df)
fig2 = severity_bar(df)
fig3 = status_pie(df)
fig4 = cvss_radar(df)
fig5 = category_bar(df)

# Display in browser
fig1.show()
```

---

## 📐 Risk Score Calculation

The overall risk score is a weighted average based on severity:

| Severity | Weight |
|----------|--------|
| Critical | 10     |
| High     | 7      |
| Medium   | 4      |
| Low      | 1      |

```
Risk Score = (Σ weight per vulnerability) / (max_weight × total_vulnerabilities) × 100
```

A score of 0–33 is considered Low risk, 33–67 Medium, and 67–100 High.

---

## 🎨 Design

All charts use a consistent dark theme with a navy/slate background and a neon accent palette:

| Severity / Status | Color     |
|-------------------|-----------|
| Critical / Open   | `#ff3b5c` |
| High / In Progress| `#ff8c00` |
| Medium            | `#ffc800` |
| Low / Resolved    | `#00ff88` |
| CVSS Accent       | `#00d4ff` |
| Category Bars     | `#7c3aed` |

---

## 🔮 Future Improvements

- [ ] Add a Streamlit or Dash front-end for a fully interactive web dashboard
- [ ] Support CSV/JSON file upload for dynamic data ingestion
- [ ] Add time-series charts to track vulnerability trends over time
- [ ] Export reports as PDF
- [ ] Add filtering by category, severity, and date range

---

## 🧑‍💻 Author

**Your Name**  
Final Year Project — B.Tech / BSc Computer Science  
[Your Institution], [Year]

---

## 📄 License

This project is for academic purposes. See `LICENSE` for details.
