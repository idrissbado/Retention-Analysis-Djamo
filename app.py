import pandas as pd
from sqlalchemy import create_engine
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import LogisticRegression
import json

# Dashboard App
app = Dash(__name__)

# Global Variables
db_config = {"host": "", "port": "", "username": "", "password": "", "database": ""}

# Connect to the database
def connect_to_db():
    try:
        connection_url = f"mysql+pymysql://{db_config['username']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
        engine = create_engine(connection_url)
        return engine
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

# Extract data based on table and columns
def extract_data(table, columns, engine):
    try:
        query = f"SELECT {', '.join(columns)} FROM {table}"
        return pd.read_sql(query, engine)
    except Exception as e:
        print(f"Error extracting data: {e}")
        return None

# Fraud Detection
def detect_fraud(data):
    data['commission_to_deposit_ratio'] = data['commissions'] / data['deposits']
    features = data[['commissions', 'sign_ups', 'commission_to_deposit_ratio']]

    model = IsolationForest(contamination=0.05)
    data['fraud_risk'] = model.fit_predict(features)
    return data

# Churn Analysis
def churn_analysis(data):
    data['churn'] = (data['last_active_days'] > 30).astype(int)
    features = data[['session_count', 'deposit_count', 'feature_usage']]
    target = data['churn']

    model = LogisticRegression()
    model.fit(features, target)

    data['churn_prediction'] = model.predict(features)
    return data, pd.Series(model.coef_[0], index=features.columns)

# Feature Usage
def feature_usage_analysis(data):
    usage_summary = data.groupby('feature').size().sort_values(ascending=False)
    return usage_summary

# Dashboard Layout
app.layout = html.Div([
    html.H1("Djamo Business Case Dashboard"),
    html.Div([
        html.Label("Database Configuration"),
        dcc.Input(id="db-host", type="text", placeholder="Host", debounce=True),
        dcc.Input(id="db-port", type="number", placeholder="Port", debounce=True),
        dcc.Input(id="db-username", type="text", placeholder="Username", debounce=True),
        dcc.Input(id="db-password", type="password", placeholder="Password", debounce=True),
        dcc.Input(id="db-name", type="text", placeholder="Database Name", debounce=True),
    ], style={"marginBottom": "20px"}),

    html.Div([
        html.Label("Select Table:"),
        dcc.Input(id="table-name", type="text", placeholder="Table Name"),
        html.Label("Select Columns (comma-separated):"),
        dcc.Input(id="columns", type="text", placeholder="Column Names"),
        html.Button("Load Data", id="load-data", n_clicks=0)
    ], style={"marginBottom": "20px"}),

    html.Div(id="data-status", style={"color": "red", "marginBottom": "20px"}),

    dcc.Tabs(id="tabs", value="fraud", children=[
        dcc.Tab(label="Fraud Detection", value="fraud"),
        dcc.Tab(label="Churn Analysis", value="churn"),
        dcc.Tab(label="Feature Usage", value="usage")
    ]),
    html.Div(id="tab-content")
])

# Callbacks
@app.callback(
    Output("data-status", "children"),
    Output("tab-content", "children"),
    Input("db-host", "value"),
    Input("db-port", "value"),
    Input("db-username", "value"),
    Input("db-password", "value"),
    Input("db-name", "value"),
    Input("table-name", "value"),
    Input("columns", "value"),
    Input("load-data", "n_clicks"),
    Input("tabs", "value")
)
def update_dashboard(host, port, username, password, db_name, table, columns, n_clicks, tab):
    global db_config
    db_config.update({"host": host, "port": port, "username": username, "password": password, "database": db_name})

    if n_clicks > 0:
        engine = connect_to_db()
        if engine:
            columns_list = columns.split(",") if columns else []
            data = extract_data(table, columns_list, engine)

            if data is not None:
                if tab == "fraud":
                    fraud_data = detect_fraud(data)
                    fig = px.scatter(fraud_data, x="commissions", y="deposits", color="fraud_risk",
                                     title="Fraud Detection")
                    return "Data loaded successfully", dcc.Graph(figure=fig)
                elif tab == "churn":
                    churn_data, coefficients = churn_analysis(data)
                    fig = px.bar(coefficients, title="Churn Feature Importance")
                    return "Data loaded successfully", dcc.Graph(figure=fig)
                elif tab == "usage":
                    usage_summary = feature_usage_analysis(data)
                    fig = px.bar(x=usage_summary.index, y=usage_summary.values, title="Feature Usage Analysis")
                    return "Data loaded successfully", dcc.Graph(figure=fig)
        return "Failed to connect or load data. Check configuration.", None

    return "Waiting for data load...", None

if __name__ == "__main__":
    app.run_server(debug=True)

