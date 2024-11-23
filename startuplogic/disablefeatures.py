import os
import winreg as reg
def disablefeatures():
 try:
  reg_key = reg.CreateKey(reg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Policies\System")
  reg.SetValueEx(reg_key, "DisableTaskMgr", 0, reg.REG_DWORD, 0)
  reg.SetValueEx(reg_key, "DisableRegistryTools", 0, reg.REG_DWORD, 0)
  reg.CloseKey(reg_key)
 except Exception as e:
  print(f"Error: {e}")
disablefeatures()
