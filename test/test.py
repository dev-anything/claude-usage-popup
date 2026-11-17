import platform
from pathlib import Path
import json
import requests

http_url = "https://api.anthropic.com/api/oauth/usage"
agent_credentials = Path(r"C:\Users\USER\.claude\.credentials.json")
agent_version = "2.1.325"

print(platform.system())

token_info = {}

with open(agent_credentials, "r", encoding="utf-8") as f:
    data = json.load(f)
    token_info = data["claudeAiOauth"]

access_token = token_info["accessToken"]
refresh_token = token_info["refreshToken"]

print(f"[ACCESS TOKEN]  => {access_token}")
print(f"[REFRESH TOKEN] => {refresh_token}")

http_headers = {
    "Authorization": f"Bearer {access_token}",
    "User-Agent": f"claude-code/{agent_version}",
    "Content-Type": "application/json",
    "anthropic-beta": "oauth-2025-04-20"
}

http_response = requests.get(http_url, headers=http_headers)

print(f"[STATUS]   => {http_response.status_code}")
print(f"[RESPONSE] => {http_response.text}")

with open("res.json", "w", encoding="utf-8") as f:
    f.write(http_response.text)