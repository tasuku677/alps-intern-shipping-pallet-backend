import os
from fastapi import FastAPI, File, Form, UploadFile, status
from fastapi.responses import JSONResponse

from fastapi.middleware.cors import CORSMiddleware

import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/photos", )
async def photo_store(
    blobArray: list[UploadFile] = File(...),
    employeeId: str = Form(...),
    palletId: str = Form(...),
):

    year_month = blobArray[0].filename.split("_")[-1][:6]
    folder_path = "./temp/{year_month}".format(year_month=year_month)
    os.makedirs(folder_path, exist_ok=True)
    photo_name_list = []

    try:
        for _, file in enumerate(blobArray):
            file_path = os.path.join(folder_path, f"{file.filename}.jpg")
            with open(file_path, "wb") as f:
                f.write(await file.read())
            photo_name_list.append(file.filename)
       
        if(os.path.exists('./info.json')):
            with open('./info.json', 'r') as json_file:
                try:
                    data = json.load(json_file)
                except json.JSONDecodeError:
                    data = []   
        else:
            data = []
        json_data = {
            "palletId": palletId,
            "employeeId": employeeId,
            "photos": photo_name_list
        }                
        data.append(json_data)   
        with open('./info.json', "w") as json_file:
            json.dump(data, json_file, indent=4)

        return JSONResponse(status_code=status.HTTP_200_OK, content={
                "message": "Photos uploaded successfully",
                "employeeId": employeeId,
                "palletId": palletId
            })
            
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={
            "message": "Failed to upload photos",
            "error": str(e)
        })

# def 