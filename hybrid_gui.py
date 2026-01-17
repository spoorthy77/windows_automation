"""
Hybrid GUI Chatbot - Windows Automation with Automatic Online/Offline Switching

A beautiful GUI chatbot that automatically detects internet connectivity and switches
between online (Grok AI) and offline (local NLP) modes seamlessly.
"""

import tkinter as tk
from tkinter import scrolledtext, Frame, Label, Entry, Button
import threading
from hybrid_chatbot_core import process_user_input, get_current_mode


class HybridChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 Windows Automation Assistant (Hybrid Mode)")
        self.root.geometry("950x750")
        self.root.configure(bg="#1a1a2e")
        
        # Make window resizable
        self.root.minsize(700, 550)
        
        # Color scheme - Modern dark theme
        self.bg_color = "#1a1a2e"
        self.chat_bg = "#16213e"
        self.user_msg_bg = "#0f3460"
        self.bot_msg_bg = "#1a1a2e"
        self.text_color = "#e0e0e0"
        self.accent_color = "#00adb5"
        self.button_color = "#00adb5"
        self.button_hover = "#00c9d1"
        self.online_color = "#00ff00"
        self.offline_color = "#ff5555"
        
        # Header with mode indicator
        header_frame = Frame(root, bg=self.accent_color, height=80)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header_frame.pack_propagate(False)
        
        title_label = Label(
            header_frame, 
            text="🤖 Windows Automation Assistant",
            font=("Segoe UI", 18, "bold"),
            bg=self.accent_color,
            fg="white"
        )
        title_label.pack(pady=8)
        
        subtitle_label = Label(
            header_frame,
            text="Hybrid Mode: Automatic Online/Offline Switching",
            font=("Segoe UI", 10),
            bg=self.accent_color,
            fg="#e8f4f8"
        )
        subtitle_label.pack()
        
        # Mode indicator
        self.mode_label = Label(
            header_frame,
            text="🔄 Detecting mode...",
            font=("Segoe UI", 9, "bold"),
            bg=self.accent_color,
            fg="white"
        )
        self.mode_label.pack(pady=2)
        
        # Main container
        main_container = Frame(root, bg=self.bg_color)
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Chat display area with scrollbar
        chat_frame = Frame(main_container, bg=self.chat_bg, relief=tk.FLAT)
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg=self.chat_bg,
            fg=self.text_color,
            insertbackground=self.accent_color,
            relief=tk.FLAT,
            padx=15,
            pady=15,
            spacing1=5,
            spacing2=2,
            spacing3=5,
            state=tk.DISABLED
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        
        # Configure tags for different message types
        self.chat_display.tag_config("user", foreground="#4fc3f7", font=("Segoe UI", 10, "bold"))
        self.chat_display.tag_config("bot", foreground="#66ff99", font=("Segoe UI", 10, "bold"))
        self.chat_display.tag_config("system", foreground="#ffaa33", font=("Segoe UI", 9, "italic"))
        self.chat_display.tag_config("mode_online", foreground=self.online_color, font=("Segoe UI", 9))
        self.chat_display.tag_config("mode_offline", foreground=self.offline_color, font=("Segoe UI", 9))
        
        # Input area
        input_container = Frame(main_container, bg=self.bg_color)
        input_container.pack(fill=tk.X, pady=(10, 0))
        
        # Input field
        self.user_input = Entry(
            input_container,
            font=("Segoe UI", 11),
            bg="#2c3e50",
            fg=self.text_color,
            insertbackground=self.accent_color,
            relief=tk.FLAT,
            borderwidth=2
        )
        self.user_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10), ipady=8)
        self.user_input.bind("<Return>", lambda e: self.send_message())
        self.user_input.focus()
        
        # Send button
        self.send_button = Button(
            input_container,
            text="Send ➤",
            font=("Segoe UI", 11, "bold"),
            bg=self.button_color,
            fg="white",
            activebackground=self.button_hover,
            activeforeground="white",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.send_message,
            padx=20,
            pady=8
        )
        self.send_button.pack(side=tk.LEFT)
        
        # Footer with quick actions
        footer_frame = Frame(main_container, bg=self.bg_color)
        footer_frame.pack(fill=tk.X, pady=(10, 0))
        
        quick_actions = [
            ("📊 System Info", "system summary"),
            ("⚙️ Settings", "open settings"),
            ("🔋 Battery", "battery status"),
            ("📝 Notepad", "open notepad"),
            ("🔄 Refresh Mode", "refresh"),
            ("❓ Help", "help")
        ]
        
        for i, (text, cmd) in enumerate(quick_actions):
            btn = Button(
                footer_frame,
                text=text,
                font=("Segoe UI", 8),
                bg="#2c3e50",
                fg=self.text_color,
                activebackground="#34495e",
                activeforeground="white",
                relief=tk.FLAT,
                cursor="hand2",
                command=lambda c=cmd: self.quick_action(c),
                padx=8,
                pady=4
            )
            btn.grid(row=0, column=i, padx=3, sticky="ew")
            footer_frame.grid_columnconfigure(i, weight=1)
        
        # Display welcome message and detect mode
        self.display_welcome()
        self.update_mode_indicator()
    
    def display_welcome(self):
        """Display welcome message in chat."""
        welcome_msg = """
╔════════════════════════════════════════════════════════════════╗
║       Welcome to Windows Automation Assistant (Hybrid)         ║
╚════════════════════════════════════════════════════════════════╝

🤖 I can help you automate Windows tasks!

✨ HYBRID MODE:
   • 🟢 Online: Uses Grok AI for intelligent responses
   • 🔴 Offline: Uses local NLP with fuzzy matching

📌 Example Commands:
   • "open calculator"
   • "show cpu usage"
   • "create folder MyFiles"
   • "check battery"
   • "enable dark mode"
   • "shutdown computer" (with 30s delay)

💡 I understand typos! Try "opn setings" or "lauch notpad"

Type your command below or use quick action buttons!
────────────────────────────────────────────────────────────────
"""
        self.display_message(welcome_msg, "system")
    
    def display_message(self, message, tag="bot"):
        """Display a message in the chat window."""
        self.chat_display.config(state=tk.NORMAL)
        
        if tag == "user":
            prefix = "\n💬 You: "
        elif tag == "bot":
            prefix = "\n🤖 Bot: "
        elif tag == "system":
            prefix = ""
        else:
            prefix = "\n"
        
        self.chat_display.insert(tk.END, prefix, tag)
        self.chat_display.insert(tk.END, message + "\n")
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
    
    def update_mode_indicator(self):
        """Update the mode indicator in the header."""
        try:
            mode, status = get_current_mode()
            
            if mode == "online":
                indicator = "🟢 ONLINE MODE"
                color = self.online_color
            else:
                indicator = "🔴 OFFLINE MODE"
                color = self.offline_color
            
            self.mode_label.config(text=indicator, fg=color)
            
        except Exception as e:
            self.mode_label.config(text="⚠️ MODE ERROR", fg="#ffaa33")
    
    def send_message(self):
        """Handle sending user message."""
        user_text = self.user_input.get().strip()
        
        if not user_text:
            return
        
        # Clear input
        self.user_input.delete(0, tk.END)
        
        # Display user message
        self.display_message(user_text, "user")
        
        # Disable send button while processing
        self.send_button.config(state=tk.DISABLED, text="Processing...")
        
        # Process in background thread
        thread = threading.Thread(target=self.process_message, args=(user_text,))
        thread.daemon = True
        thread.start()
    
    def process_message(self, user_text):
        """Process user message and display response."""
        try:
            # Handle special commands
            if user_text.lower() in ["exit", "quit", "bye"]:
                self.display_message("Goodbye! Have a great day! 👋", "bot")
                self.root.after(1500, self.root.quit)
                return
            
            if user_text.lower() in ["refresh", "refresh mode", "check mode"]:
                self.update_mode_indicator()
                mode, status = get_current_mode()
                self.display_message(status, "system")
                self.root.after(0, lambda: self.send_button.config(state=tk.NORMAL, text="Send ➤"))
                return
            
            if user_text.lower() in ["help", "?"]:
                help_msg = """
📖 AVAILABLE COMMANDS:

🖥️  System Info:
   • cpu usage, memory usage, system info, battery status
   • check storage, show ip, what time is it

📁 Files & Folders:
   • list files, create folder [name], delete folder [name]

🚀 Open Apps:
   • open notepad/calculator/chrome/cmd/whatsapp
   • open task manager, open settings

⚙️  System Control:
   • enable dark mode, mute volume, increase/decrease volume
   • turn on/off bluetooth, lock pc, shutdown/restart pc

💡 I understand typos and variations!
"""
                self.display_message(help_msg, "system")
                self.root.after(0, lambda: self.send_button.config(state=tk.NORMAL, text="Send ➤"))
                return
            
            # Process command through hybrid core
            response, mode = process_user_input(user_text)
            
            # Display response with mode indicator
            mode_indicator = f"[{mode.upper()}] "
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.insert(tk.END, f"\n🤖 Bot {mode_indicator}", "bot")
            
            if mode == "online":
                self.chat_display.insert(tk.END, "", "mode_online")
            else:
                self.chat_display.insert(tk.END, "", "mode_offline")
            
            self.chat_display.insert(tk.END, response + "\n")
            self.chat_display.config(state=tk.DISABLED)
            self.chat_display.see(tk.END)
            
            # Update mode indicator
            self.root.after(0, self.update_mode_indicator)
        
        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            self.display_message(error_msg, "bot")
        
        finally:
            # Re-enable send button
            self.root.after(0, lambda: self.send_button.config(state=tk.NORMAL, text="Send ➤"))
    
    def quick_action(self, command):
        """Execute a quick action."""
        if command == "refresh":
            self.update_mode_indicator()
            mode, status = get_current_mode()
            self.display_message(status, "system")
        else:
            self.user_input.delete(0, tk.END)
            self.user_input.insert(0, command)
            self.send_message()


def launch_gui():
    """Launch the hybrid GUI chatbot."""
    root = tk.Tk()
    app = HybridChatbotGUI(root)
    root.mainloop()


if __name__ == "__main__":
    launch_gui()
