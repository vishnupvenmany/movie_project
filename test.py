import httpx
import srt
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from textblob import TextBlob  # ✅ Lightweight sentiment analysis

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For local testing, change in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenSubtitles API info
OPEN_SUBTITLES_API_KEY = "uVC7NFtKCyy01OM7WMZpBojwLg0gguFO"
HEADERS = {
    "Api-Key": OPEN_SUBTITLES_API_KEY,
    "User-Agent": "PlotHolePlotter/1.0"
}

# Request body structure
class SearchRequest(BaseModel):
    title: str

# Search subtitles
async def search_subtitle_id(title: str):
    url = "https://api.opensubtitles.com/api/v1/subtitles/"
    params = {"query": title, "languages": "en"}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=HEADERS, params=params)
            response.raise_for_status()
            results = response.json()
            if results.get("data"):
                return results["data"][0]["attributes"]["files"][0]["file_id"]
        except Exception as e:
            print(f"Subtitle search error: {e}")
    return None

# Download .srt
async def download_subtitle_file(file_id: int):
    url = "https://api.opensubtitles.com/api/v1/download"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=HEADERS, json={"file_id": file_id})
            response.raise_for_status()
            link = response.json().get("link")
            if link:
                subtitle_response = await client.get(link)
                subtitle_response.raise_for_status()
                return subtitle_response.text
        except Exception as e:
            print(f"Download error: {e}")
    return None

@app.post("/fetch_subtitles")
async def fetch_subtitles(req: SearchRequest):
    try:
        file_id = await search_subtitle_id(req.title)
        if not file_id:
            return {"data": [], "error": "No subtitles found for this title."}

        srt_text = await download_subtitle_file(file_id)
        if not srt_text:
            return {"data": [], "error": "Failed to download subtitle file."}

        subs = list(srt.parse(srt_text))
        if not subs:
            return {"data": [], "error": "No subtitle content found."}

        keywords = ["secret", "reveal", "love", "urgent", "danger"]
        data = []

        for sub in subs:
            blob = TextBlob(sub.content)
            polarity = blob.sentiment.polarity  # [-1.0, 1.0]
            importance = sum(1 for kw in keywords if kw in sub.content.lower())
            if polarity < -0.2:
                importance += 1
            data.append({
                "time": sub.start.total_seconds(),
                "importance": importance,
                "text": sub.content
            })

        return {"data": data}

    except Exception as e:
        print(f"Fetch subtitles error: {e}")
        return {"data": [], "error": "Internal server error."}
