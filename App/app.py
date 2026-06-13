import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="Bike Sharing Rebalancing System",
    page_icon="🚲",
    layout="wide"
)

# ----------------------------
# LOAD DATA
# ----------------------------

@st.cache_data
def load_data():
    df = pd.read_csv(
        "data/202601-capitalbikeshare-tripdata.csv"
    )

    return df

df = load_data()

# ----------------------------
# PREPROCESS
# ----------------------------

time_cols = []

for col in df.columns:
    if "start" in col.lower():
        time_cols.append(col)

    if "end" in col.lower():
        time_cols.append(col)

for col in time_cols:
    try:
        df[col] = pd.to_datetime(df[col])
    except:
        pass

start_time_col = time_cols[0]

df["hour"] = df[start_time_col].dt.hour

# ----------------------------
# SIDEBAR
# ----------------------------

st.sidebar.title("🚲 Bike Rebalancing")

page = st.sidebar.radio(
    "Navigation",
    [
        "Overview",
        "Demand Analytics",
        "Station Intelligence",
        "Rebalancing Center",
        "Insights"
    ]
)

# ----------------------------
# OVERVIEW
# ----------------------------

if page == "Overview":

    st.title("🚲 Bike Sharing Rebalancing Dashboard")

    col1,col2,col3,col4 = st.columns(4)

    total_trips = len(df)

    total_bikes = (
        df["Bike_ID"].nunique()
        if "Bike_ID" in df.columns
        else 0
    )

    stations = []

    if "Start_Station_ID" in df.columns:
        stations.extend(
            df["Start_Station_ID"].unique()
        )

    if "End_Station_ID" in df.columns:
        stations.extend(
            df["End_Station_ID"].unique()
        )

    total_stations = len(set(stations))

    peak_hour = (
        df["hour"]
        .value_counts()
        .idxmax()
    )

    col1.metric("Trips", f"{total_trips:,}")
    col2.metric("Bikes", total_bikes)
    col3.metric("Stations", total_stations)
    col4.metric("Peak Hour", f"{peak_hour}:00")

    hourly = (
        df.groupby("hour")
        .size()
        .reset_index(name="Trips")
    )

    fig = px.line(
        hourly,
        x="hour",
        y="Trips",
        title="Hourly Demand Trend"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ----------------------------
# DEMAND ANALYTICS
# ----------------------------

elif page == "Demand Analytics":

    st.title("📈 Demand Analytics")

    hourly = (
        df.groupby("hour")
        .size()
        .reset_index(name="Trips")
    )

    fig = px.bar(
        hourly,
        x="hour",
        y="Trips",
        title="Trips by Hour"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ----------------------------
# STATION ANALYTICS
# ----------------------------

elif page == "Station Intelligence":

    st.title("🏢 Station Intelligence")

    start_col = "Start_Station_ID"

    station_usage = (
        df.groupby(start_col)
        .size()
        .reset_index(name="Trips")
        .sort_values(
            "Trips",
            ascending=False
        )
        .head(10)
    )

    fig = px.bar(
        station_usage,
        x=start_col,
        y="Trips",
        title="Top 10 Busy Stations"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ----------------------------
# REBALANCING
# ----------------------------

elif page == "Rebalancing Center":

    st.title("⚠ Rebalancing Center")

    outs = (
        df.groupby("Start_Station_ID")
        .size()
        .reset_index(name="Checkouts")
    )

    ins = (
        df.groupby("End_Station_ID")
        .size()
        .reset_index(name="Checkins")
    )

    flow = pd.merge(
        outs,
        ins,
        left_on="Start_Station_ID",
        right_on="End_Station_ID",
        how="outer"
    )

    flow = flow.fillna(0)

    flow["NetFlow"] = (
        flow["Checkins"]
        - flow["Checkouts"]
    )

    deficit = (
        flow.sort_values("NetFlow")
        .head(5)
    )

    overflow = (
        flow.sort_values(
            "NetFlow",
            ascending=False
        )
        .head(5)
    )

    st.subheader("Critical Deficit Stations")
    st.dataframe(deficit)

    st.subheader("Overflow Stations")
    st.dataframe(overflow)

# ----------------------------
# INSIGHTS
# ----------------------------

elif page == "Insights":

    st.title("💡 Operational Insights")

    peak_hour = (
        df["hour"]
        .value_counts()
        .idxmax()
    )

    st.success(
        f"Peak demand occurs around {peak_hour}:00."
    )

    st.info(
        "High-demand stations should receive additional bikes before peak periods."
    )

    st.warning(
        "Stations with sustained negative net flow require rebalancing."
    )

    st.markdown(
        """
        ### Recommendations

        - Schedule bike transfers before morning rush hours.
        - Monitor top deficit stations continuously.
        - Increase dock capacity at busy stations.
        - Deploy maintenance teams near high-utilization stations.
        """
    )
