# Retention-Analysis-Djamo
This dashboard allows Djamo to analyze critical business cases
# Djamo Business Case Dashboard

## Overview
This dashboard allows Djamo to analyze critical business cases:
1. **Fraud Detection**: Identify suspicious agents using isolation forest.
2. **Churn Analysis**: Analyze user churn drivers and predict churn.
3. **Feature Usage**: Explore app feature usage trends.

---

## Features
- **Database Configuration**: Input host, port, username, password, and database name to connect.
- **Dynamic Column Selection**: Select relevant columns for analysis.
- **Real-Time Analysis**: Results displayed instantly based on the selected business case.
- **Interactive Dashboard**: Tabs for Fraud, Churn, and Feature Usage analysis.

---

## Installation
1. Install dependencies:
   ```bash
   pip install pandas sqlalchemy plotly dash scikit-learn

# Run the application:


python app.py
Open http://127.0.0.1:8050/ in your browser.

# Usage
Fill in the database credentials.
Specify the table and columns to analyze.
Select the tab for the desired business case:
Fraud Detection: Requires commissions, deposits, and sign_ups.
Churn Analysis: Requires last_active_days, session_count, deposit_count, and feature_usage.
Feature Usage: Requires feature.
# Requirements
Python 3.8+
MySQL Database
Required tables: Transactions, User Activity, Usage Logs


# This setup includes:
- Full functionality to connect to a database.
- Real-time interactive analysis for each business case.
- A complete README file for setup and usage.
