from dddpy.shared.supabase.supabase_manager import supabase
from dddpy.shared.logging.logging import Logger
from fastapi import UploadFile
import time

logging = Logger("BrandCmdRepositoryImpl")


class UploadService:
    def __init__(self):
        self.bucket_name = "brand"
        self._supabase = supabase
        logging.info("UploadService initialized with Supabase Client")

    async def upload_image_to_supabase(self, brand_id: str, file: UploadFile):
        try:
            file_bytes = await file.read()

            extension = file.filename.split(".")[-1] if "." in file.filename else "png"
            unique_name = f"audit_{int(time.time())}.{extension}"
            path_on_bucket = f"{brand_id}/{unique_name}"

            self._supabase.storage.from_(self.bucket_name).upload(
                path=path_on_bucket,
                file=file_bytes,
                file_options={"content-type": file.content_type},
            )

            file_url = self._supabase.storage.from_(self.bucket_name).get_public_url(
                path_on_bucket
            )

            return file_url

        except Exception as e:
            logging.error(f"Error en UploadService: {str(e)}")
            raise e
