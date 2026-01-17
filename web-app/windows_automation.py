"""
Complete Windows Automation Module
100% Offline - No Internet Required
Handles all Windows automation tasks locally
"""

import os
import subprocess
import psutil
from datetime import datetime
from typing import Optional, Dict

try:
    from offline_program_generator import generate_program
except Exception:
    generate_program = None  # will handle gracefully


class WindowsAutomation:
    """Complete Windows automation handler"""
    
    def __init__(self):
        self.last_command = None
    
    # ==================== UTILITY FUNCTIONS ====================
    
    def run_cmd(self, cmd: str, limit: int = 2000) -> str:
        """Run a Windows command and return output"""
        try:
            result = subprocess.run(
                cmd, 
                shell=True, 
                capture_output=True, 
                text=True,
                timeout=10
            )
            output = (result.stdout or result.stderr).strip()
            
            if len(output) > limit:
                output = output[:limit] + "\n\n...OUTPUT TRIMMED..."
            
            return output
        except subprocess.TimeoutExpired:
            return "⏱️ Command timed out"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    # ==================== APP LAUNCHERS ====================
    
    def open_notepad(self) -> str:
        """Open Notepad"""
        try:
            subprocess.Popen("notepad")
            return "✅ Notepad opened successfully! 📝"
        except Exception as e:
            return f"❌ Failed to open Notepad: {str(e)}"
    
    def open_calculator(self) -> str:
        """Open Calculator"""
        try:
            subprocess.Popen("calc")
            return "✅ Calculator opened successfully! 🔢"
        except Exception as e:
            return f"❌ Failed to open Calculator: {str(e)}"
    
    def open_cmd(self) -> str:
        """Open Command Prompt"""
        try:
            subprocess.Popen("cmd")
            return "✅ Command Prompt opened successfully! 💻"
        except Exception as e:
            return f"❌ Failed to open CMD: {str(e)}"
    
    def open_chrome(self) -> str:
        """Open Chrome browser"""
        try:
            subprocess.Popen("start chrome", shell=True)
            return "✅ Chrome browser launched! 🌐"
        except Exception as e:
            return f"❌ Failed to open Chrome: {str(e)}"
    
    def open_whatsapp(self) -> str:
        """Open WhatsApp Desktop"""
        try:
            # Method 1: Try URL protocol (most reliable for Microsoft Store version)
            try:
                subprocess.Popen("start whatsapp:", shell=True)
                return "✅ WhatsApp opened successfully! 💬"
            except:
                pass
            
            # Method 2: Try direct executable paths
            whatsapp_paths = [
                r"C:\Program Files\WindowsApps\WhatsApp\WhatsApp.exe",
                r"C:\Users\{}\AppData\Local\WhatsApp\WhatsApp.exe".format(os.environ.get('USERNAME', '')),
                r"C:\Users\{}\AppData\Local\Programs\WhatsApp\WhatsApp.exe".format(os.environ.get('USERNAME', ''))
            ]
            
            for path in whatsapp_paths:
                if os.path.exists(path):
                    subprocess.Popen(path)
                    return "✅ WhatsApp opened successfully! 💬"
            
            # Method 3: Try using explorer to search
            subprocess.Popen("explorer.exe shell:AppsFolder\\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App", shell=True)
            return "✅ WhatsApp launch command sent! 💬"
        except Exception as e:
            return f"❌ WhatsApp not found. Please install WhatsApp Desktop from Microsoft Store."
    
    def open_task_manager(self) -> str:
        """Open Task Manager"""
        try:
            subprocess.Popen("taskmgr")
            return "✅ Task Manager opened successfully! 📊"
        except Exception as e:
            return f"❌ Failed to open Task Manager: {str(e)}"
    
    # ==================== SETTINGS ====================
    
    def open_settings(self) -> str:
        """Open Windows Settings"""
        try:
            subprocess.Popen("start ms-settings:", shell=True)
            return "✅ Windows Settings opened! ⚙️"
        except Exception as e:
            return f"❌ Failed to open Settings: {str(e)}"
    
    def open_network_settings(self) -> str:
        """Open Network Settings"""
        try:
            subprocess.Popen("start ms-settings:network", shell=True)
            return "✅ Network Settings opened! 🌐"
        except Exception as e:
            return f"❌ Failed to open Network Settings: {str(e)}"
    
    # ==================== SYSTEM INFO ====================
    
    def cpu_usage(self) -> str:
        """Get CPU usage"""
        try:
            cpu = psutil.cpu_percent(interval=1)
            return f"⚡ CPU Usage: {cpu}%"
        except Exception as e:
            return f"❌ Failed to get CPU usage: {str(e)}"
    
    def memory_usage(self) -> str:
        """Get memory/RAM usage"""
        try:
            mem = psutil.virtual_memory()
            used_gb = round(mem.used / (1024**3), 2)
            total_gb = round(mem.total / (1024**3), 2)
            return f"🧠 Memory Usage: {mem.percent}% ({used_gb} GB / {total_gb} GB)"
        except Exception as e:
            return f"❌ Failed to get memory usage: {str(e)}"
    
    def battery_status(self) -> str:
        """Get battery status"""
        try:
            battery = psutil.sensors_battery()
            if battery is None:
                return "🔌 Battery information not available (Desktop PC)"
            
            plugged = "🔌 Yes" if battery.power_plugged else "🔋 No"
            return f"🔋 Battery: {battery.percent}% | Plugged in: {plugged}"
        except Exception as e:
            return f"❌ Failed to get battery status: {str(e)}"
    
    def check_storage(self) -> str:
        """Check disk storage"""
        try:
            disk = psutil.disk_usage("C:\\")
            used_gb = round(disk.used / (1024**3), 2)
            free_gb = round(disk.free / (1024**3), 2)
            total_gb = round(disk.total / (1024**3), 2)
            
            return (
                f"💾 Disk C: Storage\n"
                f"📊 Used: {used_gb} GB\n"
                f"📁 Free: {free_gb} GB\n"
                f"💿 Total: {total_gb} GB\n"
                f"📈 Usage: {disk.percent}%"
            )
        except Exception as e:
            return f"❌ Failed to check storage: {str(e)}"
    
    def system_info(self) -> str:
        """Get detailed system information"""
        try:
            result = self.run_cmd("systeminfo", limit=2500)
            return f"💻 System Information:\n{result}"
        except Exception as e:
            return f"❌ Failed to get system info: {str(e)}"
    
    def system_summary(self) -> str:
        """Get quick system summary"""
        try:
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
        except Exception as e:
            return f"❌ Failed to get system summary: {str(e)}"
    
    def show_ip(self) -> str:
        """Show IP configuration"""
        try:
            result = self.run_cmd("ipconfig", limit=2500)
            return f"🌐 Network Configuration:\n{result}"
        except Exception as e:
            return f"❌ Failed to get IP info: {str(e)}"
    
    def show_datetime(self) -> str:
        """Show current date and time"""
        try:
            now = datetime.now().strftime("%d-%m-%Y %I:%M %p")
            return f"🕐 Current Date & Time: {now}"
        except Exception as e:
            return f"❌ Failed to get date/time: {str(e)}"
    
    def show_processes(self) -> str:
        """Show running processes"""
        try:
            result = self.run_cmd("tasklist", limit=3000)
            return f"🔄 Running Processes:\n{result}"
        except Exception as e:
            return f"❌ Failed to get processes: {str(e)}"
    
    # ==================== VOLUME CONTROL ====================
    
    def mute_volume(self) -> str:
        """Mute system volume"""
        try:
            # Using nircmd if available, otherwise PowerShell
            self.run_cmd('powershell -c "(New-Object -ComObject WScript.Shell).SendKeys([char]173)"')
            return "🔇 Volume muted!"
        except Exception as e:
            return f"❌ Failed to mute: {str(e)}"
    
    def increase_volume(self) -> str:
        """Increase system volume"""
        try:
            # Increase volume using PowerShell
            for _ in range(2):
                self.run_cmd('powershell -c "(New-Object -ComObject WScript.Shell).SendKeys([char]175)"')
            return "🔊 Volume increased!"
        except Exception as e:
            return f"❌ Failed to increase volume: {str(e)}"
    
    def decrease_volume(self) -> str:
        """Decrease system volume"""
        try:
            # Decrease volume using PowerShell
            for _ in range(2):
                self.run_cmd('powershell -c "(New-Object -ComObject WScript.Shell).SendKeys([char]174)"')
            return "🔉 Volume decreased!"
        except Exception as e:
            return f"❌ Failed to decrease volume: {str(e)}"
    
    # ==================== BLUETOOTH ====================
    
    def turn_on_bluetooth(self) -> str:
        """Turn on Bluetooth"""
        try:
            # Open Bluetooth settings
            subprocess.Popen("start ms-settings:bluetooth", shell=True)
            return "✅ Bluetooth settings opened! Please enable manually. 📡"
        except Exception as e:
            return f"❌ Failed to access Bluetooth: {str(e)}"
    
    def turn_off_bluetooth(self) -> str:
        """Turn off Bluetooth"""
        try:
            # Open Bluetooth settings
            subprocess.Popen("start ms-settings:bluetooth", shell=True)
            return "✅ Bluetooth settings opened! Please disable manually. 📡"
        except Exception as e:
            return f"❌ Failed to access Bluetooth: {str(e)}"
    
    # ==================== THEME ====================
    
    def enable_night_theme(self) -> str:
        """Enable night/dark theme"""
        try:
            # Open personalization settings
            subprocess.Popen("start ms-settings:personalization-colors", shell=True)
            return "✅ Theme settings opened! Select Dark mode. 🌙"
        except Exception as e:
            return f"❌ Failed to open theme settings: {str(e)}"
    
    # ==================== POWER COMMANDS ====================
    
    def lock_pc(self) -> str:
        """Lock the PC"""
        try:
            subprocess.Popen("rundll32.exe user32.dll,LockWorkStation", shell=True)
            return "🔒 PC locked successfully!"
        except Exception as e:
            return f"❌ Failed to lock PC: {str(e)}"
    
    def shutdown(self) -> str:
        """Shutdown PC (30 second delay)"""
        try:
            subprocess.Popen("shutdown /s /t 30", shell=True)
            return "⚠️ SHUTDOWN initiated! PC will shut down in 30 seconds.\nType 'cancel shutdown' to abort."
        except Exception as e:
            return f"❌ Failed to initiate shutdown: {str(e)}"
    
    def restart(self) -> str:
        """Restart PC (30 second delay)"""
        try:
            subprocess.Popen("shutdown /r /t 30", shell=True)
            return "⚠️ RESTART initiated! PC will restart in 30 seconds.\nType 'cancel shutdown' to abort."
        except Exception as e:
            return f"❌ Failed to initiate restart: {str(e)}"
    
    def cancel_shutdown(self) -> str:
        """Cancel shutdown/restart"""
        try:
            subprocess.Popen("shutdown /a", shell=True)
            return "✅ Shutdown/Restart cancelled!"
        except Exception as e:
            return f"❌ Failed to cancel: {str(e)}"
    
    # ==================== FILE OPERATIONS ====================
    
    def get_location_path(self, location: Optional[str] = None) -> str:
        """
        Get full path for a location
        Default is Desktop if location is None
        
        Args:
            location: 'desktop', 'downloads', 'documents', or None
            
        Returns:
            Full path to the location
        """
        username = os.environ.get('USERNAME', '')
        base_path = f"C:\\Users\\{username}"
        
        location_map = {
            'desktop': f"{base_path}\\Desktop",
            'downloads': f"{base_path}\\Downloads",
            'documents': f"{base_path}\\Documents"
        }
        
        # Default to Desktop if location not specified
        if location is None or location not in location_map:
            return location_map['desktop']
        
        return location_map[location]
    
    def create_folder(self, folder_name: str, location: Optional[str] = None) -> str:
        """
        Create a folder at the specified location (default: Desktop)
        
        Args:
            folder_name: Name of the folder to create
            location: 'desktop', 'downloads', 'documents', or None (defaults to Desktop)
            
        Returns:
            Success or error message
        """
        try:
            if not folder_name:
                return "❌ Please provide a folder name!"
            
            # Get full path
            base_path = self.get_location_path(location)
            full_path = os.path.join(base_path, folder_name)
            
            # Check if folder already exists
            if os.path.exists(full_path):
                return f"⚠️ Folder '{folder_name}' already exists at {self._get_location_display(location)}!"
            
            # Create folder
            os.makedirs(full_path, exist_ok=True)
            
            location_display = self._get_location_display(location)
            return f"✅ Folder '{folder_name}' created successfully at {location_display}! 📁\n📍 Path: {full_path}"
            
        except PermissionError:
            return f"❌ Permission denied! Cannot create folder at this location."
        except Exception as e:
            return f"❌ Failed to create folder: {str(e)}"
    
    def delete_folder(self, folder_name: str, location: Optional[str] = None) -> str:
        """
        Delete a folder from the specified location (default: Desktop)
        
        Args:
            folder_name: Name of the folder to delete
            location: 'desktop', 'downloads', 'documents', or None (defaults to Desktop)
            
        Returns:
            Success or error message
        """
        try:
            if not folder_name:
                return "❌ Please provide a folder name!"
            
            # Get full path
            base_path = self.get_location_path(location)
            full_path = os.path.join(base_path, folder_name)
            
            # Check if folder exists
            if not os.path.exists(full_path):
                return f"❌ Folder '{folder_name}' not found at {self._get_location_display(location)}!"
            
            # Check if it's a directory
            if not os.path.isdir(full_path):
                return f"❌ '{folder_name}' is not a folder!"
            
            # Delete folder and all its contents
            import shutil
            shutil.rmtree(full_path)
            
            location_display = self._get_location_display(location)
            return f"✅ Folder '{folder_name}' deleted successfully from {location_display}! 🗑️"
            
        except PermissionError:
            return f"❌ Permission denied! Cannot delete this folder."
        except Exception as e:
            return f"❌ Failed to delete folder: {str(e)}"
    
    def create_file(self, file_name: str, location: Optional[str] = None) -> str:
        """
        Create an empty file at the specified location (default: Desktop)
        
        Args:
            file_name: Name of the file to create
            location: 'desktop', 'downloads', 'documents', or None (defaults to Desktop)
            
        Returns:
            Success or error message
        """
        try:
            if not file_name:
                return "❌ Please provide a file name!"
            
            # Get full path
            base_path = self.get_location_path(location)
            full_path = os.path.join(base_path, file_name)
            
            # Check if file already exists
            if os.path.exists(full_path):
                return f"⚠️ File '{file_name}' already exists at {self._get_location_display(location)}!"
            
            # Create empty file
            with open(full_path, 'w') as f:
                pass  # Create empty file
            
            location_display = self._get_location_display(location)
            return f"✅ File '{file_name}' created successfully at {location_display}! 📄\n📍 Path: {full_path}"
            
        except PermissionError:
            return f"❌ Permission denied! Cannot create file at this location."
        except Exception as e:
            return f"❌ Failed to create file: {str(e)}"
    
    def delete_file(self, file_name: str, location: Optional[str] = None) -> str:
        """
        Delete a file from the specified location (default: Desktop)
        
        Args:
            file_name: Name of the file to delete
            location: 'desktop', 'downloads', 'documents', or None (defaults to Desktop)
            
        Returns:
            Success or error message
        """
        try:
            if not file_name:
                return "❌ Please provide a file name!"
            
            # Get full path
            base_path = self.get_location_path(location)
            full_path = os.path.join(base_path, file_name)
            
            # Check if file exists
            if not os.path.exists(full_path):
                return f"❌ File '{file_name}' not found at {self._get_location_display(location)}!"
            
            # Check if it's a file
            if not os.path.isfile(full_path):
                return f"❌ '{file_name}' is not a file!"
            
            # Delete file
            os.remove(full_path)
            
            location_display = self._get_location_display(location)
            return f"✅ File '{file_name}' deleted successfully from {location_display}! 🗑️"
            
        except PermissionError:
            return f"❌ Permission denied! Cannot delete this file."
        except Exception as e:
            return f"❌ Failed to delete file: {str(e)}"
    
    def _get_location_display(self, location: Optional[str]) -> str:
        """Helper to get display name for location"""
        if location == 'downloads':
            return "Downloads"
        elif location == 'documents':
            return "Documents"
        else:
            return "Desktop"
    
    def list_files(self) -> str:
        """List files in current directory"""
        try:
            result = self.run_cmd("dir")
            return f"📁 Files and folders:\n{result}"
        except Exception as e:
            return f"❌ Failed to list files: {str(e)}"
    
    # ==================== HELP ====================
    
    def help(self) -> str:
        """Show help message"""
        return """
🤖 Windows Automation Chatbot - Available Commands

📱 Open Apps:
  • Open notepad, calculator, Chrome, WhatsApp
  • Open command prompt, task manager
  
⚙️ Settings:
  • Open settings, network settings
  • Enable night theme/dark mode
  • Turn on/off Bluetooth
  
📊 System Info:
  • CPU usage, memory usage, battery status
  • Check storage, system info, system summary
  • Show IP address, date and time
  • Show running processes
  
🔊 Volume Control:
  • Mute, increase volume, decrease volume
  
⚡ Power Commands:
  • Lock PC, shutdown, restart
  • Cancel shutdown
  
📁 Folder Management:
  • Create folder [name] - Creates folder on Desktop
  • Create folder [name] in downloads/documents/desktop
  • Delete folder [name] - Deletes from Desktop
  • Delete folder [name] in downloads/documents/desktop
  
📄 File Management:
  • Create file [name.ext] - Creates file on Desktop (any extension supported)
  • Create file [name.ext] in downloads/documents/desktop
  • Delete file [name.ext] - Deletes from Desktop
  • Delete file [name.ext] in downloads/documents/desktop
  
Examples: .txt, .docx, .pdf, .jpg, .exe, .zip, .py, .html, etc.
  
📂 Files:
  • List files

💡 Just type naturally! Typos are okay!
Examples: "opn calc", "chk stroage", "show baterry"
Examples: "create folder test", "create file notes.docx in downloads", "delete file image.jpg"
"""


