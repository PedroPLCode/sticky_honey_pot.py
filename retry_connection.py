import time
import requests
import smtplib
from logger import save_log


def retry_connection(max_retries=3, delay=1):

    def retry_connection_decorator(func):
        def retry_connection_wrapper(*args, **kwargs):
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
                    retry_msg = f"retry_connection Connection failed (attempt {retries}/{max_retries}). Retrying in {delay} seconds..."
                    save_log(retry_msg)
                    time.sleep(delay)
            error_msg = f"retry_connection. Max retries reached. Connection failed. max_retries: {max_retries}, delay: {delay}"
            save_log(error_msg)
            raise Exception(error_msg)

        return retry_connection_wrapper

    return retry_connection_decorator