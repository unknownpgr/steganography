#! /usr/bin/env python3

import os
import uuid

import uvicorn
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from encoder import decode_image, encode_image, get_available_bytes

app = FastAPI()


@app.get("/")
async def handle_root():
    return RedirectResponse(url="/index.html")

@app.get("/get-available-bytes")
async def handle_get_available_bytes(width: int, height: int):
    return {"available_bytes": get_available_bytes(width, height)}


@app.post("/encode-image")
async def handle_encode_image(
    image: UploadFile = File(...), input_text: str = Form(...)
):
    try:
        extension = image.filename.split(".")[-1]
        filename = str(uuid.uuid4()) + "." + extension
        with open(f"{filename}", "wb") as f:
            f.write(await image.read())
        print(f"Saved image to {filename}")
        new_image_path = encode_image(filename, input_text)
        return {"new_image_path": new_image_path}
    except Exception as e:
        print(e)
        return {"error": "Failed to save image"}
    finally:
        os.remove(f"{filename}")


@app.post("/decode-image")
async def handle_decode_image(
    original_image: UploadFile = File(...), encoded_image: UploadFile = File(...)
):
    try:
        original_image_path = "/tmp/images/" + str(uuid.uuid4()) + ".png"
        with open(original_image_path, "wb") as f:
            f.write(await original_image.read())
        encoded_image_path = "/tmp/images/" + str(uuid.uuid4()) + ".png"
        with open(encoded_image_path, "wb") as f:
            f.write(await encoded_image.read())
        result = decode_image(original_image_path, encoded_image_path)
        return {"result": result}
    except Exception as e:
        print(e)
        return {"error": "Failed to decode image"}
    finally:
        os.remove(original_image_path)
        os.remove(encoded_image_path)


# Mount the static files directory
app.mount("/images/", StaticFiles(directory="/tmp/images"), name="images")
app.mount("/", StaticFiles(directory="./public"), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
