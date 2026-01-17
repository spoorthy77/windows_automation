import os
import subprocess
import psutil
import shutil
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
    result = run_cmd("dir")
    return f"📁 Files and folders in current directory:\n{result}"


def show_ip() -> str:
    result = run_cmd("ipconfig", limit=2500)
    return f"🌐 Network Configuration:\n{result}"


def system_info() -> str:
    result = run_cmd("systeminfo", limit=2500)
    return f"💻 System Information:\n{result}"


def cpu_usage() -> str:
    cpu = psutil.cpu_percent(interval=1)
    return f"⚡ CPU Usage: {cpu}%"


def memory_usage() -> str:
    mem = psutil.virtual_memory()
    return f"🧠 Memory Usage: {mem.percent}% ({round(mem.used / (1024**3), 2)} GB / {round(mem.total / (1024**3), 2)} GB)"


def system_summary() -> str:
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("C:\\")

    return (
        "\n" + "=" * 50 + "\n"
        "📊 SYSTEM SUMMARY\n"
        "=" * 50 + "\n"
        f"⚡ CPU Usage       : {cpu}%\n"
        f"🧠 Memory Usage    : {mem.percent}%\n"
        f"💾 Total RAM       : {round(mem.total / (1024**3), 2)} GB\n"
        f"💿 Disk C: Used    : {round(disk.used / (1024**3), 2)} GB\n"
        f"📁 Disk C: Free    : {round(disk.free / (1024**3), 2)} GB\n"
        f"📈 Disk C: Usage   : {disk.percent}%\n"
        + "=" * 50
    )


# ------------------- HIGH-VALUE WINDOWS AUTOMATION -------------------

def open_notepad() -> str:
    subprocess.Popen("notepad")
    return "✅ Notepad opened successfully! 📝"


def open_calculator() -> str:
    # Windows calculator
    subprocess.Popen("calc")
    return "✅ Calculator opened successfully! 🔢"


def open_cmd() -> str:
    subprocess.Popen("cmd")
    return "✅ Command Prompt opened successfully! 💻"


def open_chrome() -> str:
    # If chrome is installed, Windows can open it like this
    subprocess.Popen("start chrome", shell=True)
    return "✅ Chrome browser launched! 🌐 (if installed)"


# ------------------- FOLDER AUTOMATION -------------------

def create_folder(folder_name: str) -> str:
    if not folder_name:
        return "❌ Please provide a folder name. Example: create folder MyData"

    try:
        os.makedirs(folder_name, exist_ok=True)
        return f"✅ Folder created successfully: 📁 {folder_name}"
    except PermissionError:
        return f"❌ Permission denied: Cannot create folder '{folder_name}'"
    except Exception as e:
        return f"❌ Error creating folder: {str(e)}"


def delete_folder(folder_name: str) -> str:
    if not folder_name:
        return "❌ Please provide a folder name. Example: delete folder temp"

    if not os.path.exists(folder_name):
        return "❌ Folder not found. Please check the name and try again."
    
    if not os.path.isdir(folder_name):
        return f"❌ '{folder_name}' is not a folder."
    
    try:
        shutil.rmtree(folder_name)
        return f"✅ Folder deleted successfully: 🗑️  {folder_name}"
    except PermissionError:
        return f"❌ Permission denied: Cannot delete folder '{folder_name}'. Close any open files."
    except Exception as e:
        return f"❌ Error deleting folder: {str(e)}"


def open_folder(path: str) -> str:
    if not path:
        return "❌ Please provide folder path. Example: open folder C:\\Users"

    if os.path.exists(path):
        os.startfile(path)
        return f"✅ Folder opened in Explorer: 📂 {path}"
    else:
        return "❌ Folder path not found. Please check the path and try again."


# ------------------- UTILITIES -------------------

def show_datetime() -> str:
    now = datetime.now().strftime("%d-%m-%Y %I:%M %p")
    return f"🕐 Current Date & Time: {now}"


def battery_status() -> str:
    battery = psutil.sensors_battery()
    if battery is None:
        return "🔌 Battery information not available on this system (likely a desktop PC)."
    
    plugged = "🔌 Yes" if battery.power_plugged else "🔋 No"
    return f"🔋 Battery Level: {battery.percent}% | Plugged in: {plugged}"


# ------------------- POWER ACTIONS -------------------

def shutdown_pc() -> str:
    """
    Shutdown PC after 30 seconds.
    """
    subprocess.Popen("shutdown /s /t 30", shell=True)
    return "⚠️  SHUTDOWN initiated! PC will shutdown in 30 seconds. Type 'cancel shutdown' to stop."


def restart_pc() -> str:
    """
    Restart PC after 30 seconds.
    """
    subprocess.Popen("shutdown /r /t 30", shell=True)
    return "⚠️  RESTART initiated! PC will restart in 30 seconds. Type 'cancel shutdown' to stop."


