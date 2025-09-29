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
    "2023 Avg Sales": [
        145131.92, 47557.67, 114952.22, 35393.20, 59992.56, 23033.44,
        38269.96, 41732.51, 27821.39, 22563.94, 67147.62,
        22052.98, 0, 109818.31, 0, 0, 755467.70
    ],
    "2023 Mar(%)": [
        19.95, 20.92, 19.77, 17.65, 16.36, 19.36,
        19.17, 21.74, 21.32, 20.83, 20.72,
        20.34, 0, 17.49, 0, 0, 19.42
    ],
    "2024 Total Sales": [
        34639834.01, 13065728.25, 29616414.52, 12060825.99, 14851756.73, 5753112.33,
        9948602.69, 10876887.59, 6741894.61, 6292322.86, 17859351.69,
        6148201.78, 5533772.24, 33194831.22, 4640301.45, 0, 211223837.96
    ],
    "2024 Avg Sales": [
        141966.53, 53548.07, 121378.75, 49429.61, 60867.86, 23578.33,
        40772.96, 44577.41, 27630.72, 25788.21, 73194.06,
        25197.55, 22679.39, 136044.39, 38349.60, 0, 885003.44
    ],
    "2024 Mar(%)": [
        20.94, 20.68, 17.88, 17.44, 16.05, 19.10,
        19.60, 21.47, 21.37, 23.06, 19.49,
        21.15, 17.18, 18.00, 15.44, 0, 19.14
    ],
    "2025 Total Sales": [
        31162845.37, 10289632.43, 27783796.93, 10570459.29, 13602032.89, 4564110.21,
        9042951.59, 10270157.40, 6337346.41, 5889305.34, 17966957.48,
        6571452.28, 6159775.78, 34964501.80, 9708622.47, 9789990.97, 214673938.64
    ],
    "2025 Avg Sales": [
        128242.16, 42344.17, 114336.61, 43499.83, 55975.44, 18782.35,
        37213.79, 42264.02, 26079.61, 24235.82, 73938.10,
        27043.01, 25348.87, 143886.84, 39953.18, 40288.03, 883431.85
    ],
    "2025 Mar(%)": [
        21.39, 22.65, 19.72, 18.75, 16.61, 19.79,
        19.83, 23.04, 21.19, 24.60, 20.66,
        21.82, 19.38, 19.99, 18.22, 24.59, 20.53
    ],
    "DIFFERENCE Total Sales": [
        -3476988.64, -2776095.82, -1832617.59, -1490366.70, -1249723.84, -1189002.12,
        -905651.10, -606730.19, -404548.20, -403017.52, 107605.79,
        423250.50, 626003.54, 1769670.58, 5068321.02, 9789990.97, -6339890.29
    ],
    "DIFFERENCE Avg Sales": [
        -13724.37, -11203.90, -7042.14, -5929.78, -4892.41, -4795.98,
        -3559.17, -2313.39, -1551.10, -1552.38, 744.03,
        1845.47, 2669.48, 7842.45, 1603.58, 40288.03, -41859.62
    ],
    "DIFFERENCE Mar(%)": [
        0.45, 1.97, 1.84, 1.32, 0.56, 0.69,
        0.23, 1.57, -0.17, 1.54, 1.17,
        0.67, 2.20, 1.99, 2.78, 24.59, 19.14
    ]
}

df = pd.DataFrame(data)

# --- Sidebar Filter (Only Branches, No "All") ---
branches = df["Branch"].tolist()[:-1]  # Exclude Grand Total
selected_branch = st.sidebar.selectbox("Select Branch", branches)

# Filter for selected branch (for key metrics only)
filtered_df = df[df["Branch"] == selected_branch]

# --- Key Metrics ---
st.subheader("📌 Key Metrics")
metrics1 = st.columns(3)
metrics1[0].metric("2023 Total Sales", f"{filtered_df['2023 Total Sales'].sum():,.2f}")
metrics1[1].metric("2023 Avg Sales", f"{filtered_df['2023 Avg Sales'].sum():,.2f}")
metrics1[2].metric("2023 Margin (%)", f"{filtered_df['2023 Mar(%)'].sum():.2f}")

metrics2 = st.columns(3)
metrics2[0].metric("2024 Total Sales", f"{filtered_df['2024 Total Sales'].sum():,.2f}")
metrics2[1].metric("2024 Avg Sales", f"{filtered_df['2024 Avg Sales'].sum():,.2f}")
metrics2[2].metric("2024 Margin (%)", f"{filtered_df['2024 Mar(%)'].sum():.2f}")

metrics3 = st.columns(3)
metrics3[0].metric("2025 Total Sales", f"{filtered_df['2025 Total Sales'].sum():,.2f}")
metrics3[1].metric("2025 Avg Sales", f"{filtered_df['2025 Avg Sales'].sum():,.2f}")
metrics3[2].metric("2025 Margin (%)", f"{filtered_df['2025 Mar(%)'].sum():.2f}")

metrics4 = st.columns(3)
metrics4[0].metric("Difference Total Sales", f"{filtered_df['DIFFERENCE Total Sales'].sum():,.2f}")
metrics4[1].metric("Difference Avg Sales", f"{filtered_df['DIFFERENCE Avg Sales'].sum():,.2f}")
metrics4[2].metric("Difference Margin (%)", f"{filtered_df['DIFFERENCE Mar(%)'].sum():,.2f}")

st.markdown("---")

# --- Function to Plot Horizontal Bar Charts ---
def plot_horizontal_bar(df, column, title, color_scale):
    fig = px.bar(
        df,
        x=column,
        y="Branch",
        orientation='h',
        text=column,
        color=column,
        color_continuous_scale=color_scale
    )
    fig.update_traces(texttemplate='%{text:,.2f}', textposition='outside')
    fig.update_layout(
        height=600,
        yaxis={'categoryorder':'total ascending'},
        margin=dict(l=150, r=50, t=50, b=50),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("<br>", unsafe_allow_html=True)

# --- Graphs Section (Always All Branches) ---
st.subheader("📊 Branch Comparison Charts (All Branches)")
for year, color in zip(["2023", "2024", "2025"], ["Viridis", "Blues", "Greens"]):
    st.markdown(f"### {year} Sales Metrics")
    plot_horizontal_bar(df[:-1], f"{year} Total Sales", f"{year} Total Sales", color)  # exclude Grand Total
    plot_horizontal_bar(df[:-1], f"{year} Avg Sales", f"{year} Avg Sales", color)
    plot_horizontal_bar(df[:-1], f"{year} Mar(%)", f"{year} Margin (%)", color)
