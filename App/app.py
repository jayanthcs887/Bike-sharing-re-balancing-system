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
st.markdown("""
<style>
.main {
    background-color: #0E1117;
}

.metric-card {
    background: linear-gradient(135deg,#1F2937,#111827);
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #374151;
    text-align: center;
    margin-bottom: 15px;
}

.metric-value {
    font-size: 32px;
    font-weight: bold;
    color: white;
}

.metric-label {
    color: #9CA3AF;
}

.insight-box {
    padding:15px;
    border-radius:10px;
    margin:10px 0;
    background:#1F2937;
}
</style>
""", unsafe_allow_html=True)

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
    st.markdown("""
    # 🚲 Bike Sharing Rebalancing Analytics
    
    ### Urban Mobility Intelligence Dashboard
    
    Monitor demand, analyze station performance, identify deficits, and optimize bike redistribution.
    """)

    total_trips = len(df)
    total_bikes = df["Bike number"].nunique()

    stations = pd.concat([
        df["Start station"],
        df["End station"]
    ]).nunique()

    peak_hour = df["Hour"].value_counts().idxmax()

    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_trips:,}</div>
            <div class="metric-label">🚲 Total Trips</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_bikes}</div>
            <div class="metric-label">🔧 Unique Bikes</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{stations}</div>
            <div class="metric-label">🏢 Stations</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{peak_hour}:00</div>
            <div class="metric-label">⏰ Peak Hour</div>
        </div>
        """, unsafe_allow_html=True)

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

    st.plotly_chart(fig, width="stretch")

# -----------------------------------
# DEMAND ANALYTICS
# -----------------------------------

elif page == "Demand Analytics":

    st.title("📈 Demand Analytics")
    df["Weekday"] = df["Start date"].dt.day_name()
    weekday_order = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
    ]

    df["Weekday"] = pd.Categorical(
        df["Weekday"],
        categories=weekday_order,
        ordered=True
    )

    heatmap = pd.crosstab(
    df["Weekday"],
    df["Hour"]
    )

    heatmap = heatmap.reindex(weekday_order)
    
    fig = px.imshow(
    heatmap,
    title="Demand Heatmap: Trips by Hour and Weekday",
    aspect="auto",
    labels={
        "x": "Hour of Day",
        "y": "Weekday",
        "color": "Trips"
    }
    )
    
    fig.update_layout(
        template="plotly_dark",
        height=500
    )
    
    st.plotly_chart(fig, width="stretch")

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

    st.plotly_chart(fig, width="stretch")

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

    st.plotly_chart(fig2, width="stretch")

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

    st.plotly_chart(fig, width="stretch")

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

    st.plotly_chart(fig, width="stretch")

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

    # Fix Streamlit Cloud / Pandas 3.x issue
    flow["Checkouts"] = flow["Checkouts"].fillna(0)
    flow["Checkins"] = flow["Checkins"].fillna(0)
    
    flow["Start station"] = flow["Start station"].fillna("")
    flow["End station"] = flow["End station"].fillna("")

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
    st.markdown("""
    <div class='insight-box'>
    🚀 Peak demand occurs during morning commuting hours.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='insight-box'>
    ⚠ Certain stations consistently experience negative net flow.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='insight-box'>
    📈 Top stations account for a significant portion of all trips.
    </div>
    """, unsafe_allow_html=True)

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
