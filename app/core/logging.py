import logging

# Настройка логирования один раз для всего приложения
logging.basicConfig(level=logging.ERROR)

def get_logger(name: str) -> logging.Logger:
    """Получает логгер для модуля"""
    return logging.getLogger(name)
