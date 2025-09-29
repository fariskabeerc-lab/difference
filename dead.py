import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Setup ---
st.set_page_config(page_title="Branch Yearly Sales Report", layout="wide")
st.title("📊 Branch Yearly Sales Insights")

# --- Load Data ---
df = pd.read_excel("Sales 2024 Vs 2025 (1).Xlsx")  # Replace with your file

# --- Calculate Totals ---
years = ["2023", "2024", "2025"]
metrics = ["Total Sales", "Avg Sales", "Mar(%)"]

# Initialize dictionary to store totals
totals = {}
for year in years:
    totals[year] = {}
    for metric in metrics:
        col_name = f"{year} 01-JAN to 31-AUG {metric}"
        totals[year][metric] = df[col_name].sum() if metric != "Mar(%)" else df[col_name].mean()

# --- Calculate Differences ---
diff_2024_2023 = totals["2024"]["Total Sales"] - totals["2023"]["Total Sales"]
diff_2025_2024 = totals["2025"]["Total Sales"] - totals["2024"]["Total Sales"]

# --- Display Insights ---
st.subheader("Key Insights")
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales 2023", f"{totals['2023']['Total Sales']:,.2f}")
col2.metric("Total Sales 2024", f"{totals['2024']['Total Sales']:,.2f}", f"{diff_2024_2023:,.2f}")
col3.metric("Total Sales 2025", f"{totals['2025']['Total Sales']:,.2f}", f"{diff_2025_2024:,.2f}")

col4, col5, col6 = st.columns(3)
col4.metric("Average Sales 2023", f"{totals['2023']['Avg Sales']:,.2f}")
col5.metric("Average Sales 2024", f"{totals['2024']['Avg Sales']:,.2f}")
col6.metric("Average Sales 2025", f"{totals['2025']['Avg Sales']:,.2f}")

col7, col8, col9 = st.columns(3)
col7.metric("Avg Margin 2023 (%)", f"{totals['2023']['Mar(%)']:.2f}%")
col8.metric("Avg Margin 2024 (%)", f"{totals['2024']['Mar(%)']:.2f}%")
col9.metric("Avg Margin 2025 (%)", f"{totals['2025']['Mar(%)']:.2f}%")

st.markdown("---")

# --- Show DataFrame ---
st.subheader("Branch-wise Data")
st.dataframe(df, height=500)

# --- Optional: Visualize Total Sales by Year ---
sales_df = pd.DataFrame({
    "Year": years,
    "Total Sales": [totals[y]["Total Sales"] for y in years]
})

st.subheader("Total Sales Trend")
fig = px.bar(sales_df, x="Year", y="Total Sales", text="Total Sales", color="Total Sales",
             color_continuous_scale="Viridis")
fig.update_traces(texttemplate='%{text:,.2f}', textposition='outside')
fig.update_layout(yaxis_title="Total Sales", xaxis_title="Year", height=500)
st.plotly_chart(fig, use_container_width=True)
