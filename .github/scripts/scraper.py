import requests
import json
import re
import sys
from datetime import datetime

USERNAME = "ayomiolutoye"  # 🔁 Change this to your TryHackMe username

def fetch_thm_profile(username):
    """Fetch public profile data from TryHackMe API endpoints."""
    base = "https://tryhackme.com"
    headers = {"User-Agent": "Mozilla/5.0"}

    data = {
        "username": username,
        "points": "N/A",
        "rank": "N/A",
        "streak": "N/A",
        "completed_rooms": [],
        "badges": [],
        "skills": [],
        "last_updated": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
    }

    # --- User stats ---
    try:
        r = requests.get(f"{base}/api/user/rank/{username}", headers=headers, timeout=10)
        if r.status_code == 200:
            stats = r.json()
            data["points"] = stats.get("points", "N/A")
            data["rank"] = stats.get("userRank", "N/A")
    except Exception as e:
        print(f"[WARN] Could not fetch rank: {e}")

    # --- Streak ---
    try:
        r = requests.get(f"{base}/api/user/streak/{username}", headers=headers, timeout=10)
        if r.status_code == 200:
            streak_data = r.json()
            data["streak"] = streak_data.get("currentStreak", "N/A")
    except Exception as e:
        print(f"[WARN] Could not fetch streak: {e}")

    # --- Completed rooms ---
    try:
        r = requests.get(f"{base}/api/no-auth/get-rooms-completed-public/{username}", headers=headers, timeout=10)
        if r.status_code == 200:
            rooms = r.json()
            data["completed_rooms"] = [
                {"title": room.get("title", "Unknown"), "url": f"https://tryhackme.com/room/{room.get('code', '')}"}
                for room in (rooms if isinstance(rooms, list) else [])
            ]
    except Exception as e:
        print(f"[WARN] Could not fetch completed rooms: {e}")

    # --- Badges ---
    try:
        r = requests.get(f"{base}/api/no-auth/get-badges-public/{username}", headers=headers, timeout=10)
        if r.status_code == 200:
            badges = r.json()
            data["badges"] = [
                badge.get("name", "Unknown")
                for badge in (badges if isinstance(badges, list) else [])
            ]
    except Exception as e:
        print(f"[WARN] Could not fetch badges: {e}")

    return data


def build_readme_section(data):
    """Build the markdown block to inject into README.md."""
    rooms_md = "\n".join(
        [f"- [{r['title']}]({r['url']})" for r in data["completed_rooms"][:20]]  # cap at 20 for readability
    ) or "_No rooms found or profile is private._"

    badges_md = ", ".join(data["badges"]) if data["badges"] else "_No badges yet._"

    section = f"""<!-- THM-STATS:START -->
## 🛡️ TryHackMe Progress

| Stat | Value |
|------|-------|
| 🏆 Rank | {data['rank']} |
| 💰 Points | {data['points']} |
| 🔥 Current Streak | {data['streak']} days |
| ✅ Rooms Completed | {len(data['completed_rooms'])} |

### 🎖️ Badges Earned
{badges_md}

### 📚 Completed Rooms (latest 20)
{rooms_md}

> _Last updated: {data['last_updated']}_
<!-- THM-STATS:END -->"""

    return section


def update_readme(section, readme_path="README.md"):
    """Replace the THM stats block in the README, or append it."""
    try:
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        content = "# My CyberSecurity Journey\n\n"

    pattern = r"<!-- THM-STATS:START -->.*?<!-- THM-STATS:END -->"
    if re.search(pattern, content, re.DOTALL):
        content = re.sub(pattern, section, content, flags=re.DOTALL)
    else:
        content += f"\n\n{section}\n"

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("✅ README.md updated successfully.")


if __name__ == "__main__":
    print(f"🔍 Fetching TryHackMe data for: {USERNAME}")
    profile_data = fetch_thm_profile(USERNAME)
    print(json.dumps(profile_data, indent=2))
    section = build_readme_section(profile_data)
    update_readme(section)
