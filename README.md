# 🚲 Bike Sharing Rebalancing Analytics System

## 📌 Project Overview

The Bike Sharing Rebalancing Analytics System is a data-driven dashboard developed to analyze bike-sharing operations and identify station-level imbalances using historical trip data.

The system provides actionable insights into rider demand, station utilization, bike usage patterns, and operational bottlenecks. By analyzing trip origins, destinations, and usage trends, transportation operators can optimize bike distribution and improve service availability across the network.

---

## 🎯 Problem Statement

Bike-sharing systems often face operational challenges where:

* Some stations become empty due to high demand.
* Some stations become overcrowded due to excess returns.
* Bikes are unevenly distributed across stations.
* Operators struggle to identify high-demand areas.

This project analyzes historical trip data and generates insights that support efficient bike redistribution strategies.

---

## 🚀 Features

### 📊 Executive Dashboard

* Total Trips
* Total Bikes
* Total Stations
* Peak Demand Hour
* Interactive KPI Cards

### 📈 Demand Analytics

* Hourly Demand Analysis
* Daily Usage Trends
* Rider Activity Distribution
* Peak Usage Identification

### 🏢 Station Intelligence

* Top 10 Most Active Stations
* Station Traffic Analysis
* High Demand Station Identification
* Station Performance Comparison

### 🔧 Bike Utilization Analysis

* Most Utilized Bikes
* Fleet Usage Statistics
* Maintenance Planning Support

### ⚠ Rebalancing Analysis

* Deficit Stations Detection
* Overflow Stations Detection
* Net Flow Analysis
* Redistribution Recommendations

### 💡 Business Insights

* Peak Traffic Periods
* User Behavior Patterns
* Operational Recommendations
* Resource Optimization Suggestions

---

## 📂 Dataset Information

Dataset Used:

**201912-capitalbikeshare-tripdata.csv**

### Dataset Attributes

| Column               | Description              |
| -------------------- | ------------------------ |
| Duration             | Trip duration            |
| Start date           | Trip start timestamp     |
| End date             | Trip end timestamp       |
| Start station number | Origin station ID        |
| Start station        | Origin station name      |
| End station number   | Destination station ID   |
| End station          | Destination station name |
| Bike number          | Bike identifier          |
| Member type          | Casual or Member rider   |

---

## 📊 Analytics Performed

### Demand Analysis

* Hour-wise trip distribution
* Daily usage patterns
* Peak demand identification

### Station Analysis

* Station-wise trip count
* Most active stations
* Station load balancing

### Rebalancing Analysis

Net Flow Calculation:

Net Flow = Check-ins − Check-outs

Classification:

* Positive Net Flow → Overflow Station
* Negative Net Flow → Deficit Station

### Fleet Utilization Analysis

* Bike usage frequency
* High-utilization bikes
* Maintenance indicators

---

## 🛠️ Technologies Used

* Python
* Streamlit
* Pandas
* NumPy
* Plotly

---

## 📁 Project Structure

```text
Bike-Sharing-Analytics/
│
├── app.py
├── requirements.txt
├── README.md
│
├── 201912-capitalbikeshare-tripdata.csv
│
└── screenshots/
    ├── dashboard.png
    ├── overview.png
    ├── station_analysis.png
    └── rebalancing.png
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/Bike-Sharing-Analytics.git

cd Bike-Sharing-Analytics
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
streamlit run app.py
```

---

## 📸 Dashboard Screenshots

### Dashboard

![Dashboard](screenshots/dashboard.png)

### Overview

![Overview](screenshots/overview.png)

### Station Analysis

![Station Analysis](screenshots/station_analysis.png)

### Rebalancing Analysis

![Rebalancing](screenshots/rebalancing.png)

---

## 💡 Key Insights

* Peak demand occurs during commuting hours.
* Certain stations consistently experience bike shortages.
* A small number of stations account for a significant share of total trips.
* Bike utilization is highly concentrated among specific bikes.
* Rebalancing operations can improve bike availability and user satisfaction.

---

## 🔮 Future Enhancements

* Demand Forecasting
* Predictive Analytics
* Route Optimization
* Real-Time Monitoring
* Interactive Maps
* Maintenance Prediction Models

---

## 👨‍💻 Team

Hackathon Project – Bike Sharing Rebalancing Analytics System

Developed using Python, Streamlit, and Data Analytics techniques to improve operational efficiency in urban bike-sharing networks.
## Team members
* Jayanth C S
* Dheeraj M
* Monaj S S
* R P Pavan Kumar

---
