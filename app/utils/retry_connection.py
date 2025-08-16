import time
import requests
import smtplib
from typing import Callable, Any, TypeVar
from app.utils.logs_utils import write_log

F = TypeVar("F", bound=Callable[..., Any])


def retry_connection(max_retries: int = 3, delay: int = 1):
    """
    Decorator to retry a function upon connection-related exceptions.

    Retries the decorated function up to `max_retries` times with a delay of `delay` seconds between attempts.
    Handles exceptions including ConnectionError, TimeoutError, requests.exceptions.RequestException,
    smtplib.SMTPException, and OSError. Logs each retry attempt and raises an Exception if all retries fail.

    Args:
        func (callable): The function to decorate.

    Returns:
        callable: The wrapped function with retry logic.

    Raises:
            Exception: If the maximum number of retries is reached and the function still fails.
    """

    def retry_connection_decorator(func: F) -> F:
        def retry_connection_wrapper(*args: Any, **kwargs: dict[str, Any]) -> Any:
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except (
                    ConnectionError,
                    TimeoutError,
                    requests.exceptions.RequestException,
                    smtplib.SMTPException,
                    OSError,
                ) as e:
                    retries += 1
                    retry_msg = f"retry_connection Connection failed (attempt {retries}/{max_retries}). Retrying in {delay} seconds...\n{str(e)}"
                    write_log(retry_msg)
                    time.sleep(delay)
            error_msg = f"retry_connection. Max retries reached. Connection failed. max_retries: {max_retries}, delay: {delay}"
            write_log(error_msg)
            raise Exception(error_msg)

        return retry_connection_wrapper  # type: ignore

    return retry_connection_decorator
