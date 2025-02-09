from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from logic import process_image

app = FastAPI()

# Get the absolute path to the directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")

# Create directories if they don't exist
os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs(OUTPUTS_DIR, exist_ok=True)

# CORS middleware setup remains the same
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static directories with absolute paths
app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")
app.mount("/outputs", StaticFiles(directory=OUTPUTS_DIR), name="outputs")

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOADS_DIR, file.filename)
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        output_path = process_image(file_path)
        if not os.path.exists(output_path):
            raise HTTPException(status_code=500, detail="Processing failed, output image not found.")

        filename = os.path.basename(output_path)
        
        return JSONResponse(content={
            "processed_image_url": f"/outputs/{filename}", # Changed to match frontend
            "full_path": output_path
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/outputs/{filename}")
async def get_image(filename: str):
    file_path = os.path.join(OUTPUTS_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Image not found at {file_path}")
    return FileResponse(file_path, media_type="image/png")
