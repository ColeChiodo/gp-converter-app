from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import tempfile
import shutil
import os
from .gp_parser import gp5_to_binary_folder

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # adjust for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/parse-gp/")
async def parse_gp(file: UploadFile = File(...)):
    # Save uploaded file to temp
    with tempfile.NamedTemporaryFile(delete=False, suffix=".gp5") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    # Convert GP5 to binary folder
    out_folder = gp5_to_binary_folder(tmp_path)

    # Create a temporary zip file
    zip_tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".zip")
    zip_path = zip_tmp.name
    zip_tmp.close()
    shutil.make_archive(base_name=zip_path.replace(".zip", ""), format="zip", root_dir=out_folder)

    # Clean up uploaded file and folder
    os.remove(tmp_path)
    shutil.rmtree(out_folder)

    # Return zip file
    return FileResponse(path=zip_path, filename="gp_binary.zip", media_type="application/zip")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

