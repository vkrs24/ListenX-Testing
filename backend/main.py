from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ytmusicapi import YTMusic
import yt_dlp

app = FastAPI()

# Enable CORS for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ytmusic = YTMusic()

@app.get("/search")
async def search_music(q: str):
    """Search YouTube Music and return relevant song results with thumbnails."""
    search_results = ytmusic.search(q, filter="songs", limit=5)

    songs = []
    for result in search_results:
        if "videoId" in result:
            songs.append({
                "title": result["title"],
                "artist": result["artists"][0]["name"] if "artists" in result else "Unknown",
                "videoId": result["videoId"],
                "thumbnail": result["thumbnails"][-1]["url"] if "thumbnails" in result else None  # Highest resolution thumbnail
            })

    return songs

def get_audio_url(video_id):
    """Extracts the audio URL from a YouTube video."""
    url = f"https://www.youtube.com/watch?v={video_id}"
    ydl_opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "extract_flat": False,
        "force_generic_extractor": False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info["url"] if "url" in info else None

@app.get("/get_audio")
async def get_audio(video_id: str):
    """Returns the direct audio URL of a YouTube video."""
    audio_url = get_audio_url(video_id)
    if not audio_url:
        return {"error": "Audio not found"}
    return {"audio_url": audio_url}
