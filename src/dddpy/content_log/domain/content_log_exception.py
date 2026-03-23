class ContentLogNotFound(Exception):
    def __init__(self):
        super().__init__("Content Log no encontrado")


class ContentLogNotAllowedToChangeStatus(Exception):
    def __init__(self):
        super().__init__("El estatus del log es distinto a 'PENDIENTE' no encontrado")
