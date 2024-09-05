from typing import Union

from fastapi import FastAPI, File, Form, UploadFile, status
from fastapi.responses import JSONResponse

from pydantic import BaseModel


from fastapi.middleware.cors import CORSMiddleware
import os


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

    folder_path = "./temp/{palletId}".format(palletId=palletId)
    os.makedirs(folder_path, exist_ok=True)
    
    try:
        for _, file in enumerate(blobArray):
            file_path = os.path.join(folder_path, f"{file.filename}.jpg")
            # Save the image data to a file
            with open(file_path, "wb") as f:
                f.write(await file.read())
            print('file', file)
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
