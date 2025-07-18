# --- Import libraries ---
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# --- Load the original dataset ---
df = pd.read_csv("../week1 project/WorldExpenditures.csv")

# --- Page Title ---
st.title("🌍 World Expenditures Analysis - Week 1 Project")
st.header("Initial Data Overview")

# --- Show Raw Data Info Before Cleaning ---
st.write("### Original Dataset Shape:")
st.write(df.shape)

st.write("### Sample of Raw Data:")
st.write(df.head())

st.write("### Missing Values:")
st.write(df.isnull().sum())

st.write("### Data Types:")
st.write(df.dtypes)

# --- Data Cleaning ---
df.drop(columns=["Unnamed: 0"], inplace=True, errors='ignore')  # Drop unnecessary column if exists
df.dropna(subset=["Expenditure(million USD)", "GDP(%)"], inplace=True)
df.drop_duplicates(inplace=True)
df = df[df["Sector"].str.strip().str.lower() != "total function"]  # Remove "Total function"

# --- Save Cleaned File (Optional) ---
df.to_csv("WorldExpenditures_CLEAN.csv", index=False)

# --- Show Updated Info ---
st.header("🧹 Data Cleaned Successfully")
st.write("### Cleaned Dataset Shape:")
st.write(df.shape)

st.write("### Remaining Missing Values:")
st.write(df.isnull().sum())

st.write("### Number of Exact Duplicate Rows:")
st.write(df.duplicated().sum())

# --- Statistics AFTER Cleaning ---
st.header("📊 Basic Statistics (After Cleaning)")

# Exclude non-numeric or unwanted columns (like 'Year')
numeric_cols = [col for col in df.select_dtypes(include=np.number).columns if col != 'Year']

st.subheader("Mean:")
st.write(df[numeric_cols].mean())

st.subheader("Median:")
st.write(df[numeric_cols].median())

st.subheader("Mode:")
st.write(df[numeric_cols].mode().iloc[0])  # First mode row

# --- Visualizations ---
st.header("📈 Basic Visualizations")

# Histogram of Expenditure
fig1, ax1 = plt.subplots()
df["Expenditure(million USD)"].hist(ax=ax1, bins=30, color='skyblue', edgecolor='black')
ax1.set_title("Distribution of Expenditure")
ax1.set_xlabel("Expenditure (Million USD)")
ax1.set_ylabel("Frequency")
st.pyplot(fig1)

# Correlation heatmap (excluding Year)
fig2, ax2 = plt.subplots()
sns.heatmap(df[numeric_cols].corr(), annot=True, cmap="coolwarm", ax=ax2)
ax2.set_title("Correlation Heatmap")
st.pyplot(fig2)

# --- Question 1: Top 5 Countries by Total Expenditure ---
st.header("📌 Question 1: Top 5 Countries by Total Expenditure")

top5_countries = (
    df.groupby("Country")["Expenditure(million USD)"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

st.dataframe(top5_countries)

fig3, ax3 = plt.subplots()
top5_countries.plot(kind='bar', ax=ax3, color='lightgreen')
ax3.set_title("Top 5 Countries by Total Expenditure")
ax3.set_ylabel("Expenditure (Million USD)")
st.pyplot(fig3)

st.markdown("**Insight:** The United States leads in total expenditure, followed by China, Japan, Germany, and France.")

# --- Question 2: Top 5 Sectors by Average Expenditure ---
st.header("📌 Question 2: Top 5 Sectors by Average Expenditure")

top_avg_sectors = (
    df.groupby("Sector")["Expenditure(million USD)"]
    .mean()
    .sort_values(ascending=False)
    .head(5)
)

st.dataframe(top_avg_sectors)

fig4, ax4 = plt.subplots()
top_avg_sectors.plot(kind='bar', ax=ax4, color='orange')
ax4.set_title("Top 5 Sectors by Average Expenditure")
ax4.set_ylabel("Average Expenditure (Million USD)")
st.pyplot(fig4)

st.markdown("**Insight:** Social protection, Education, and Health remain among the highest average spending sectors.")


import plotly.express as px
import plotly.graph_objects as go

# --- Question 3: Most Stable Spending Sectors ---
st.header("📌 Q3: Most Stable Spending Sectors")

sector_variation = (
    df.groupby("Sector")["Expenditure(million USD)"].std().sort_values()
)

fig_q3 = px.bar(
    sector_variation,
    title="Sectors with the Most Stable Spending (Lowest Std Dev)",
    labels={"value": "Standard Deviation", "Sector": ""},
    color=sector_variation.values,
    color_continuous_scale="Blues",
)

fig_q3.update_layout(xaxis_title="Sector", yaxis_title="Standard Deviation")

st.plotly_chart(fig_q3)

st.markdown("**Insight:** Lower standard deviation values indicate more consistent spending across years.")

# --- Question 4: Average GDP% per Sector Globally ---
st.header("📌 Q4: Average GDP% per Sector Globally")

avg_gdp_per_sector = (
    df.groupby("Sector")["GDP(%)"].mean().sort_values(ascending=False)
)

fig_q4 = px.pie(
    names=avg_gdp_per_sector.index,
    values=avg_gdp_per_sector.values,
    title="Average GDP% Spent Per Sector (Global)",
    hole=0.4,
    color_discrete_sequence=px.colors.sequential.RdBu,
)

st.plotly_chart(fig_q4)

st.markdown("**Insight:** This view shows which sectors receive the highest proportional GDP spending on average.")

# --- Optional: Dropdown to explore GDP% by country ---
st.header("🌐 Explore GDP% by Sector and Country")

selected_country = st.selectbox("Select a Country:", df["Country"].unique())

country_sector_gdp = df[df["Country"] == selected_country]

fig_country = px.bar(
    country_sector_gdp,
    x="Sector",
    y="GDP(%)",
    color="GDP(%)",
    title=f"GDP% Allocation by Sector - {selected_country}",
    labels={"GDP(%)": "% of GDP"},
    color_continuous_scale="Viridis"
)

fig_country.update_layout(xaxis_tickangle=-45)

st.plotly_chart(fig_country)

st.markdown("**Tip:** Use the dropdown to explore how different countries allocate GDP across sectors.")

