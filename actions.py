import os
import subprocess
import psutil
from datetime import datetime


def run_cmd(cmd: str, limit: int = 2000) -> str:
    """
    Runs a Windows command and returns output (trimmed).
    """
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    output = (result.stdout or result.stderr).strip()

    if len(output) > limit:
        output = output[:limit] + "\n\n...OUTPUT TRIMMED (too long)..."

    return output


# ------------------- BASIC AUTOMATION -------------------

def list_files() -> str:
    return run_cmd("dir")


def show_ip() -> str:
    return run_cmd("ipconfig", limit=2500)


def system_info() -> str:
    return run_cmd("systeminfo", limit=2500)


def system_summary() -> str:
    """
    Professional short system info (recommended instead of full systeminfo).
    """
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("C:\\")

    summary = (
        "===== SYSTEM SUMMARY =====\n"
        f"CPU Usage       : {cpu}%\n"
        f"Memory Usage    : {mem.percent}%\n"
        f"Total RAM       : {round(mem.total / (1024**3), 2)} GB\n"
        f"Disk C: Used    : {round(disk.used / (1024**3), 2)} GB\n"
        f"Disk C: Free    : {round(disk.free / (1024**3), 2)} GB\n"
        f"Disk C: Usage   : {disk.percent}%\n"
        "=========================="
    )
    return summary


def cpu_usage() -> str:
    return f"CPU Usage: {psutil.cpu_percent(interval=1)}%"


def memory_usage() -> str:
    mem = psutil.virtual_memory()
    return f"Memory Usage: {mem.percent}%"


# ------------------- HIGH-VALUE WINDOWS AUTOMATION -------------------

def open_notepad() -> str:
    subprocess.Popen("notepad")
    return "Opened Notepad."


def open_calculator() -> str:
    subprocess.Popen("calc")
    return "Opened Calculator."


def open_cmd() -> str:
    subprocess.Popen("cmd")
    return "Opened Command Prompt."


def open_chrome() -> str:
    subprocess.Popen("start chrome", shell=True)
    return "Opened Chrome (if installed)."


# ------------------- FOLDER AUTOMATION -------------------

def create_folder(folder_name: str) -> str:
    if not folder_name:
        return "Please provide a folder name. Example: create folder test"

    os.makedirs(folder_name, exist_ok=True)
    return f"Folder created: {folder_name}"


def delete_folder(folder_name: str) -> str:
    if not folder_name:
        return "Please provide a folder name. Example: delete folder test"

    if os.path.exists(folder_name):
        try:
            os.rmdir(folder_name)  # works only if folder is empty
            return f"Folder deleted: {folder_name}"
        except OSError:
            return "Folder is not empty. Delete files inside first."
    else:
        return "Folder not found."


def open_folder(path: str) -> str:
    if not path:
        return "Please provide folder path. Example: open folder C:\\Users"

    if os.path.exists(path):
        os.startfile(path)
        return f"Opened folder: {path}"
    else:
        return "Folder path not found."


# ------------------- UTILITIES -------------------

def show_datetime() -> str:
    now = datetime.now().strftime("%d-%m-%Y %I:%M %p")
    return f"Current Date & Time: {now}"


def battery_status() -> str:
    battery = psutil.sensors_battery()
    if battery is None:
        return "Battery information not available on this system."
    return f"Battery: {battery.percent}% (Plugged in: {battery.power_plugged})"


# ------------------- POWER ACTIONS -------------------

def shutdown_pc() -> str:
    """
    Shutdown PC after 30 seconds.
    """
    subprocess.Popen("shutdown /s /t 30", shell=True)
    return "Shutdown started. PC will shutdown in 30 seconds. Type cancel to stop."


def restart_pc() -> str:
    """
    Restart PC after 30 seconds.
    """
    subprocess.Popen("shutdown /r /t 30", shell=True)
    return "Restart started. PC will restart in 30 seconds. Type cancel to stop."


def cancel_shutdown() -> str:
    """
    Cancel any pending shutdown/restart.
    """
    subprocess.Popen("shutdown /a", shell=True)
    return "Shutdown/Restart cancelled."


