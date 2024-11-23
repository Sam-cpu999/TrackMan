import subprocess

def get_wifi_info():
    wifi_info = []

    try:
        profiles_output = subprocess.check_output("netsh wlan show profiles", shell=True, text=True)

        ssids = []
        for line in profiles_output.split('\n'):
            if "All User Profile" in line:
                ssid = line.split(":")[1][1:]
                ssid = ssid.strip()
                ssids.append(ssid)

        for ssid in ssids:
            try:
                password_output = subprocess.check_output(f"netsh wlan show profile name=\"{ssid}\" key=clear", shell=True, text=True)
                password_found = False

                for pass_line in password_output.split('\n'):
                    if "Key Content" in pass_line:
                        password = pass_line.split(":")[1][1:].strip()
                        wifi_info.append(f"{ssid}:{password}")
                        password_found = True
                        break

                if not password_found:
                    wifi_info.append(f"{ssid}:NO PWD")

            except subprocess.CalledProcessError as e:
                 wifi_info.append(f"{ssid}:Error retrieving password")

    except subprocess.CalledProcessError:
        return "Could not retrieve Wi-Fi profiles or insufficient permissions."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

    return '\n'.join(wifi_info) if wifi_info else "No Wi-Fi information available."

if __name__ == "__main__":
    wifi_info = get_wifi_info()