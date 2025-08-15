import functools

def exception_handler(default_return=None):
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
    def exception_handler_decorator(func):
        @functools.wraps(func)
        def exception_handler_wrapper(*args, **kwargs):

            try:
                return func(*args, **kwargs)
            except Exception as e:
                from utils.utils import save_log_and_send_telegram
                save_log_and_send_telegram(f"Exception in {func.__name__}: {str(e)}")
            return default_return

        return exception_handler_wrapper

    return exception_handler_decorator