def lock_pc() -> str:
    """
    Lock Windows PC immediately.
    """
    subprocess.Popen("rundll32.exe user32.dll,LockWorkStation", shell=True)
    return "PC locked successfully."


# ------------------- ADDITIONAL AUTOMATION -------------------

def enable_night_theme() -> str:
    """
    Enable Windows dark mode / night theme.
    """
    cmd = 'reg add HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize /v AppsUseLightTheme /t REG_DWORD /d 0 /f'
    subprocess.run(cmd, shell=True, capture_output=True)
    return " Dark mode enabled! Your screen is now dark."


def open_whatsapp() -> str:
    """
    Open WhatsApp Desktop application.
    """
    try:
        subprocess.Popen("start whatsapp:", shell=True)
        return " WhatsApp Desktop launched! "
    except Exception as e:
        return " WhatsApp Desktop not found. Please install it from Microsoft Store."


def check_storage() -> str:
    """
    Show disk space for all drives.
    """
    result = [" Disk Space Information:\n"]
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            result.append(
                f"Drive {partition.device}\n"
                f"  Total: {round(usage.total / (1024**3), 2)} GB\n"
                f"  Used: {round(usage.used / (1024**3), 2)} GB\n"
                f"  Free: {round(usage.free / (1024**3), 2)} GB\n"
                f"  Usage: {usage.percent}%\n"
            )
        except:
            pass
    return "\n".join(result)


def open_task_manager() -> str:
    """
    Open Windows Task Manager.
    """
    subprocess.Popen("taskmgr", shell=True)
    return " Task Manager opened! "


def show_running_processes() -> str:
    """
    Show top 15 running processes by CPU usage.
    """
    result = [" Top Running Processes (by CPU usage):\n"]
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            processes.append(proc.info)
        except:
            pass
    
    # Sort by CPU usage
    processes = sorted(processes, key=lambda x: x['cpu_percent'] or 0, reverse=True)[:15]
    
    for i, proc in enumerate(processes, 1):
        result.append(f"{i}. {proc['name']} - PID: {proc['pid']} - CPU: {proc['cpu_percent']}%")
    
    return "\n".join(result)


def mute_volume() -> str:
    """
    Mute system volume.
    """
    subprocess.run("nircmd.exe mutesysvolume 1", shell=True, capture_output=True)
    # Alternative method using PowerShell
    cmd = '(New-Object -ComObject WScript.Shell).SendKeys([char]173)'
    subprocess.run(["powershell", "-Command", cmd], capture_output=True)
    return " Volume muted!"


def increase_volume() -> str:
    """
    Increase system volume.
    """
    # Using PowerShell to increase volume
    cmd = '(New-Object -ComObject WScript.Shell).SendKeys([char]175)'
    subprocess.run(["powershell", "-Command", cmd], capture_output=True)
    return " Volume increased!"


def decrease_volume() -> str:
    """
    Decrease system volume.
    """
    cmd = '(New-Object -ComObject WScript.Shell).SendKeys([char]174)'
    subprocess.run(["powershell", "-Command", cmd], capture_output=True)
    return " Volume decreased!"


def open_settings() -> str:
    """
    Open Windows Settings.
    """
    subprocess.Popen("start ms-settings:", shell=True)
    return " Windows Settings opened!"


def open_network_settings() -> str:
    """
    Open Network Settings.
    """
    subprocess.Popen("start ms-settings:network", shell=True)
    return " Network Settings opened!"


def turn_on_bluetooth() -> str:
    """
    Turn on Bluetooth (opens Bluetooth settings).
    """
    subprocess.Popen("start ms-settings:bluetooth", shell=True)
    return " Bluetooth settings opened! Please enable Bluetooth from there."


def turn_off_bluetooth() -> str:
    """
    Turn off Bluetooth (opens Bluetooth settings).
    """
    subprocess.Popen("start ms-settings:bluetooth", shell=True)
    return " Bluetooth settings opened! Please disable Bluetooth from there."

