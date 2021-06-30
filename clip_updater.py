import sqlite3
import time

import requests


def save_clips(clips):
    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()

    for clip in clips:
        if node := clip.get("node"):
            title = node["title"]
            clip_id = node["id"]
            url = node["url"]
            embed_url = node["embedURL"]
            slug = node["slug"]
            thumbnail_url = node["thumbnailURL"]
            curator = node["curator"]["displayName"] if node["curator"] else "Frag mich mal was leichteres"
            clip_url = thumbnail_url.split("-preview-")[0] + ".mp4"

            c.execute(
                'INSERT INTO strolchguru_clip (title, clip_id, url, embed_url, slug, thumbnail_url, curator, clip_url, is_published) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT (clip_id) DO NOTHING',
                (title, clip_id, url, embed_url, slug, thumbnail_url, curator, clip_url, True))

    conn.commit()
    conn.close()


def get_clips(cursor=None):
    auth = "kimne78kx3ncx6brgo4mv6wki5h1ko"
    headers = {"client-id": f"{auth}", "Content-Type": "application/json"}
    after = f", after: \"{cursor}\"" if cursor else ""
    response = requests.post("https://gql.twitch.tv/gql",
                             headers=headers,
                             json={
                                 "query": "query {\r\n user(login: \"indiestrolche\") {\r\n clips(first: 100" + after + ", criteria: { sort: VIEWS_DESC, period: ALL_TIME }) {\r\n edges {\r\n node {\r\n title\r\n id\r\n url\r\n embedURL\r\n slug\r\n thumbnailURL\r\n \t\t\t\t\tcurator {\r\n displayName\r\n }\r\n }\r\n cursor\r\n }\r\n }\r\n }\r\n}"})

    if response.status_code == 200:
        json = response.json()
        if json.get("errors"):
            return
        if data := json.get("data"):
            return data["user"]["clips"]["edges"]


def get_all_clips():
    cursor = None
    while True:
        clips = get_clips(cursor)
        if clips:
            cursor = clips[-1]["cursor"]
            save_clips(clips)
            if not cursor:
                return
        time.sleep(10)


while True:
    get_all_clips()
    print("Sooo... alle Clips wurden gegönnt :)")
    time.sleep(1800)
