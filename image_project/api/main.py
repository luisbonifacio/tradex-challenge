from fastapi import FastAPI

from api import __version__
from api.routes import image


app = FastAPI(title='Image API',
              description="API to manipulate and gather information about base64 images.",
              version=__version__
              )

v1 = FastAPI()
v1.include_router(image.router, prefix='/image',
                  tags=['image'])

app.mount("/api/v1", v1)
