class BrandManualVectorNotFound(Exception):
    def __init__(self):
        super().__init__("BrandManualVector not found")


class RepeatedBrandManualVectorName(Exception):
    def __init__(self):
        super().__init__("BrandManualVector brand_id already exists")
