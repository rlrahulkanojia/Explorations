
import io
import os
import uuid
from PIL import Image
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi import File, UploadFile
from service.commons.logger import get_logger
from service.commons.environment import CHECKPOINT_PATH, DEVICE, OUTPUT_DIR
from service.inference.process import generate_mask, load_seg_model, get_palette

log = get_logger(__name__)
MODEL = load_seg_model(CHECKPOINT_PATH,device=DEVICE)  
PALETTE = get_palette(4)

class ImageResponse(BaseModel):
    width: int
    height: int
    format: str
    mode: str
    size_bytes: int


async def get_cloth(file: UploadFile = File(...)):
    try:
        # Read the uploaded file
        contents = await file.read()
        
        # Open the image using Pillow
        image = Image.open(io.BytesIO(contents))
        
        # Get image information
        image_metadata = ImageResponse(
            width=image.width,
            height=image.height,
            format=image.format,
            mode=image.mode,
            size_bytes=len(contents)
        )

        outut_image = generate_mask(
            image,
            net=MODEL,
            palette=PALETTE,
            device=DEVICE
        )

       # Convert to RGB mode if it's not already
        if outut_image.mode in ('RGBA', 'P'):
            outut_image = outut_image.convert('RGB')

        filename = f"output_{uuid.uuid4()}.jpg"
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        output_path = os.path.join(OUTPUT_DIR, filename)
        outut_image.save(output_path, format="JPEG")

        return {
            "status": 200,
            "path": "DONE",
            "metadata" : image_metadata,
            "output_path" : output_path
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"message": f"Error processing image: {str(e)}"}
        )