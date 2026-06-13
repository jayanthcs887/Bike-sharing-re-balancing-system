import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="Bike Sharing Analytics Dashboard",
    page_icon="🚲",
    layout="wide"
)

# -----------------------------------
# LOAD DATA
# -----------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("data/201912-capitalbikeshare-tripdata.csv")

    df["Start date"] = pd.to_datetime(df["Start date"])
    df["End date"] = pd.to_datetime(df["End date"])

    df["Hour"] = df["Start date"].dt.hour
    df["Day"] = df["Start date"].dt.day_name()

    return df

df = load_data()

# -----------------------------------
# SIDEBAR
# -----------------------------------

st.sidebar.title("🚲 Navigation")

page = st.sidebar.radio(
    "Select Page",
    [
        "Dashboard",
        "Demand Analytics",
        "Station Analytics",
        "Bike Utilization",
        "Rebalancing Analysis",
        "Insights"
    ]
)

# -----------------------------------
# DASHBOARD
# -----------------------------------

if page == "Dashboard":

    st.title("🚲 Bike Sharing Analytics Dashboard")

    total_trips = len(df)
    total_bikes = df["Bike number"].nunique()

    stations = pd.concat([
        df["Start station"],
        df["End station"]
    ]).nunique()

    peak_hour = df["Hour"].value_counts().idxmax()

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Total Trips", f"{total_trips:,}")
    c2.metric("Unique Bikes", total_bikes)
    c3.metric("Stations", stations)
    c4.metric("Peak Hour", f"{peak_hour}:00")

    hourly = (
        df.groupby("Hour")
        .size()
        .reset_index(name="Trips")
    )

    fig = px.line(
        hourly,
        x="Hour",
        y="Trips",
        markers=True,
        title="Trips by Hour"
    )

    st.plotly_chart(fig, use_container_width=True)

# -----------------------------------
# DEMAND ANALYTICS
# -----------------------------------

elif page == "Demand Analytics":

    st.title("📈 Demand Analytics")

    hourly = (
        df.groupby("Hour")
        .size()
        .reset_index(name="Trips")
    )

    fig = px.bar(
        hourly,
        x="Hour",
        y="Trips",
        title="Hourly Demand"
    )

    st.plotly_chart(fig, use_container_width=True)

    daily = (
        df.groupby("Day")
        .size()
        .reset_index(name="Trips")
    )

    fig2 = px.pie(
        daily,
        names="Day",
        values="Trips",
        title="Trips Distribution by Day"
    )

    st.plotly_chart(fig2, use_container_width=True)

# -----------------------------------
# STATION ANALYTICS
# -----------------------------------

elif page == "Station Analytics":

    st.title("🏢 Station Analytics")

    top_stations = (
        df.groupby("Start station")
        .size()
        .reset_index(name="Trips")
        .sort_values(
            "Trips",
            ascending=False
        )
        .head(10)
    )

    fig = px.bar(
        top_stations,
        x="Trips",
        y="Start station",
        orientation="h",
        title="Top 10 Busy Stations"
    )

    st.plotly_chart(fig, use_container_width=True)

# -----------------------------------
# BIKE UTILIZATION
# -----------------------------------

elif page == "Bike Utilization":

    st.title("🔧 Bike Utilization Analysis")

    bike_usage = (
        df.groupby("Bike number")
        .size()
        .reset_index(name="Trips")
        .sort_values(
            "Trips",
            ascending=False
        )
        .head(20)
    )

    fig = px.bar(
        bike_usage,
        x="Bike number",
        y="Trips",
        title="Top 20 Most Utilized Bikes"
    )

    st.plotly_chart(fig, use_container_width=True)

# -----------------------------------
# REBALANCING ANALYSIS
# -----------------------------------

elif page == "Rebalancing Analysis":

    st.title("⚠ Rebalancing Analysis")

    checkouts = (
        df.groupby("Start station")
        .size()
        .reset_index(name="Checkouts")
    )

    checkins = (
        df.groupby("End station")
        .size()
        .reset_index(name="Checkins")
    )

    flow = pd.merge(
        checkouts,
        checkins,
        left_on="Start station",
        right_on="End station",
        how="outer"
    )

    flow.fillna(0, inplace=True)

    flow["Station"] = flow["Start station"].fillna(
        flow["End station"]
    )

    flow["Net Flow"] = (
        flow["Checkins"]
        - flow["Checkouts"]
    )

    deficit = (
        flow.sort_values("Net Flow")
        .head(10)
    )

    overflow = (
        flow.sort_values(
            "Net Flow",
            ascending=False
        )
        .head(10)
    )

    st.subheader("Deficit Stations")

    st.dataframe(
        deficit[
            ["Station","Net Flow"]
        ]
    )

    st.subheader("Overflow Stations")

    st.dataframe(
        overflow[
            ["Station","Net Flow"]
        ]
    )

# -----------------------------------
# INSIGHTS
# -----------------------------------

elif page == "Insights":

    st.title("💡 Business Insights")

    peak_hour = (
        df["Hour"]
        .value_counts()
        .idxmax()
    )

    busiest_station = (
        df["Start station"]
        .value_counts()
        .idxmax()
    )

    top_member = (
        df["Member type"]
        .value_counts()
        .idxmax()
    )

    st.success(
        f"Peak demand occurs around {peak_hour}:00."
    )

    st.info(
        f"Most active station: {busiest_station}"
    )

    st.warning(
        f"Majority rider category: {top_member}"
    )

    st.markdown("""
    ### Recommendations

    - Rebalance bikes before peak hours.
    - Add more docks at busy stations.
    - Monitor heavily used bikes.
    - Increase bike availability at deficit stations.
    - Plan maintenance for frequently used bikes.
    """)
