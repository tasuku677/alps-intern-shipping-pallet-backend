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
    try:
        photo_name_list = await store_photo(blobArray)
        make_backup(employeeId, palletId, photo_name_list, './info.json')
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


