from importlib import import_module
from typing import Any


def import_function(method_path: str) -> Any:
    module_name, method = method_path.rsplit('.', 1)
    module = import_module(module_name)
    return getattr(module, method, lambda *args, **kwargs: None)