def cancel_shutdown() -> str:
    """
    Cancel any pending shutdown/restart.
    """
    subprocess.Popen("shutdown /a", shell=True)
    return "✅ Shutdown/Restart cancelled successfully! Your system is safe."


def lock_pc() -> str:
    """
    Lock Windows PC immediately.
    """
    subprocess.Popen("rundll32.exe user32.dll,LockWorkStation", shell=True)
    return "🔒 PC locked successfully! See you soon!"


# ------------------- ADDITIONAL AUTOMATION -------------------

def enable_night_theme() -> str:
    """
    Enable Windows dark mode / night theme.
    """
    cmd = 'reg add HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize /v AppsUseLightTheme /t REG_DWORD /d 0 /f'
    subprocess.run(cmd, shell=True, capture_output=True)
    return "🌙 Dark mode enabled! Your screen is now dark."


def disable_night_theme() -> str:
    """
    Disable Windows dark mode / enable light theme.
    """
    cmd = 'reg add HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize /v AppsUseLightTheme /t REG_DWORD /d 1 /f'
    subprocess.run(cmd, shell=True, capture_output=True)
    return "☀️ Light mode enabled! Your screen is now bright."


def open_whatsapp() -> str:
    """
    Open WhatsApp Desktop application.
    """
    try:
        # Method 1: Try URL protocol (most reliable for Microsoft Store version)
        try:
            subprocess.Popen("start whatsapp:", shell=True)
            return "✅ WhatsApp Desktop launched! 📱"
        except:
            pass
        
        # Method 2: Try direct executable paths
        import os
        whatsapp_paths = [
            r"C:\Users\{}\AppData\Local\WhatsApp\WhatsApp.exe".format(os.environ.get('USERNAME', '')),
            r"C:\Users\{}\AppData\Local\Programs\WhatsApp\WhatsApp.exe".format(os.environ.get('USERNAME', ''))
        ]
        
        for path in whatsapp_paths:
            if os.path.exists(path):
                subprocess.Popen(path)
                return "✅ WhatsApp Desktop launched! 📱"
        
        return "❌ WhatsApp Desktop not found. Please install it from Microsoft Store."
    except Exception as e:
        return f"❌ Error launching WhatsApp: {str(e)}"


def check_storage() -> str:
    """
    Show disk space for all drives.
    """
    result = ["💾 Disk Space Information:\n"]
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
    return "✅ Task Manager opened! 📊"


def show_running_processes() -> str:
    """
    Show top 15 running processes by CPU usage.
    """
    result = ["🔄 Top Running Processes (by CPU usage):\n"]
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
    return "🔇 Volume muted!"


def increase_volume() -> str:
    """
    Increase system volume.
    """
    # Using PowerShell to increase volume
    cmd = '(New-Object -ComObject WScript.Shell).SendKeys([char]175)'
    subprocess.run(["powershell", "-Command", cmd], capture_output=True)
    return "🔊 Volume increased!"


def decrease_volume() -> str:
    """
    Decrease system volume.
    """
    cmd = '(New-Object -ComObject WScript.Shell).SendKeys([char]174)'
    subprocess.run(["powershell", "-Command", cmd], capture_output=True)
    return "🔉 Volume decreased!"


def open_settings() -> str:
    """
    Open Windows Settings.
    """
    subprocess.Popen("start ms-settings:", shell=True)
    return "⚙️ Windows Settings opened!"


def open_network_settings() -> str:
    """
    Open Network Settings.
    """
    subprocess.Popen("start ms-settings:network", shell=True)
    return "🌐 Network Settings opened!"


def turn_on_bluetooth() -> str:
    """
    Turn on Bluetooth (opens Bluetooth settings).
    """
    subprocess.Popen("start ms-settings:bluetooth", shell=True)
    return "📶 Bluetooth settings opened! Please enable Bluetooth from there."


def turn_off_bluetooth() -> str:
    """
    Turn off Bluetooth (opens Bluetooth settings).
    """
    subprocess.Popen("start ms-settings:bluetooth", shell=True)
    return "📵 Bluetooth settings opened! Please disable Bluetooth from there."


# ------------------- PROGRAM GENERATION -------------------

def generate_program(user_request: str, language: str = None, output_dir: str = None) -> str:
    """
    Generate a program using offline LLM with auto-validation and error correction.
    
    Args:
        user_request: Natural language description of program to generate
        language: Programming language (python, java, c, cpp) - auto-detected if None
        output_dir: Custom output directory - defaults to Desktop/GeneratedPrograms
        
    Returns:
        Result message with program details
    """
    try:
        from program_generator import program_generator
        
        result = program_generator.generate_program(user_request, language, output_dir)
        return result['message']
        
    except ImportError as e:
        return f"❌ Program generator not available: {str(e)}\n\nPlease ensure Ollama is installed and running."
    except Exception as e:
        return f"❌ Program generation error: {str(e)}"

