
# --- Page Setup ---
st.set_page_config(page_title="Branch Yearly Sales Report", layout="wide")
st.title("📊 Branch Yearly Sales Insights")

# --- Load Data ---
df = pd.read_excel("Sales 2024 Vs 2025 (1).Xlsx")  # Replace with your file

# --- Sidebar Filters ---
branches = df["Branch"].unique().tolist()
branches = ["All Branches"] + branches
selected_branch = st.sidebar.selectbox("Select Branch", branches)

years = ["2023", "2024", "2025"]
selected_years = st.sidebar.multiselect("Select Year(s)", years, default=years)

# --- Filter Data by Branch ---
filtered_df = df.copy()
if selected_branch != "All Branches":
    filtered_df = filtered_df[filtered_df["Branch"] == selected_branch]

# --- Prepare Metrics for Insights ---
metrics = ["Total Sales", "Avg Sales", "Mar(%)"]

# Initialize dictionaries to store totals
totals = {}
for year in selected_years:
    totals[year] = {}
    for metric in metrics:
        col_name = f"{year} 01-JAN to 31-AUG {metric}"
        if metric != "Mar(%)":
            totals[year][metric] = filtered_df[col_name].sum()
        else:
            totals[year][metric] = filtered_df[col_name].mean()

# Calculate differences between years (for Total Sales)
diffs = {}
for i in range(1, len(selected_years)):
    year_prev = selected_years[i-1]
    year_curr = selected_years[i]
    diffs[f"{year_curr}-{year_prev}"] = totals[year_curr]["Total Sales"] - totals[year_prev]["Total Sales"]

# Compute Average Sales as Total Sales ÷ 269
for year in selected_years:
    totals[year]["Average Sales"] = totals[year]["Total Sales"] / 269

# --- Display Key Insights ---
st.subheader("Key Insights")
cols = st.columns(len(selected_years))
for idx, year in enumerate(selected_years):
    diff_text = ""
    if idx > 0:
        prev_year = selected_years[idx-1]
        diff_val = diffs[f"{year}-{prev_year}"]
        diff_text = f"{diff_val:,.2f}"
    cols[idx].metric(f"Total Sales {year}", f"{totals[year]['Total Sales']:,.2f}", diff_text)

cols_avg = st.columns(len(selected_years))
for idx, year in enumerate(selected_years):
    cols_avg[idx].metric(f"Average Sales {year}", f"{totals[year]['Average Sales']:,.2f}")

cols_margin = st.columns(len(selected_years))
for idx, year in enumerate(selected_years):
    cols_margin[idx].metric(f"Avg Margin {year} (%)", f"{totals[year]['Mar(%)']:.2f}%")

st.markdown("---")

# --- Horizontal Bar Charts Function ---
def plot_horizontal_bar(data, x_col, y_col, color_col, title, color_scale):
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
for metric in metrics:
    chart_data = []
    if selected_branch == "All Branches":
        # Aggregate by Branch
        for b in filtered_df["Branch"].unique():
            branch_data = {"Branch": b}
            for year in selected_years:
                col_name = f"{year} 01-JAN to 31-AUG {metric}"
                if metric != "Mar(%)":
                    branch_data[year] = filtered_df[filtered_df["Branch"] == b][col_name].sum()
                else:
                    branch_data[year] = filtered_df[filtered_df["Branch"] == b][col_name].mean()
            chart_data.append(branch_data)
        chart_df = pd.DataFrame(chart_data)
        for year in selected_years:
            st.subheader(f"{metric} - {year}")
            plot_horizontal_bar(chart_df, year, "Branch", year, f"{metric} ({year})", "Viridis" if metric=="Total Sales" else "Blues")
    else:
        # Single branch - show metrics per year
        branch_data = {"Metric": metric}
        for year in selected_years:
            col_name = f"{year} 01-JAN to 31-AUG {metric}"
            branch_data[year] = filtered_df.iloc[0][col_name]
        st.subheader(f"{metric} - {selected_branch}")
        st.bar_chart(pd.DataFrame(branch_data, index=[0]).set_index("Metric"))

st.markdown("---")

# --- Show Filtered Data ---
st.subheader("Branch-wise Data")
st.dataframe(filtered_df, height=500)
