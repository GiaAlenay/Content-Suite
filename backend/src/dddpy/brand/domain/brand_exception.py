class BrandNotFound(Exception):
    def __init__(self):
        super().__init__("Brand no encontrado")


class RepeatedBrandCode(Exception):
    def __init__(self):
        super().__init__("Brand code already exists")
