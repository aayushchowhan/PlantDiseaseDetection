from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from typing import Optional
import os

app = FastAPI()

class PlantInfo(BaseModel):
    name: str
    accuracy: Optional[float] = None
    disease_type: Optional[str] = None

@app.post("/analyze/{plant_name}")
async def analyze_plant(plant_name: str, image: UploadFile):
    # Save the uploaded image to a temporary directory
    os.makedirs("temp", exist_ok=True)
    file_path = os.path.join("temp", image.filename)
    with open(file_path, "wb") as f:
        f.write(image.file.read())
    plant_info=PlantInfo(name=plant_name,accuracy=100.0,disease_type='Leave spots')

    return plant_info