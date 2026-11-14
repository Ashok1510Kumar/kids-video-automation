#!/usr/bin/env python3
"""
Exchanges a one-time Google OAuth authorization code for a permanent refresh token.
"""
import os
import sys
import requests

CLIENT_ID = os.environ.get("YT_CLIENT_ID", "")
CLIENT_SECRET = os.environ.get("YT_CLIENT_SECRET", "")
REDIRECT_URI = "http://localhost:8080"

def exchange_code(auth_code: str, client_id: str, client_secret: str):
    if "code=" in auth_code:
        auth_code = auth_code.split("code=")[1].split("&")[0]
    auth_code = auth_code.strip()

    token_url = "https://oauth2.googleapis.com/token"
    payload = {
        "code": auth_code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code"
    }

    res = requests.post(token_url, data=payload)
    if res.status_code == 200:
        data = res.json()
        print("\nSUCCESS! Refresh token:", data.get("refresh_token"))
    else:
        print(f"Error ({res.status_code}): {res.text}")

if __name__ == "__main__":
    cid = CLIENT_ID or input("Enter Client ID: ").strip()
    csecret = CLIENT_SECRET or input("Enter Client Secret: ").strip()
    code = sys.argv[1] if len(sys.argv) > 1 else input("Enter Auth Code: ").strip()
    exchange_code(code, cid, csecret)
