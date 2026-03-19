import streamlit as st
import pandas as pd
import numpy as np
import requests
import pydeck as pdk
import time
from datetime import datetime

# ===============================
# CONFIG
# ===============================

NEWS_API_KEY = "YOUR_NEWSAPI_KEY"

country_coordinates = {
    "Ukraine": [50.45, 30.52],
    "Russia": [55.75, 37.61],
    "Iran": [35.68, 51.41],
    "Israel": [31.76, 35.21],
    "China": [39.90, 116.40],
    "Taiwan": [25.03, 121.56],
    "USA": [38.90, -77.03],
    "India": [28.61, 77.20],
    "North Korea": [39.03, 125.75],
    "South Korea": [37.56, 126.97]
}

# economic dependencies (simplified)
economic_dependencies = {
    "oil": ["USA","China","India","Europe"],
    "gas": ["Germany","France","Italy"],
    "semiconductors": ["USA","China","Japan"],
    "shipping": ["Global"]
}

conflict_keywords = [
    "war","attack","military","missile","invasion",
    "airstrike","troops","conflict","bomb","sanctions"
]

# ===============================
# PAGE CONFIG
# ===============================

st.set_page_config(
    page_title="Global Conflict Intelligence System",
    layout="wide"
)

st.title("🌍 Global Conflict Impact Intelligence System")
st.markdown("Real-time geopolitical risk monitoring")

# ===============================
# NEWS FETCHER
# ===============================

@st.cache_data(ttl=300)
def fetch_news():

    url = f"https://newsapi.org/v2/everything?q=war OR conflict OR military&language=en&apiKey={NEWS_API_KEY}"

    r = requests.get(url)
    data = r.json()

    articles = []

    for a in data.get("articles", []):
        articles.append({
            "title": a["title"],
            "source": a["source"]["name"],
            "time": a["publishedAt"],
            "content": a["title"] + " " + str(a["description"])
        })

    return pd.DataFrame(articles)

# ===============================
# CONFLICT SCORING AI
# ===============================

def calculate_conflict_score(text):

    score = 0

    for k in conflict_keywords:
        if k in text.lower():
            score += 1

    return score

# ===============================
# COUNTRY DETECTION
# ===============================

def detect_country(text):

    for country in country_coordinates:
        if country.lower() in text.lower():
            return country

    return None


# ===============================
# PROCESS NEWS
# ===============================

def process_news(df):

    heatmap_data = []

    conflict_events = []

    for _,row in df.iterrows():

        text = row["content"]

        score = calculate_conflict_score(text)

        country = detect_country(text)

        if country:

            lat,lon = country_coordinates[country]

            heatmap_data.append({
                "lat":lat,
                "lon":lon,
                "intensity":score + 1
            })

            conflict_events.append({
                "country":country,
                "risk_score":score,
                "headline":row["title"],
                "time":row["time"]
            })

    return pd.DataFrame(heatmap_data), pd.DataFrame(conflict_events)


# ===============================
# SUPPLY CHAIN IMPACT
# ===============================

def supply_chain_risk(events):

    impacts = []

    for _,e in events.iterrows():

        country = e["country"]

        if country in ["Iran","Russia"]:
            impacts.append(("Oil Supply", "High Risk"))

        if country in ["China","Taiwan"]:
            impacts.append(("Semiconductors", "Critical Risk"))

        if country in ["Ukraine","Russia"]:
            impacts.append(("Food / Wheat Supply","Medium Risk"))

    return impacts


# ===============================
# ECONOMIC IMPACT ESTIMATION
# ===============================

def estimate_market_impact(events):

    risk = len(events)

    impact = {
        "Oil Price Pressure": risk * 2,
        "Stock Market Volatility": risk * 1.5,
        "Shipping Disruption": risk * 1.2,
        "Inflation Risk": risk * 1.1
    }

    return impact


# ===============================
# LOAD DATA
# ===============================

news_df = fetch_news()

heatmap_df,events_df = process_news(news_df)

# ===============================
# DASHBOARD LAYOUT
# ===============================

col1,col2,col3 = st.columns(3)

with col1:
    st.metric("Total Conflict Signals", len(events_df))

with col2:
    st.metric("Active Risk Zones", events_df["country"].nunique() if not events_df.empty else 0)

with col3:
    st.metric("News Events Processed", len(news_df))


# ===============================
# WORLD HEATMAP
# ===============================

st.subheader("🔥 Global Conflict Heatmap")

if not heatmap_df.empty:

    layer = pdk.Layer(
        "HeatmapLayer",
        data=heatmap_df,
        get_position='[lon, lat]',
        aggregation='"SUM"',
        get_weight="intensity"
    )

    view_state = pdk.ViewState(
        latitude=30,
        longitude=20,
        zoom=1.3
    )

    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state
    )

    st.pydeck_chart(r)

else:
    st.info("No conflict signals detected yet.")


# ===============================
# ECONOMIC IMPACT PANEL
# ===============================

st.subheader("📊 Economic Market Impact")

impact = estimate_market_impact(events_df)

impact_df = pd.DataFrame(list(impact.items()),columns=["Market","Risk Score"])

st.bar_chart(impact_df.set_index("Market"))


# ===============================
# SUPPLY CHAIN RISK
# ===============================

st.subheader("🚢 Supply Chain Risk Monitor")

risks = supply_chain_risk(events_df)

if risks:

    risk_df = pd.DataFrame(risks,columns=["Sector","Risk Level"])
    st.table(risk_df)

else:
    st.write("No major supply chain disruptions detected.")


# ===============================
# LIVE NEWS STREAM
# ===============================

st.subheader("📰 Live Conflict News Feed")

for _,row in news_df.head(10).iterrows():

    st.markdown(f"""
    **{row['title']}**

    Source: {row['source']}  
    Time: {row['time']}
    """)

    st.divider()


# ===============================
# AI WAR PREDICTION MODEL
# ===============================

st.subheader("🤖 AI Conflict Escalation Prediction")

if not events_df.empty:

    risk_score = events_df["risk_score"].sum()

    if risk_score > 15:
        prediction = "HIGH probability of escalation"
    elif risk_score > 7:
        prediction = "MODERATE escalation risk"
    else:
        prediction = "LOW escalation risk"

    st.warning(f"AI Prediction: {prediction}")

else:
    st.success("No escalation signals detected")


# ===============================
# AUTO REFRESH
# ===============================

st.caption("Dashboard auto-refresh every 5 minutes")

time.sleep(2)