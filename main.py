from pathlib import Path
import json
import requests



#class Graph:
class Http:
    usage_url = "https://api.anthropic.com/api/oauth/usage"
    agent_ver = "2.1.326"
    
    def get_agent_usage(access_token):
        http_header = {
            "Authorization": f"Bearer {access_token}",
            "User-Agent": f"claude-code/{Http.agent_ver}",
            "Content-Type": "application/json",
            "anthropic-beta": "oauth-2025-04-20"
        }
        
        http_response = requests.get(Http.usage_url, headers=http_header)
        
        return http_response

class Credential:
    credential_path = Path(r"C:\Users\USER\.claude\.credentials.json")
    latest_access_token = None
    
    
    
    def __init__(self):
        Credential.latest_access_token = self.save_access_token()
    
    def save_access_token():
        with open(Credential.credential_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            token_info = data["claudeAiOauth"]
        
        if (Credential.latest_access_token is None) or (Credential.latest_access_token != token_info):
            Credential.latest_access_token = token_info["accessToken"]
            
    def get_access_token():
        return Credential.latest_access_token
    
    
class App:
    
    

if __name__ == "__main__":
    