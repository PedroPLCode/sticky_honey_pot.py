import functools
from logger import save_log
from telegram import send_telegram

def exception_handler(default_return=None):
    def exception_handler_decorator(func):
        @functools.wraps(func)
        def exception_handler_wrapper(*args, **kwargs):

            try:
                return func(*args, **kwargs)
            except Exception as e:
                save_log(f"Exception in {func.__name__}: {str(e)}")
                send_telegram(f"Exception in {func.__name__}: {str(e)}")
            return default_return

        return exception_handler_wrapper

    return exception_handler_decorator