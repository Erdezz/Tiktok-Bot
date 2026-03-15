import requests
import os
import json

# Récupération des variables cachées dans GitHub Secrets
WEBHOOK_URL = os.getenv("https://discord.com/api/webhooks/1482699572857016320/Wgm7ufX6cqlxiuXdbbG58yIaSKDB-0BVhnxBS5ZHdSRim0lcd19aSyFzPOATBSwv5l_Y")
HASHTAGS = ["hacco", "hacoo", "haccolinks"]
DB_FILE = "seen_videos.json"

def load_seen_videos():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return []

def save_seen_videos(seen_ids):
    with open(DB_FILE, "w") as f:
        json.dump(seen_ids, f)

def fetch_tiktok_videos(hashtag):
    # Ici, on simule l'appel. En pratique, il faut utiliser une lib 
    # comme 'tiktok-scraper-py' ou une API de scraping.
    print(f"Recherche pour #{hashtag}...")
    return [] # Liste de dictionnaires {'id': '...', 'url': '...'}

def main():
    seen_ids = load_seen_videos()
    new_seen_ids = seen_ids.copy()
    
    for tag in HASHTAGS:
        videos = fetch_tiktok_videos(tag)
        for video in videos:
            if video['id'] not in seen_ids:
                # Envoi au Webhook
                payload = {"content": f"🚀 **Nouveau lien #{tag} !**\n{video['url']}"}
                requests.post(WEBHOOK_URL, json=payload)
                new_seen_ids.append(video['id'])
    
    save_seen_videos(new_seen_ids[:100]) # On garde les 100 derniers pour limiter la taille

if __name__ == "__main__":
    main()
