import json
import requests
import platform
import getpass
import subprocess
import sys
import streamlit as st
import plotly.graph_objects as go

class Agentinfo:
    def __init__(self, agent_name):
        self.__agent_name = agent_name
        self.save_credential_path()
        self.save_access_token()
        self.__agent_version = self.save_agent_version(self.__agent_name)
        
        print(f"Initialize done.")
        #print(f"[SAVED] Credential path: {self.__credential_path}")
        #print(f"[SAVED] Access token: {self.__access_token}")
        #print(f"[SAVED] {self.__agent_name} agent version: {self.__agent_version}")
    
    def save_credential_path(self):
        user_os = platform.system()
        
        if (user_os == "Windows"):
            self.__credential_path = f"C:\\Users\\{getpass.getuser()}\\.claude\\.credentials.json"
        
    # 멤버변수 access_token에 저장
    def save_access_token(self):
        with open(self.__credential_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.__access_token = data["claudeAiOauth"]["accessToken"]
        
    # 에이전트 버전 구하기
    def save_agent_version(self, agent_name):
        agent_name_split = agent_name.split("-")[0]
        print(agent_name)
        prompt_result = subprocess.run(f"{agent_name_split} --version", shell=True, capture_output=True, text=True)
        version = (prompt_result.stdout).split(maxsplit=1)[0]
        return version
        
    def get_credential_path(self):
        return self.__credential_path
    # access_token 가져오기
    def get_access_token(self):
        return self.__access_token
    
    def get_agent_version(self):
        return self.__agent_version
        #return "2.1.327"

    def get_agent_name(self):
        return self.__agent_name


class AgentApiClient:
    def __init__(self, access_token, agent_name, agent_version):
        self.__http_headers = {
            "Authorization": f"Bearer {access_token}",
            "User-Agent": f"{agent_name}/{agent_version}",
            "Content-Type": "application/json",
            "anthropic-beta": "oauth-2025-04-20"
        }
        self.__usage_url = "https://api.anthropic.com/api/oauth/usage"
        
        print("[DONE] HTTP Headers set.")
    
    def get_usage(self, agent):
        try:
            #print(f"version: {self.__http_headers["User-Agent"]}")
            response = requests.get(self.__usage_url, headers=self.__http_headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            #print(f"[ERROR] HTTP Error ==> {e.response.status_code}")
            
            # 토큰 갱신하기
            if (e.response.status_code == 401):
                print(f"[CODE] ==> {e.response.status_code}")
                #path = agent.get_credential_path()
                #print(f"[GET] Credential path ==> {path}")
                agent.save_access_token()
                
                #print(agent.get_access_token())
                
                self.__http_headers["Authorization"] = f"Bearer {agent.get_access_token()}"

                #print(f"[HEADER] http header: {self.__http_headers}")

                response = requests.get(self.__usage_url, headers=self.__http_headers)
            
        except requests.exceptions.RequestException as e:
            print(f"[FAILED] Requests Failed ==> {e}")
        
        finally:
            with open("usage.json", "w", encoding="utf-8") as f:
                f.write(response.text)
            
            print(response.text)
            
            return response.json()
        
        
class Screen:
    def __init__(self, screen_name):
        self.__screen_name = screen_name
        self.__count = 0
    @st.fragment(run_every="1m")
    def update_screen(self, client, agent):
        self.__count = self.__count + 1
        st.title(self.__screen_name)
        st.write(self.__count)
        usage = client.get_usage(agent)
        
        
        five_hour = usage["five_hour"]
        seven_day = usage["seven_day"]
        
        # ==== 차트 그리기(5시간 사용량) ====
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
        st.plotly_chart(fig, width="stretch", key="fivehour")
        # ==== 차트 그리기(5시간 사용량) ====
        
        # ==== 차트 그리기(일주일 사용량) ====
        seven_day_usage = seven_day["utilization"]
        
        labels = ["used", "remain"]
        values = [seven_day_usage, 100 - seven_day_usage]
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
        st.plotly_chart(fig, width="stretch", key="sevenday")
        # ==== 차트 그리기(일주일 사용량) ====
        
        
 
if __name__ == "__main__":
    if (len(sys.argv) < 2):
        print("사용법: python main.py <agent_name>")
        sys.exit(1)
    
    agent = Agentinfo(sys.argv[1])
    client = AgentApiClient(
        agent.get_access_token(),
        #"sk-ant",
        agent.get_agent_name(),
        agent.get_agent_version()
        #"2.1.327"
    )
    
    screen = Screen("claude usage")
    
    st.set_page_config(
        page_title="Claude Usage Board"
    )
    
    screen.update_screen(client, agent)

    #usage = client.get_usage(agent)
    