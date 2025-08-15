import functools

def exception_handler(default_return=None):
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