import streamlit as st
from datetime import datetime
import requests
import platform
import json

import test.constants as constants

import plotly.graph_objects as go

print(platform.system())


st.subheader("Claude Usage Board")

st.title("Claude Usage")
st.write("Hello, Users!")

@st.fragment(run_every="1m")
def get_usage_and_update_ui():
    token_info = {}
    latest_access_token = None
    try:
        with open(constants.AGENT_CREDENTIALS, "r", encoding="utf-8") as f:
            data = json.load(f)
            token_info = data["claudeAiOauth"]
        
        access_token = token_info["accessToken"]
        
        if latest_access_token != access_token or latest_access_token is None:
            latest_access_token = access_token
        
        print(f"[ACCESS TOKEN] => {latest_access_token}")
        
        http_headers = {
            "Authorization": f"Bearer {latest_access_token}",
            "User-Agent": f"claude-code/{constants.AGENT_VERSION}",
            "Content-Type": "application/json",
            "anthropic-beta": "oauth-2025-04-20"
        }
        
        http_response = requests.get(constants.AGENT_URL, headers=http_headers).json()

        #print(f"[STATUS]   => {http_response.status_code}")
        #print(f"[RESPONSE] => {http_response.text}")

        #with open("res.json", "w", encoding="utf-8") as f:
        #    f.write(http_response.text)
        
        #st.write(http_response.text)
        
        five_hour = http_response["five_hour"]
        
        #st.write(five_hour["utilization"])
        
        # ==== 차트 그리기 ====
        five_hour_usage = five_hour["utilization"]
        
        labels = ["used", "remain"]
        values = [five_hour_usage, 100 - five_hour_usage]
        colors = ["#FF4B4B", "#E6EAF1"]
        
        fig = go.Figure(
            data = [
                go.Pie(
                    labels=labels,
                    values=values,
                    hole=0.7,
                    marker_colors=colors,
                    textinfo="none",
                    #hoverinfo="label+percent",
                    sort=False
                )
            ]
        )
        
        fig.update_layout(
            showlegend=False,
            margin=dict(t=10, b=10, l=10, r=10),
            height=250
        )
        # ==== 차트 그리기 ====
        st.plotly_chart(fig, width="stretch")
        
    except Exception as e:
            st.error(f"Something Wrong... => {e}")
            
get_usage_and_update_ui()