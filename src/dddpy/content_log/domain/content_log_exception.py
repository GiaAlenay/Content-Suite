class ContentLogNotFound(Exception):
    def __init__(self):
        super().__init__("ContentLog not found")


class RepeatedContentLogCode(Exception):
    def __init__(self):
        super().__init__("ContentLog content_data already exists")


class RepeatedContentLogName(Exception):
    def __init__(self):
        super().__init__("ContentLog brand_id already exists")
