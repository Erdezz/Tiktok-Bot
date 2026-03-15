import requests
import os
import json

# Variables récupérées depuis les Secrets GitHub
WEBHOOK_URL = os.getenv("https://discord.com/api/webhooks/1482699572857016320/Wgm7ufX6cqlxiuXdbbG58yIaSKDB-0BVhnxBS5ZHdSRim0lcd19aSyFzPOATBSwv5l_Y")
RAPID_API_KEY = os.getenv("RAPID_API_KEY")
RAPID_API_HOST = "tik-tok-feed.p.rapidapi.com"

HASHTAGS = ["hacco", "hacoo", "haccolinks"]
DB_FILE = "seen_videos.json"

def main():
    # 1. Charger l'historique pour éviter les doublons
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            seen_ids = json.load(f)
    else:
        seen_ids = []

    new_ids = []

    for tag in HASHTAGS:
        # 2. Appel à l'API
        url = f"https://{RAPID_API_HOST}/"
        headers = {"x-rapidapi-key": RAPID_API_KEY, "x-rapidapi-host": RAPID_API_HOST}
        params = {"search": tag, "type": "challenge-feed"}

        try:
            r = requests.get(url, headers=headers, params=params)
            videos = r.json().get('items', [])
            
            for v in videos[:5]: # On check les 5 dernières
                v_id = str(v.get('id'))
                if v_id and v_id not in seen_ids:
                    # 3. Envoi sur Discord
                    v_url = f"https://www.tiktok.com/video/{v_id}"
                    requests.post(WEBHOOK_URL, json={"content": f"✅ **#{tag}** : {v_url}"})
                    new_ids.append(v_id)
        except:
            print(f"Erreur sur le tag {tag}")

    # 4. Sauvegarder les nouveaux IDs
    if new_ids:
        with open(DB_FILE, "w") as f:
            json.dump((seen_ids + new_ids)[-200:], f)

if __name__ == "__main__":
    main()
