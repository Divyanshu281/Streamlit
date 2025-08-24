import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout='wide', page_title='🚀 Startup Funding Dashboard')

df = pd.read_csv('cleaned_startup.csv')
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

investors = sorted(set(i.strip() for inv in df['investors'].dropna() for i in inv.split(',')))
cities = sorted(df['city'].dropna().unique())

# Sidebar filters
st.sidebar.header("🔎 Filters")
selected_year = st.sidebar.multiselect("Select Year", sorted(df['year'].dropna().unique()), default=sorted(df['year'].dropna().unique()))
selected_city = st.sidebar.multiselect("Select City", cities, default=cities)
amount_range = st.sidebar.slider("Select Investment Amount Range (Cr)", 
                                 int(df['amount'].min()), int(df['amount'].max()), 
                                 (int(df['amount'].min()), int(df['amount'].max())))

df_filtered = df[(df['year'].isin(selected_year)) &
                 (df['city'].isin(selected_city)) &
                 (df['amount'].between(amount_range[0], amount_range[1]))]

# ================= Overall Analysis =================
def load_overall_analysis():
    st.title("📊 Overall Startup Funding Analysis")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Total Investment", f"{round(df_filtered['amount'].sum())} Cr")
    col2.metric("🚀 Funded Startups", df_filtered['startup'].nunique())
    col3.metric("🏦 No. of Investors", len(investors))
    col4.metric("📅 Time Period", f"{df['year'].min()} - {df['year'].max()}")

    # MoM Trend
    st.subheader("📈 Month-on-Month Trend")
    temp = df_filtered.groupby(['year','month'])['amount'].sum().reset_index()
    temp['period'] = pd.to_datetime(temp[['year','month']].assign(day=1))

    fig = px.line(temp, x="period", y="amount", markers=True, title="Investment Trend")
    st.plotly_chart(fig, use_container_width=True)

    # City wise investments
    st.subheader("🌍 Top Cities by Funding")
    city_series = df_filtered.groupby('city')['amount'].sum().sort_values(ascending=False).head(10)
    fig2 = px.bar(city_series, x=city_series.index, y=city_series.values, text=city_series.values, title="Top Cities")
    st.plotly_chart(fig2, use_container_width=True)


# ================= Investor Analysis =================
def load_investor_details(investor):
    st.title(f"🤑 {investor} - Investor Profile")

    inv_df = df[df['investors'].str.contains(investor, na=False)]

    col1, col2, col3 = st.columns(3)
    col1.metric("💸 Total Invested", f"{round(inv_df['amount'].sum())} Cr")
    col2.metric("🚀 No. of Startups Funded", inv_df['startup'].nunique())
    col3.metric("🎯 Biggest Deal", f"{inv_df['amount'].max()} Cr")

    st.subheader("📅 Recent Investments")
    st.dataframe(inv_df.sort_values("date", ascending=False).head(10))

    st.subheader("🏢 Top Startups Funded")
    top_startups = inv_df.groupby("startup")['amount'].sum().sort_values(ascending=False).head(10)
    fig = px.bar(top_startups, x=top_startups.index, y=top_startups.values, text=top_startups.values)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📊 Sector Split")
    vertical_series = inv_df.groupby("vertical")['amount'].sum().sort_values(ascending=False).head(7)
    fig2 = px.pie(vertical_series, values=vertical_series.values, names=vertical_series.index, hole=0.4)
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("📈 YoY Trend")
    yoy = inv_df.groupby("year")['amount'].sum().cumsum()
    fig3 = px.line(yoy, x=yoy.index, y=yoy.values, markers=True, title="Cumulative Investments")
    st.plotly_chart(fig3, use_container_width=True)

    st.download_button("⬇️ Download Investor Data", inv_df.to_csv(index=False), file_name=f"{investor}_data.csv")


# ================= Main App =================
st.sidebar.title("📌 Navigation")
options = st.sidebar.radio("Go To", ["Overall Analysis", "Investor Analysis"])

if options == "Overall Analysis":
    load_overall_analysis()
else:
    selected_investor = st.sidebar.selectbox("Select Investor", investors)
    if st.sidebar.button("Show Investor Details"):
        load_investor_details(selected_investor)
