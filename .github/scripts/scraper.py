import re
from datetime import datetime

# ✏️ UPDATE THESE MANUALLY whenever you complete new rooms or earn badges
USERNAME = "ayomiolutoye"
POINTS = 34
STREAK = 80
RANK = "Hacker"  # Your TryHackMe rank title e.g. "Hacker", "Pro Hacker" etc.

COMPLETED_ROOMS = [
    {"title": "SQL Fundamentals", "url": "https://tryhackme.com/room/sqlfundamentals"},
    # Add more rooms below as you complete them:
    # {"title": "Room Name", "url": "https://tryhackme.com/room/roomcode"},
]

BADGES = [
    # Add your badges here as you earn them:
    # "7 Day Streak", "Advent of Cyber", etc.
]

SKILLS = [
    "SQL",
    # Add skills as you learn them e.g. "Linux", "Networking", "Web Hacking"
]

def build_readme_section():
    rooms_md = "\n".join(
        [f"- [{r['title']}]({r['url']})" for r in COMPLETED_ROOMS]
    ) or "_No rooms yet._"

    badges_md = "\n".join([f"- {b}" for b in BADGES]) or "_No badges yet._"
    skills_md = ", ".join(SKILLS) or "_No skills listed yet._"
    last_updated = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    section = f"""<!-- THM-STATS:START -->
## 🛡️ TryHackMe Progress

| Stat | Value |
|------|-------|
| 👤 Username | [{USERNAME}](https://tryhackme.com/p/{USERNAME}) |
| 🏆 Rank | {RANK} |
| 💰 Points | {POINTS} |
| 🔥 Current Streak | {STREAK} days |
| ✅ Rooms Completed | {len(COMPLETED_ROOMS)} |

### 🎖️ Badges Earned
{badges_md}

### 🧠 Skills Gained
{skills_md}

### 📚 Completed Rooms
{rooms_md}

> _Last updated: {last_updated}_
<!-- THM-STATS:END -->"""

    return section


def update_readme(section, readme_path="README.md"):
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
    section = build_readme_section()
    update_readme(section)
