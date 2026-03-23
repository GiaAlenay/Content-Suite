class BrandManualVectorNotFound(Exception):
    def __init__(self):
        super().__init__("BrandManualVector no encontrado")


class RepeatedBrandManualVectorName(Exception):
    def __init__(self):
        super().__init__("BrandManualVector brand_id already exists")
