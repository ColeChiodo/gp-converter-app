from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import guitarpro

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/parse-gp/")
async def parse_gp(file: UploadFile = File(...)):
    # Save uploaded file to temp
    tmp = tempfile.NamedTemporaryFile(delete=False)
    tmp.write(await file.read())
    tmp.close()

    # Parse .gp file
    song = guitarpro.parse(tmp.name)

    # Example: convert to minimal JSON
    result = {
        "title": song.title,
        "artist": song.artist,
        "bpm": song.tempo,
        "tracks": [
            {
                "name": track.name,
                "tuning": track.strings,
                "bars": len(track.bars)
            }
            for track in song.tracks
        ]
    }
    return result

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
