from dddpy.shared.supabase.supabase_manager import supabase
from dddpy.shared.logging.logging import Logger
from fastapi import UploadFile
import time

logging = Logger("BrandCmdRepositoryImpl")


class StorageService:
    def __init__(self):
        self.bucket_name = "brand"
        self._supabase = supabase
        logging.info("StorageService initialized with Supabase Client")

    async def upload_image_to_supabase(self, brand_code: str, file: UploadFile):
        try:
            file_bytes = await file.read()

            extension = file.filename.split(".")[-1] if "." in file.filename else "png"
            unique_name = f"audit_{int(time.time())}.{extension}"
            path_on_bucket = f"{brand_code}/{unique_name}"

            self._supabase.storage.from_(self.bucket_name).upload(
                path=path_on_bucket,
                file=file_bytes,
                file_options={"content-type": file.content_type},
            )

            file_url = await self._supabase.storage.from_(
                self.bucket_name
            ).get_public_url(path_on_bucket)

            return file_url

        except Exception as e:
            logging.error(f"Error en StorageService: {str(e)}")
            raise e

    async def upload_file(
        self, file_bytes: bytes, destination_path: str, content_type: str
    ) -> str:
        """Sube cualquier stream de bytes a Supabase y retorna la URL pública"""
        try:
            self._supabase.storage.from_(self.bucket_name).upload(
                path=destination_path,
                file=file_bytes,
                file_options={"content-type": content_type},
            )

            return self._supabase.storage.from_(self.bucket_name).get_public_url(
                destination_path
            )
        except Exception as e:
            logging.error(f"Error subiendo archivo a Supabase: {str(e)}")
            raise e
