class ManualRecordNotFound(Exception):
    def __init__(self):
        super().__init__("ManualRecord no encontrado")
