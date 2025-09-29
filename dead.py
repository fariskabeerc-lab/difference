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

# Compute Average Sales as Total ÷ 269
for year in years:
    totals[year]["Average Sales"] = totals[year]["Total Sales"] / 269

# --- Key Insights ---
st.subheader("Key Insights")
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales 2023", f"{totals['2023']['Total Sales']:,.2f}")
col2.metric("Total Sales 2024", f"{totals['2024']['Total Sales']:,.2f}",
            f"{totals['2024']['Total Sales'] - totals['2023']['Total Sales']:,.2f}")
col3.metric("Total Sales 2025", f"{totals['2025']['Total Sales']:,.2f}",
            f"{totals['2025']['Total Sales'] - totals['2024']['Total Sales']:,.2f}")

col4, col5, col6 = st.columns(3)
col4.metric("Avg Sales 2023", f"{totals['2023']['Average Sales']:,.2f}")
col5.metric("Avg Sales 2024", f"{totals['2024']['Average Sales']:,.2f}")
col6.metric("Avg Sales 2025", f"{totals['2025']['Average Sales']:,.2f}")

col7, col8, col9 = st.columns(3)
col7.metric("Avg Margin 2023 (%)", f"{totals['2023']['Mar(%)']:.2f}")
col8.metric("Avg Margin 2024 (%)", f"{totals['2024']['Mar(%)']:.2f}")
col9.metric("Avg Margin 2025 (%)", f"{totals['2025']['Mar(%)']:.2f}")

st.markdown("---")

# --- Function to plot horizontal bar ---
def plot_horizontal_bar(data, x_col, y_col, color_col, title, color_scale="Viridis"):
    fig = px.bar(
        data,
        y=y_col,
        x=x_col,
        orientation='h',
        text=x_col,
        color=color_col,
        color_continuous_scale=color_scale,
        labels={x_col: title, y_col: y_col}
    )
    fig.update_traces(
        texttemplate='%{text:,.2f}',
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Value: %{x:,.2f}<extra></extra>'
    )
    fig.update_layout(
        yaxis={'categoryorder':'total ascending'},
        height=500,
        margin=dict(l=100, r=50, t=50, b=50),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig, use_container_width=True)

# --- Prepare Data for Charts ---
if selected_branch == "All Branches":
    for metric in metrics:
        for year in years:
            col_name = f"{year} 01-JAN to 31-AUG {metric}"
            st.subheader(f"{metric} - {year}")
            plot_horizontal_bar(filtered_df, col_name, "Branch", col_name,
                                f"{metric} ({year})",
                                "Viridis" if metric=="Total Sales" else "Blues")
else:
    # Single branch: show metrics over years as horizontal bars
    single_data = []
    for metric in metrics:
        row = {"Metric": metric}
        for year in years:
            col_name = f"{year} 01-JAN to 31-AUG {metric}"
            row[year] = filtered_df.iloc[0][col_name]
        single_data.append(row)
    single_df = pd.DataFrame(single_data)
    for idx, row in single_df.iterrows():
        st.subheader(f"{row['Metric']} - {selected_branch}")
        plot_horizontal_bar(pd.DataFrame({"Year": years, "Value": [row[y] for y in years]}),
                            "Value", "Year", "Value", row['Metric'])

st.markdown("---")

# --- Show Data Table ---
st.subheader("Branch-wise Full Data")
st.dataframe(filtered_df, height=600)
