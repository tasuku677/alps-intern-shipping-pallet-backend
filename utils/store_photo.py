import os
async def store_photo(blobArray):
    year_month = blobArray[0].filename.split("_")[-1][:6]
    folder_path = "./temp/{year_month}".format(year_month=year_month)
    os.makedirs(folder_path, exist_ok=True)
    try:
        for _, file in enumerate(blobArray):
            file_path = os.path.join(folder_path, f"{file.filename}.jpg")
            with open(file_path, "wb") as f:
                f.write(await file.read())
        return True
    except Exception as e:
        print(e)
        return False

