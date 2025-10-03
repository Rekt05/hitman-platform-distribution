import requests 
import json
from pathlib import Path
from datetime import datetime

#file names
OUT_MAIN = Path("MainBoard.json")
OUT_CE = Path("CategoryExtensions.json")
OUT_ET = Path("ElusiveTargets.json")
OUT_ESC = Path("Escalations.json")
OUT_FL = Path("Freelancer.json")
OUT_ALL = Path("CombinedBoards.json")

BOARDS = {
    "Main Board": "j1ne5891",
    "Category Extensions": "v1ponx76",
    "Elusive Targets": "4d7nxqn6",
    "Escalations": "kdkmjxg1",
    "Freelancer": "76r35zv6"
}

PLATFORM_MAP = {
    "4p9zjrer": "PS5",
    "8gej2n93": "PC",
    "nzelkr6q": "PS4",
    "o7e2mx6w": "Xbox One",
    "nzelyv9q": "Xbox Series X",
    "o7e2xj9w": "Xbox Series S",
    "7m6ylw9p": "Switch"
}

all_combined = []

for board_name, game_id in BOARDS.items():
    all_runs = []
    offset = 0
    BASE_URL = f"https://www.speedrun.com/api/v1/runs?game={game_id}&max=200&status=verified&offset="

    while True:
        url = BASE_URL + str(offset)
        data = requests.get(url).json().get("data", [])

        if not data:
            print(f"All {board_name} runs found")
            break

        for run in data:
            weblink = run.get("weblink")

            videos = (run.get("videos") or {}).get("links")
            video = videos[0]["uri"] if videos else "no video"

            platform_code = (run.get("system") or {}).get("platform", "Unknown")
            platform_name = PLATFORM_MAP.get(platform_code, "Unknown")

            submitted_raw = run.get("submitted")
            if submitted_raw:
                submitted_dt = datetime.fromisoformat(submitted_raw.replace("Z", "+00:00"))
                submitted_date = submitted_dt.strftime("%d/%m/%Y")

            run_entry = {
                "weblink": weblink,
                "video": video,
                "platform": platform_name,
                "submitted": submitted_date
            }

            all_runs.append(run_entry)
            all_combined.append(run_entry)

        print(f"{len(all_runs)} runs so far for {board_name}")
        offset += 200

    #save individually
    if board_name == "Main Board":
        with open(OUT_MAIN, "w", encoding="utf-8") as f:
            json.dump(all_runs, f, indent=2)
    elif board_name == "Category Extensions":
        with open(OUT_CE, "w", encoding="utf-8") as f:
            json.dump(all_runs, f, indent=2)
    elif board_name == "Elusive Targets":
        with open(OUT_ET, "w", encoding="utf-8") as f:
            json.dump(all_runs, f, indent=2)
    elif board_name == "Escalations":
        with open(OUT_ESC, "w", encoding="utf-8") as f:
            json.dump(all_runs, f, indent=2)
    elif board_name == "Freelancer":
        with open(OUT_FL, "w", encoding="utf-8") as f:
            json.dump(all_runs, f, indent=2)

#save combined
with open(OUT_ALL, "w", encoding="utf-8") as f:
    json.dump(all_combined, f, indent=2)

print(f"Total verified runs collected for Main Board: {len([r for r in all_combined if r in all_runs])}")
print(f"Total verified runs collected for Category extensions: {len([r for r in all_combined if r in all_runs])}")
print(f"Total verified runs collected for Elusive Targets: {len([r for r in all_combined if r in all_runs])}")
print(f"Total verified runs collected for Escalations: {len([r for r in all_combined if r in all_runs])}")
print(f"Total verified runs collected for Freelancer: {len([r for r in all_combined if r in all_runs])}")
print(f"Total combined verified runs collected: {len(all_combined)}")
