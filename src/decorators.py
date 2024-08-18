from functools import wraps
from typing import Any

from config import LOG_DIR_DECORATOR


def log(falename: str = LOG_DIR_DECORATOR) -> Any:
    """Логирует результат выполнения функции и записывает его в файл"""

    def decorator(func: Any) -> Any:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                with open(falename, "a", encoding="utf-8") as f:
                    f.write(f"{func.__name__} - {result} ok\n")
                return result
            except Exception as e:
                with open(falename, "a", encoding="utf-8") as f:
                    f.write(f"{func.__name__} - {e} error\n")
                print(e)

        return wrapper

    return decorator
