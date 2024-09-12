import os
import re
import logging
from fastapi import FastAPI, File, Form, UploadFile, status
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from utils.store_photo import store_photo
from utils.make_backup import make_backup
from config.configurable_value import get_config

from utils.operate_db import get_db_connection, close_db_connection, add_data

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

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
    match = re.match(get_config("FOLDER_SEPARATOR"), isoTimeStampArray[0])
    if match:
        folder_name = match.group(0)
    folder_path = f"./photos/{folder_name}"
    os.makedirs(folder_path, exist_ok=True)
    try:
        photo_name_list = await store_photo(blobArray, folder_path)
        make_backup(employeeId, palletId, photo_name_list, folder_path)

        connection = get_db_connection()
        for _, isoTimeStamp in enumerate(isoTimeStampArray):
            print(isoTimeStamp)
            add_data(connection, palletId, employeeId, isoTimeStamp)
        close_db_connection(connection)
        logger.info(f'Pallet {palletId} has been stored successfully.')
        return JSONResponse(status_code=status.HTTP_200_OK, content={
            "message": "Photos uploaded successfully",
            "employeeId": employeeId,
            "palletId": palletId
        })

    except Exception as e:
        logger.error(e, exc_info=True)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={
            "message": "Failed to upload photos",
            "error": str(e)
        })
    # finally:
    #     connection = get_db_connection()
    #     add_data(connection, palletId, employeeId, timestamp)
    #     close_db_connection(connection)
