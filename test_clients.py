import subprocess
import sys

url = "https://www.youtube.com/watch?v=qSyo5d-dVzA"
clients = [
    "android",
    "ios",
    "mweb",
    "tv_embedded",
    "android_creator"
]

print(f"Testing player clients on: {url}")

for client in clients:
    print(f"\n--- Testing player_client={client} ---")
    cmd = [
        sys.executable, "-m", "yt_dlp",
        "--remote-components", "ejs:github",
        "--extractor-args", f"youtube:player_client={client}",
        "-g",
        "-f", "best[height<=720]/best",
        url
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=30)
    print(f"Return code: {res.returncode}")
    if res.returncode == 0:
        lines = res.stdout.strip().split("\n")
        print(f"SUCCESS! Got {len(lines)} stream URL(s). First URL prefix: {lines[0][:60]}...")
    else:
        print(f"Error (stderr): {res.stderr[:250]}")
