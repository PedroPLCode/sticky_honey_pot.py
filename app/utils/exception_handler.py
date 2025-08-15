import functools

from typing import Callable, Any, TypeVar

F = TypeVar("F", bound=Callable[..., Any])

def exception_handler(default_return: object = None) -> Callable[[F], F]:
    """
    Decorator that wraps a function to catch and handle exceptions.

    If an exception occurs during the execution of the decorated function,
    it logs the exception message and sends a notification via Telegram using
    the `save_log_and_send_telegram` utility function. The decorator then returns
    a default value specified by `default_return`.

    Args:
        func (Callable): The function to be decorated.

    Returns:
        Callable: The wrapped function with exception handling.
    """
    def exception_handler_decorator(func: F) -> F:
        @functools.wraps(func)
        def exception_handler_wrapper(*args: Any, **kwargs: dict[str, Any]) -> Any:

            try:
                return func(*args, **kwargs)
            except Exception as e:
                from utils.utils import save_log_and_send_telegram
                save_log_and_send_telegram(f"Exception in {func.__name__}: {str(e)}")
            return default_return

        return exception_handler_wrapper  # type: ignore

    return exception_handler_decorator