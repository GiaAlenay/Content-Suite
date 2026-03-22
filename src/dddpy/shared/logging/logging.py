import logging
import sys


class Logger:
    def __init__(self, logger_name):
        self.logger_name = logger_name
        self.inside_method = "startup"
        self.logger = logging.getLogger(self.logger_name)
        self.logger.setLevel(logging.INFO)

        # CRÍTICO: Si el logger no tiene salida (handlers), se la añadimos
        if not self.logger.handlers:
            # Usamos StreamHandler para que salga por la consola (sys.stdout)
            channel = logging.StreamHandler(sys.stdout)
            # Un formato simple para no pelear con Uvicorn
            formatter = logging.Formatter("%(levelname)s:     %(message)s")
            channel.setFormatter(formatter)
            self.logger.addHandler(channel)

        # Evitamos que el mensaje se duplique si Uvicorn también lo captura
        self.logger.propagate = False

    def add_inside_method(self, method_name):
        self.inside_method = method_name

    def log(self, level, data, method=None, **kwargs):
        current_method = method if method else self.inside_method
        log_function = getattr(self.logger, level)
        message = f"[{self.logger_name}] - [{current_method}] - {data}"
        return log_function(message)

    # Permitimos que acepte cualquier argumento extra para que no explote
    def info(self, data, method=None, **kwargs):
        return self.log("info", data, method, **kwargs)

    def debug(self, data):
        return self.log("debug", data)

    def warning(self, data):
        return self.log("warning", data)

    def error(self, data):
        return self.log("error", data)

    def critical(self, data):
        return self.log("critical", data)
