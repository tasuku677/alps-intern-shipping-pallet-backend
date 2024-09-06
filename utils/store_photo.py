import os
async def store_photo(blobArray, folder_path):
    photo_name_list = []
    try:
        for _, file in enumerate(blobArray):
            file_path = os.path.join(folder_path, f"{file.filename}.jpg")
            with open(file_path, "wb") as f:
                f.write(await file.read())
            photo_name_list.append(file.filename)
        return photo_name_list
    except Exception as e:
        print(e)
        return photo_name_list

