from pathlib import Path
import json
import requests
import platform
import getpass
import subprocess
import sys

class Agentinfo:
    def __init__(self, agent_name):
        self.__agent_name = agent_name
        self.__credential_path = self.save_credential_path()
        self.__access_token = self.save_access_token(self.__credential_path)
        self.__agent_version = self.save_agent_version(self.__agent_name)
        
        print(f"Initialize done.")
        print(f"[SAVED] Credential path: {self.__credential_path}")
        print(f"[SAVED] Access token: {self.__access_token}")
        print(f"[SAVED] {self.__agent_name} agent version: {self.__agent_version}")
    
    def save_credential_path(self):
        user_os = platform.system()
        
        if (user_os == "Windows"):
            username = getpass.getuser()
            
            user_path = f"C:\\Users\\{username}\\.claude\\.credentials.json"
            return Path(user_path)
        
    # 멤버변수 access_token에 저장
    def save_access_token(self, credential_path):
        with open(credential_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data["claudeAiOauth"]["accessToken"]
        
    # 에이전트 버전 구하기
    def save_agent_version(self, agent_name):
        agent_name_split = agent_name.split("-")[0]
        print(agent_name)
        prompt_result = subprocess.run(f"{agent_name_split} --version", shell=True, capture_output=True, text=True)
        version = (prompt_result.stdout).split(maxsplit=1)[0]
        return version
        
    # access_token 가져오기
    def get_access_token(self):
        return self.__access_token
    
    def get_agent_version(self):
        return self.__agent_version

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
    
    def get_usage(self):
        response = requests.get(self.__usage_url, headers=self.__http_headers)
        
        with open("usage.json", "w", encoding="utf-8") as f:
            f.write(response.text)
        
        print(response.text)
        
        return response.json()
    
    

if __name__ == "__main__":
    if (len(sys.argv) < 2):
        print("사용법: python main.py <agent_name>")
        sys.exit(1)
    
    agent = Agentinfo(sys.argv[1])
    client = AgentApiClient(
        agent.get_access_token(),
        agent.get_agent_name(),
        agent.get_agent_version()
    )
    
    client.get_usage()
    