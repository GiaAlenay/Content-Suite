from dddpy.brand_manual_vector.infrastructure.brand_manual_vector_cmd_repository import (
    BrandManualVectorCmdRepositoryImpl,
)
from dddpy.brand_manual_vector.infrastructure.brand_manual_vector_query_repository import (
    BrandManualVectorQueryRepositoryImpl,
)
from dddpy.brand_manual_vector.usecase.brand_manual_vector_cmd_usecase import (
    BrandManualVectorCmdUseCase,
)
from dddpy.brand_manual_vector.usecase.brand_manual_vector_query_usecase import (
    BrandManualVectorQueryUseCase,
)


def brand_manual_vector_cmd_usecase_factory():
    repository = BrandManualVectorCmdRepositoryImpl()
    return BrandManualVectorCmdUseCase(repository)


def brand_manual_vector_query_usecase_factory():
    repository = BrandManualVectorQueryRepositoryImpl()
    return BrandManualVectorQueryUseCase(repository)
