class BrandNotFound(Exception):
    def __init__(self):
        super().__init__("Brand not found")


class RepeatedBrandCode(Exception):
    def __init__(self):
        super().__init__("Brand code already exists")
