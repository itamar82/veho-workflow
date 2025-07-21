from functools import wraps
from typing import Any, Callable, Dict

from apps.resolvers.dtos import ApiResponse


def convert_kwargs_to_pydantic(func) -> Callable:
    def convert_to_pydantic(d: Dict) -> Dict:
        converted: Dict = {}
        for k, v in d.items():
            if isinstance(v, dict):
                _type = func.__annotations__.get(k)
                converted[k] = _type(**v)
        return converted

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return func(*args, **convert_to_pydantic(kwargs))

    return wrapper


def api_response_handler(func) -> Callable:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            result = func(*args, **kwargs)
            if not result:
                return ApiResponse(success=True)

            return result
        except RuntimeError as e:
            return ApiResponse(success=False, message=str(e))

    return wrapper
