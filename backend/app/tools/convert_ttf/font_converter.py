import os
import tempfile
import uuid
from fontTools.ttLib import TTFont

BASE_DIR = "storage/converted"
os.makedirs(BASE_DIR, exist_ok=True)


async def convert_ttf_to_woff2(file):
    file_id = str(uuid.uuid4())

    suffix = os.path.splitext(file.filename)[1]

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_in:
        tmp_in.write(await file.read())
        input_path = tmp_in.name

    output_path = os.path.join(BASE_DIR, f"{file_id}.woff2")

    try:
        font = TTFont(input_path)
        font.flavor = "woff2"
        font.save(output_path)
    except Exception as e:
        raise RuntimeError(f"Font conversion failed: {str(e)}")
    finally:
        if os.path.exists(input_path):
            os.remove(input_path)

    return file_id