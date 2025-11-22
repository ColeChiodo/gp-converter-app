from fastapi import FastAPI, UploadFile, File, Response
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import tempfile
from .gp_parser import parse_gp_file

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

    # Use the external parser
    binary_data = parse_gp_file(tmp.name)

    # Return as binary response
    return Response(content=binary_data, media_type="application/octet-stream")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
