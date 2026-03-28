from fastapi import APIRouter, Depends, File, UploadFile


from dddpy.shared.upload.upload import StorageService


router = APIRouter()

from dddpy.auth.usecase.auth_checker_service import AuthChecker
from dddpy.shared.logging.logging import Logger
from dddpy.auth.usecase.auth_cmd_schema import UserRole


logging = Logger("upload_router")


@router.post(
    "/upload-imagen/{brand_code}",
    dependencies=[Depends(AuthChecker([UserRole.APPROVER_B, UserRole.ADMIN]))],
)
async def upload_imagen(brand_code: str, file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise ValueError("El archivo debe ser una imagen")

    service = StorageService()
    result_url = await service.upload_image_to_supabase(
        brand_code=brand_code, file=file
    )

    return {"image_url": result_url}
