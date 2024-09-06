import os
from fastapi import FastAPI, File, Form, UploadFile, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from utils.store_photo import store_photo
from utils.make_backup import make_backup

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


@app.post("/photos")
async def receive_photo(
    blobArray: list[UploadFile] = File(...),
    employeeId: str = Form(...),
    palletId: str = Form(...),
):
    year_month = blobArray[0].filename.split("_")[-1][:6]
    folder_path_for_image = f"./photos/{year_month}"
    folder_path_for_json = f"./json-backup/{year_month}"
    os.makedirs(folder_path_for_image, exist_ok=True)
    os.makedirs(folder_path_for_json, exist_ok=True)
    try:
        photo_name_list = await store_photo(blobArray, folder_path_for_image)
        make_backup(employeeId, palletId, photo_name_list, folder_path_for_json)
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


