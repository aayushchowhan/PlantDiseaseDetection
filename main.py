from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf
from firebaseconfig.models import FarmerField ,Node , FieldData
from firebaseconfig.firebase import get_ref
app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



def read_file_as_image(data) -> np.ndarray:
    image = np.array(Image.open(BytesIO(data)))
    return image



class PlantInfo(BaseModel):
    name: str
    accuracy: Optional[float] = None
    disease_type: Optional[str] = None
    
MODELS = {'corn':tf.keras.models.load_model("/home/rudish/Documents/aprog/PlantDiseaseDetection/Plant Dis/corn/corn.h5"),
          'potato':tf.keras.models.load_model("/home/rudish/Documents/aprog/PlantDiseaseDetection/Plant Dis/potato/potatos.h5"),
          'tomato':tf.keras.models.load_model("/home/rudish/Documents/aprog/PlantDiseaseDetection/Plant Dis/Tomato/Tomato.h5")

}
CLASS_NAMES = {'corn':['Blight', 'Common_Rust', 'Gray_Leaf_Spot', 'Healthy'],
               'potato':["Early Blight", "Late Blight", "Healthy"],
               'tomato':['Tomato_Bacterial_spot',
 'Tomato_Early_blight',
 'Tomato_Late_blight',
 'Tomato_Leaf_Mold',
 'Tomato_Septoria_leaf_spot',
 'Tomato_Spider_mites_Two_spotted_spider_mite',
 'Tomato__Target_Spot',
 'Tomato__Tomato_YellowLeaf__Curl_Virus',
 'Tomato__Tomato_mosaic_virus',
 'Tomato_healthy']}


@app.post("/analyze/{plant_name}")
async def analyze_plant(plant_name: str, file: UploadFile):

    image = read_file_as_image(await file.read())
    img_batch = np.expand_dims(image, 0)
    
    predictions = MODELS[plant_name].predict(img_batch)

    predicted_class = CLASS_NAMES[plant_name][np.argmax(predictions[0])]
    confidence = np.max(predictions[0])

    plant_info=PlantInfo(name=plant_name,accuracy=float(confidence),disease_type=predicted_class)

    return plant_info

@app.post("/FarmField/add/")
async def FarmFieldAdd(no_of_nodes: int):
    farm=FarmerField(num_of_node=no_of_nodes).create()
    print('created FarmField')
    return {'id':farm.ref.id}

@app.post('/FarmField/{farmid}/Node/add')
async def addNode(farmid:str,no_of_hands:int):
    node=Node(no_of_hands=no_of_hands,farmerfieldRef= get_ref('FarmField',farmid)).create()
    print('added node')
    return {'id':node.ref.id,'farmid':farmid}

@app.post('/FarmField/{farmid}/Node/{nodeid}/Hand/add')
async def addHand(farmid:str,nodeid:str):
    node=Node.get(nodeid)(no_of_hands=4,farmerfieldRef= get_ref('FarmField',farmid))
    hand=node.Hand(node,4).create()
    print('added hand')
    return {'id':hand.ref.id,'nodeid':node.ref.id,'farmid':farmid}

@app.post('/Hand/{handid}/FieldData/add')
async def addFieldData(handid:str,phsensor_value:float,moituresensor_value:float):
    fielddata=FieldData(HandRef= get_ref('FieldData',handid),phsensor_value=phsensor_value,moituresensor_value=moituresensor_value).create()
    print('added data')
    return {'id':fielddata.ref.id,'handid':handid,'phsensor_value':phsensor_value,'moituresensor_value':moituresensor_value}
if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)