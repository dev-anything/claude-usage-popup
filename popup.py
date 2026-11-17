import streamlit as st
from datetime import datetime
import requests
import platform
import json

import constants

print(platform.system())



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
        
        http_response = requests.get(constants.AGENT_URL, headers=http_headers)

        #print(f"[STATUS]   => {http_response.status_code}")
        #print(f"[RESPONSE] => {http_response.text}")

        with open("res.json", "w", encoding="utf-8") as f:
            f.write(http_response.text)
        
        st.write(http_response.text)
        
    except Exception as e:
            st.error(f"Something Wrong... => {e}")
            
get_usage_and_update_ui()