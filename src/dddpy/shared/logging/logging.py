import logging
import sys

# Configuración global (va en tu app/core/config.py o main.py)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - [%(method)s] - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)


class Logger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)

    def info(self, message: str, method: str = "N/A"):
        # Usamos 'extra' para pasar datos dinámicos al formato del log
        self.logger.info(message, extra={"method": method})

    def error(self, message: str, method: str = "N/A", exc_info=True):
        # exc_info=True guarda el Traceback completo (vital para errores)
        self.logger.error(message, extra={"method": method}, exc_info=exc_info)

    def warning(self, message: str, method: str = "N/A"):
        self.logger.warning(message, extra={"method": method})
