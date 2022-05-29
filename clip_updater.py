import sqlite3
import time

import youtube_dl
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport

GQL_query_clips = """
query($after: Cursor) {
    user(login: "indiestrolche") {
        clips(first: 100, after: $after, criteria: { 
            sort: VIEWS_DESC, 
            period: ALL_TIME 
        }) {
            edges {
                node {
                    title
                    id
                    url
                    embedURL
                    slug
                    game {
                        displayName
                    }
                    thumbnailURL(width: 480, height: 272)
                    curator {
                        displayName
                    }
                    createdAt
                    durationSeconds
                }
                cursor
            }
        }
    }
}
"""


def get_clip(cursor, clip_id: int):
    cursor.execute('SELECT id, title, clip_id, url, embed_url, slug, thumbnail_url, category, curator, clip_url, '
                   'is_published, created_at, custom_title, duration, is_downloaded, is_in_loop FROM strolchguru_clip '
                   'WHERE clip_id = ?', (clip_id,))
    clip = cursor.fetchone()

    return None if not clip else {
        "id": clip[0],
        "title": clip[1],
        "clip_id": clip[2],
        "url": clip[3],
        "embed_url": clip[4],
        "slug": clip[5],
        "thumbnail_url": clip[6],
        "category": clip[7],
        "curator": clip[8],
        "clip_url": clip[9],
        "is_published": clip[10],
        "created_ad": clip[11],
        "custom_title": clip[12],
        "duration": clip[13],
        "is_downloaded": clip[14],
        "is_in_loop": clip[15],
    }


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
            category = node["game"]["displayName"] if node.get("game") else None
            curator = node["curator"]["displayName"] if node["curator"] else "Frag mich mal was leichteres"
            clip_url = thumbnail_url.split("-preview-")[0] + ".mp4"
            created_at = node["createdAt"]
            duration = node["durationSeconds"]

            if clip := get_clip(c, clip_id):
                c.execute('UPDATE strolchguru_clip SET title = ?, url = ?, embed_url = ?, slug = ?, thumbnail_url = ?, '
                          'category = ?, curator = ?, clip_url = ?, created_at = ?, duration = ? '
                          'WHERE clip_id = ?',
                          (title, url, embed_url, slug, thumbnail_url, category, curator, clip_url, created_at,
                           duration, clip_id))
            else:
                c.execute(
                    'INSERT INTO strolchguru_clip (title, clip_id, url, embed_url, slug, thumbnail_url, category, '
                    'curator, clip_url, created_at, duration, is_downloaded, is_published, is_in_loop) '
                    'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                    (title, clip_id, url, embed_url, slug, thumbnail_url, category, curator, clip_url, created_at,
                     duration, False, True, True))

    conn.commit()
    conn.close()


def get_client() -> Client:
    transport = RequestsHTTPTransport(
        url="https://gql.twitch.tv/gql",
        verify=True,
        retries=3,
        headers={
            'Content-Type': 'text/plain;charset=UTF-8',
            'Client-ID': 'kimne78kx3ncx6brgo4mv6wki5h1ko',
        }
    )

    return Client(
        transport=transport,
        fetch_schema_from_transport=True
    )


def get_clips(cursor: str = "") -> dict:
    query = gql(GQL_query_clips)
    client = get_client()
    try:
        result = client.execute(query, variable_values={"after": cursor})
    except Exception:
        return get_clips(cursor=cursor)

    return result["user"]["clips"]["edges"]


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


def download_clips():
    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()

    c.execute("SELECT clip_id, url FROM strolchguru_clip WHERE is_downloaded IS false")
    clips = c.fetchall()

    with youtube_dl.YoutubeDL({"writethumbnail": True, "outtmpl": "clips/%(id)s.%(ext)s"}) as ytdl:
        for clip in clips:
            try:
                ytdl.download([clip[1]])
                c.execute("UPDATE strolchguru_clip SET is_downloaded = true WHERE clip_id = ? ", (clip[0],))
                conn.commit()
            except:
                pass

    conn.close()


while True:
    get_all_clips()
    print("Sooo... alle Clips wurden gegönnt... starte mit dem Download")
    download_clips()
    print("Auch alle Clips downgeloaded")
    time.sleep(1800)
