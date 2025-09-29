import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Setup ---
st.set_page_config(page_title="Branch Yearly Sales Dashboard", layout="wide")
st.title("📊 Branch Yearly Sales Dashboard (2023-2025)")

# --- Load Data ---
df = pd.read_excel("Sales 2024 Vs 2025 (3).Xlsx")  # replace with your file

# --- Sidebar Filters ---
branches = df["Branch"].unique().tolist()
branches = ["All Branches"] + branches
selected_branch = st.sidebar.selectbox("Select Branch", branches)

years = ["2023", "2024", "2025"]
metrics = ["Total Sales", "Avg Sales", "Mar(%)"]

# --- Filter by Branch ---
filtered_df = df.copy()
if selected_branch != "All Branches":
    filtered_df = filtered_df[filtered_df["Branch"] == selected_branch]

# --- Compute Totals & Differences ---
totals = {}
for year in years:
    totals[year] = {}
    for metric in metrics:
        col_name = f"{year} 01-JAN to 31-AUG {metric}"
        if metric != "Mar(%)":
            totals[year][metric] = filtered_df[col_name].sum()
        else:
            totals[year][metric] = filtered_df[col_name].mean()

# Differences columns exist in your data
diff_cols = ["DIFFERENCE Total Sales", "DIFFERENCE Avg Sales", "DIFFERENCE Mar(%)"]
diffs = {col: filtered_df[col].sum() for col in diff_cols}

# --- Compute Average Sales as Total ÷ 269 ---
for year in years:
    totals[year]["Average Sales"] = totals[year]["Total Sales"] / 269

# --- Key Insights ---
st.subheader("Key Insights")
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales 2023", f"{totals['2023']['Total Sales']:,.2f}")
col2.metric("Total Sales 2024", f"{totals['2024']['Total Sales']:,.2f}", f"{totals['2024']['Total Sales'] - totals['2023']['Total Sales']:,.2f}")
col3.metric("Total Sales 2025", f"{totals['2025']['Total Sales']:,.2f}", f"{totals['2025']['Total Sales'] - totals['2024']['Total Sales']:,.2f}")

col4, col5, col6 = st.columns(3)
col4.metric("Avg Sales 2023", f"{totals['2023']['Average Sales']:,.2f}")
col5.metric("Avg Sales 2024", f"{totals['2024']['Average Sales']:,.2f}")
col6.metric("Avg Sales 2025", f"{totals[']()
