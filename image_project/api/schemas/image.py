from pydantic import BaseModel
from typing import Union


class ImageInformationModel(BaseModel):
    image_data: str


class RequestCropModel(BaseModel):
    image_data: str
    x0: Union[int, None] = None
    y0: Union[int, None] = None
    x1: Union[int, None] = None
    y1: Union[int, None] = None


class ResponseImageInformationModel(BaseModel):
    image_resolution: str
    image_size: int
