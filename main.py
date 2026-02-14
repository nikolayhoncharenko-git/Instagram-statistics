import json
import csv
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent
FOLLOWERS_FILE = BASE_DIR / "followers_1.json"
FOLLOWING_FILE = BASE_DIR / "following.json"
OUTPUT_FILE = BASE_DIR / "instagram_analysis.csv"


with open(FOLLOWERS_FILE, "r", encoding="utf-8") as f:
    followers_data = json.load(f)

with open(FOLLOWING_FILE, "r", encoding="utf-8") as f:
    following_data = json.load(f)

followers_info = {}
for item in followers_data:
    sld = item.get("string_list_data", [])
    if sld:
        username = sld[0]["value"]
        href = sld[0].get("href", "")
        timestamp = sld[0].get("timestamp", "")
        followers_info[username] = {"href": href, "timestamp": timestamp}

following_info = {}
for item in following_data.get("relationships_following", []):
    username = item.get("title", "")
    sld = item.get("string_list_data", [])
    href = sld[0].get("href", "") if sld else ""
    timestamp = sld[0].get("timestamp", "") if sld else ""
    if username:
        following_info[username] = {"href": href, "timestamp": timestamp}

all_users = set(followers_info.keys()) | set(following_info.keys())

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([
        "username",
        "подписан на меня",
        "я подписан",
        "взаимная",
        "Ссылка",
        "Когда подписан на меня",
        "Когда подписался я"
    ])

    for user in sorted(all_users):
        f_info = followers_info.get(user, {})
        fg_info = following_info.get(user, {})

        f_time = datetime.fromtimestamp(f_info.get("timestamp")).strftime("%Y-%m-%d %H:%M:%S") if f_info.get(
            "timestamp") else ""
        fg_time = datetime.fromtimestamp(fg_info.get("timestamp")).strftime("%Y-%m-%d %H:%M:%S") if fg_info.get(
            "timestamp") else ""

        profile_href = f_info.get("href") or fg_info.get("href") or ""

        writer.writerow([
            user,
            "Да" if user in followers_info else "Нет",
            "Да" if user in following_info else "Нет",
            "Да" if user in followers_info and user in following_info else "Нет",
            profile_href,
            f_time,
            fg_time
        ])

print(f"Done: {OUTPUT_FILE}")