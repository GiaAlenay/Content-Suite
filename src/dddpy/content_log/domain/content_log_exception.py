class ContentLogNotFound(Exception):
    def __init__(self):
        super().__init__("ContentLog not found")
