import os
import re
from fastapi import FastAPI, File, Form, HTTPException, UploadFile, status
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from utils.store_photo import store_photo
from utils.make_backup import make_backup
from config.configurable_value import get_config

from utils.operate_db import get_db_connection, close_db_connection, add_data

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
    return FileResponse('./static/index.html')


@app.get("/assets/{file_path:path}")
async def get_js_files(file_path: str):
    return FileResponse(f'./static/assets/{file_path}')


@app.post("/api/v1/photos")
async def receive_photo(
    employeeId: str = Form(...),
    palletId: str = Form(...),
    isoTimeStampArray: list[str] = Form(...),
    blobArray: list[UploadFile] = File(...),
):
    # Store photos in the folder
    match = re.match(get_config("FOLDER_SEPARATOR"), isoTimeStampArray[0])
    if match:
        folder_name = match.group(0)
    folder_path = f"./photos/{folder_name}"
    os.makedirs(folder_path, exist_ok=True)
    try:
        photo_name_list = await store_photo(blobArray, folder_path)
        make_backup(employeeId, palletId, photo_name_list, folder_path)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={
            "message": "Failed to upload photos",
            "error": str(e)
        })
    # Operate database
    try:
        connection = get_db_connection()
        try:
            for _, isoTimeStamp in enumerate(isoTimeStampArray):
                print(isoTimeStamp)
                add_data(connection, palletId, employeeId, isoTimeStamp)
        finally:
            close_db_connection(connection)
        return JSONResponse(status_code=status.HTTP_200_OK, content={
            "message": "Photos uploaded successfully",
            "employeeId": employeeId,
            "palletId": palletId
        })
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={
            "message": e.detail
        })
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content={
            "message": "There is network issue",
            "error": str(e)
        })
