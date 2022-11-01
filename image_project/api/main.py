from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Union

from PIL import Image
import base64
import io

import cv2
import numpy as np


# mandar para model
class RequestImageModel(BaseModel):
    image_data: str
    x0: Union[int, None] = None
    y0: Union[int, None] = None
    x1: Union[int, None] = None
    y1: Union[int, None] = None


class ResponseImageInformation(BaseModel):
    image_resolution: str
    image_size: int


app = FastAPI()


@app.post("/image/")  # , response_model=ResponseImageInformation)
async def extract_info(image: RequestImageModel):
    # image service:
    try:
        image_pillow, size = base64_to_pillow(image.image_data)

    except Exception:
        raise HTTPException(
            status_code=403, detail='This is not a valid base64 image.')

    width, height = image_pillow.size

    return {"image_resolution": f"{width}x{height}", "image_size": size}


@app.post("/crop/")  # , response_model=ResponseImageInformation)
async def extract_info(image: RequestImageModel):
    # image service:
    if (image.image_data and image.x0 and image.x1 and image.y0 and image.y1):
        pass
    else:
        raise HTTPException(
            status_code=403, detail='Provide valid arguments for cropping the image.')

    return 1


def base64_to_pillow(base64_img):
    if base64_img is None:
        print(1)
        raise HTTPException(
            status_code=403, detail='No Content found. Please send a valid base64 image.')

    image_base64 = base64_img.split(';base64,')

    if (image_base64[0].split('/')[-1].lower().strip() not in ["jpg", "jpeg", "png"]):
        raise HTTPException(
            status_code=403, detail='This is not a valid base64 image encoded from a PNG or JPEG file.')

    image_retrived = base64.b64decode(image_base64[-1])
    image_bytes = io.BytesIO(image_retrived)
    size = image_bytes.getbuffer().nbytes
    image_pillow = Image.open(image_bytes)
    print(3)
    return image_pillow, size
