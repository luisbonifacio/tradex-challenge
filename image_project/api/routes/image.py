from fastapi import APIRouter, HTTPException

from api.schemas.image import ImageInformationModel, RequestCropModel, ResponseImageInformationModel

from PIL import Image
import base64
import io

router = APIRouter()


# , response_model=ResponseImageInformation)
@router.post("/", status_code=200, summary="Provide the image size in bytes and the image resolution")
def extract_info(image: ImageInformationModel) -> dict:
    """Given a base64 image, return the image size in Bytes and the image resolution."""
    # move to image service:
    try:
        image_pillow, size, _ = base64_to_pillow(image.image_data)

    except Exception:
        raise HTTPException(
            status_code=403, detail='This is not a valid base64 image.')

    width, height = image_pillow.size

    return {"image_resolution": f"{width}x{height}", "image_size": size}


# , response_model=ResponseImageInformation)
@router.post("/edit/crop/", status_code=200, summary="Insere um novo usuário no banco de dados.")
def crop_image(image: RequestCropModel) -> dict:
    # move to image service:
    try:
        if (image.image_data is None or image.x0 is None or image.x1 is None or image.y0 is None or image.y1 is None):
            print(1)
            raise HTTPException(
                status_code=403, detail='Provide valid arguments for cropping the image.')

        image_pillow, _, img_type = base64_to_pillow(image.image_data)
    except Exception:
        raise HTTPException(
            status_code=403, detail='This is not a valid base64 image.')

    try:
        (left, upper, right, lower) = (20, 20, 100, 100)
        cropped_img = image_pillow.crop(
            (image.x0, image.y0, image.x1, image.y1)
        )
        base64_img = pillow_to_base64(cropped_img, img_type)
    except Exception:
        raise HTTPException(
            status_code=500, detail='Image not cropped.')

    return {"image_data": f"data:image/{img_type};base64,"+base64_img.decode('utf-8')}


def base64_to_pillow(base64_img):
    if base64_img is None:
        raise HTTPException(
            status_code=403, detail='No Content found. Please send a valid base64 image.')

    image_base64 = base64_img.split(';base64,')
    img_type = image_base64[0].split('/')[-1].lower().strip()

    if (img_type not in ["jpg", "jpeg", "png"]):
        raise HTTPException(
            status_code=403, detail='This is not a valid base64 image encoded from a PNG or JPEG file.')

    image_retrived = base64.b64decode(image_base64[-1])
    image_bytes = io.BytesIO(image_retrived)
    size = image_bytes.getbuffer().nbytes
    image_pillow = Image.open(image_bytes)
    return image_pillow, size, img_type


def pillow_to_base64(pillow_img, img_type):
    buffer = io.BytesIO()
    pillow_img.save(buffer, format=img_type)
    image_bytes = buffer.getvalue()
    base64_img = base64.b64encode(image_bytes)
    return base64_img
