import platform
from pathlib import Path
import json
import requests

agent_credentials = Path(r"C:\Users\USER\.claude\.credentials.json")

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
    "Authorization": f"Bearer {access_token}"
}