# Global automation instance
automation = WindowsAutomation()


# Convenience functions for easier imports
def execute_automation(intent: str, params: Optional[Dict] = None) -> str:
    """
    Execute automation based on detected intent
    
    Args:
        intent: The detected intent from NLP
        params: Optional parameters (for folder/file operations)
        
    Returns:
        Result message
    """
    # Handle folder/file operations with parameters
    if intent == 'create_folder' and params:
        return automation.create_folder(params.get('name'), params.get('location'))
    elif intent == 'delete_folder' and params:
        return automation.delete_folder(params.get('name'), params.get('location'))
    elif intent == 'create_file' and params:
        return automation.create_file(params.get('name'), params.get('location'))
    elif intent == 'delete_file' and params:
        return automation.delete_file(params.get('name'), params.get('location'))
    
    # Handle offline program generation
    if intent == 'write_program':
        if generate_program is None:
            return "❌ Program generator module not available."
        # Determine base path (Desktop default, or specified)
        location = None
        language = None
        topic = None
        user_text = params.get('original_input') if params and 'original_input' in params else ''
        if params:
            location = params.get('location')
            language = params.get('language')
            topic = params.get('topic')
        base_path = automation.get_location_path(location)
        result = generate_program(user_text=user_text, language=language, topic=topic, base_dir=base_path)
        return result['message'] if result.get('ok') else result.get('message', '❌ Failed to generate program')

    # Map intents to methods (for non-parameterized commands)
    intent_map = {
        'open_notepad': automation.open_notepad,
        'open_calculator': automation.open_calculator,
        'open_chrome': automation.open_chrome,
        'open_cmd': automation.open_cmd,
        'open_whatsapp': automation.open_whatsapp,
        'open_task_manager': automation.open_task_manager,
        'open_settings': automation.open_settings,
        'open_network_settings': automation.open_network_settings,
        'cpu_usage': automation.cpu_usage,
        'memory_usage': automation.memory_usage,
        'battery_status': automation.battery_status,
        'check_storage': automation.check_storage,
        'system_info': automation.system_info,
        'system_summary': automation.system_summary,
        'show_ip': automation.show_ip,
        'show_datetime': automation.show_datetime,
        'show_processes': automation.show_processes,
        'mute_volume': automation.mute_volume,
        'increase_volume': automation.increase_volume,
        'decrease_volume': automation.decrease_volume,
        'bluetooth_on': automation.turn_on_bluetooth,
        'bluetooth_off': automation.turn_off_bluetooth,
        'night_theme': automation.enable_night_theme,
        'lock_pc': automation.lock_pc,
        'shutdown': automation.shutdown,
        'restart': automation.restart,
        'cancel_shutdown': automation.cancel_shutdown,
        'list_files': automation.list_files,
        'help': automation.help
    }
    
    # Execute the mapped function
    if intent in intent_map:
        return intent_map[intent]()
    else:
        return f"❓ Unknown intent: {intent}"


if __name__ == "__main__":
    # Test automation
    print("🧪 Testing Windows Automation")
    print("=" * 50)
    print(automation.system_summary())
    print("=" * 50)
