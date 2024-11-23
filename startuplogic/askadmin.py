import ctypes, sys, threading, time
from win10toast import ToastNotifier
sys.dont_write_bytecode = True
def is_admin():
    return ctypes.windll.shell32.IsUserAnAdmin() if ctypes.windll.shell32 else False
def send_notification(message):
    toaster = ToastNotifier()
    toaster.show_toast("Admin Permission Required", message, duration=1)
def askadmin():
    if not is_admin():
        notification_thread = threading.Thread(target=send_notification, args=("This script needs administrator privileges. Please run as admin.",))
        notification_thread.start()
        time.sleep(0.3)
        result = ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        if result <= 32:
            askadmin()
        sys.exit()
def setup():
    askadmin()
setup()