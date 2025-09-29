import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Setup ---
st.set_page_config(page_title="Branch Sales Dashboard", layout="wide")
st.title("📊 Branch Sales Dashboard (2023-2025)")

# --- Data ---
data = {
    "Branch": [
        "AZHAR", "LIWAN", "HADEQAT", "SABAH", "HILAL", "SAHAT",
        "SAFA", "PORT SAEED", "AZHAR GT", "JAIS", "FIDA",
        "BLUE PEARL", "TAYTAY", "SALEM MALL", "OUD MEHTA", "SUPERSTORE", "Grand Total"
    ],
    "2023 Total Sales": [
        35267055.52, 11556513.30, 27933389.52, 8600547.92, 14578191.25, 5597125.02,
        9299600.18, 10140998.98, 6760597.24, 5483037.45, 16316872.69,
        5358873.05, 0, 26685848.50, 0, 0, 186136308.79
    ],
    "2024 Total Sales": [
        34639834.01, 13065728.25, 29616414.52, 12060825.99, 14851756.73, 5753112.33,
        9948602.69, 10876887.59, 6741894.61, 6292322.86, 17859351.69,
        6148201.78, 5533772.24, 33194831.22, 4640301.45, 0, 211223837.96
    ],
    "2025 Total Sales": [
        31162845.37, 10289632.43, 27783796.93, 10570459.29, 13602032.89, 4564110.21,
        9042951.59, 10270157.40, 6337346.41, 5889305.34, 17966957.48,
        6571452.28, 6159775.78, 34964501.80, 9708622.47, 9789990.97, 214673938.64
    ],
    "DIFFERENCE Total Sales": [
        -3476988.64, -2776095.82, -1832617.59, -1490366.70, -1249723.84, -1189002.12,
        -905651.10, -606730.19, -404548.20, -403017.52, 107605.79,
        423250.50, 626003.54, 1769670.58, 5068321.02, 9789990.97, -6339890.29
    ]
}

df = pd.DataFrame(data)

# --- Sidebar Filters ---
branches = df["Branch"].tolist()
branches = ["All Branches"] + branches[:-1]  # exclude Grand Total
selected_branch = st.sidebar.selectbox("Select Branch", branches)

# --- Filter Data ---
if selected_branch != "All Branches":
    filtered_df = df[df["Branch"] == selected_branch]
else:
    filtered_df = df[df["Branch"] != "Grand Total"]  # exclude Grand Total for graphing

# --- Metrics ---
st.subheader("Key Metrics")
total_2023 = filtered_df["2023 Total Sales"].sum()
total_2024 = filtered_df["2024 Total Sales"].sum()
total_2025 = filtered_df["2025 Total Sales"].sum()
diff_total = filtered_df["DIFFERENCE Total Sales"].sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("2023 Total Sales", f"{total_2023:,.2f}")
col2.metric("2024 Total Sales", f"{total_2024:,.2f}")
col3.metric("2025 Total Sales", f"{total_2025:,.2f}")
col4.metric("Difference Total Sales", f"{diff_total:,.2f}")

st.markdown("---")

# --- Horizontal Bar Charts ---
st.subheader("Total Sales by Branch")

fig = px.bar(
    filtered_df,
    x="2023 Total Sales",
    y="Branch",
    orientation='h',
    text="2023 Total Sales",
    labels={"2023 Total Sales": "2023 Total Sales"},
    color="2023 Total Sales",
    color_continuous_scale="Viridis"
)
fig.update_layout(height=600, yaxis={'categoryorder':'total ascending'})
st.plotly_chart(fig, use_container_width=True)

fig2 = px.bar(
    filtered_df,
    x="2024 Total Sales",
    y="Branch",
    orientation='h',
    text="2024 Total Sales",
    labels={"2024 Total Sales": "2024 Total Sales"},
    color="2024 Total Sales",
    color_continuous_scale="Blues"
)
fig2.update_layout(height=600, yaxis={'categoryorder':'total ascending'})
st.plotly_chart(fig2, use_container_width=True)

fig3 = px.bar(
    filtered_df,
    x="2025 Total Sales",
    y="Branch",
    orientation='h',
    text="2025 Total Sales",
    labels={"2025 Total Sales": "2025 Total Sales"},
    color="2025 Total Sales",
    color_continuous_scale="Greens"
)
fig3.update_layout(height=600, yaxis={'categoryorder':'total ascending'})
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# --- Show Table ---
st.subheader("Data Table")
st.dataframe(filtered_df, height=500)
