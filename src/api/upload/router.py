from fastapi import APIRouter, Depends, File, UploadFile


from dddpy.shared.upload.upload import UploadService


router = APIRouter()

from dddpy.auth.usecase.auth_checker_service import AuthChecker
from dddpy.shared.logging.logging import Logger
from dddpy.auth.usecase.auth_cmd_schema import UserRole


logging = Logger("brand_router")


@router.post(
    "/upload-imagen/{brand_id}",
    dependencies=[Depends(AuthChecker([UserRole.APPROVER_B, UserRole.ADMIN]))],
)
async def upload_imagen(brand_id: str, file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise ValueError("El archivo debe ser una imagen")

    service = UploadService()
    result_url = await service.upload_image_to_supabase(brand_id=brand_id, file=file)

    return {"image_url": result_url}
