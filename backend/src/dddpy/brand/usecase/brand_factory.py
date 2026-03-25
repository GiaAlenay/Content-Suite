from dddpy.brand.infrastructure.brand_cmd_repository import BrandCmdRepositoryImpl
from dddpy.brand.infrastructure.brand_query_repository import BrandQueryRepositoryImpl
from dddpy.brand.usecase.brand_cmd_usecase import BrandCmdUseCase
from dddpy.brand.usecase.brand_query_usecase import BrandQueryUseCase


def brand_cmd_usecase_factory():
    repository = BrandCmdRepositoryImpl()
    return BrandCmdUseCase(repository)


def brand_query_usecase_factory():
    repository = BrandQueryRepositoryImpl()
    return BrandQueryUseCase(repository)
