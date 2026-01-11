import tkinter as tk
from tkinter import scrolledtext, Frame, Label, Entry, Button
from command_parser import parse_command
import threading


class ChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 Windows Automation Assistant")
        self.root.geometry("900x700")
        self.root.configure(bg="#1a1a2e")
        
        # Make window resizable
        self.root.minsize(600, 500)
        
        # Color scheme - Modern dark theme
        self.bg_color = "#1a1a2e"
        self.chat_bg = "#16213e"
        self.user_msg_bg = "#0f3460"
        self.bot_msg_bg = "#1a1a2e"
        self.text_color = "#e0e0e0"
        self.accent_color = "#00adb5"
        self.button_color = "#00adb5"
        self.button_hover = "#00c9d1"
        
        # Header
        header_frame = Frame(root, bg=self.accent_color, height=60)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header_frame.pack_propagate(False)
        
        title_label = Label(
            header_frame, 
            text="🤖 Windows Automation Assistant",
            font=("Segoe UI", 18, "bold"),
            bg=self.accent_color,
            fg="white"
        )
        title_label.pack(pady=15)
        
        subtitle_label = Label(
            header_frame,
            text="AI-powered Windows automation at your command",
            font=("Segoe UI", 9),
            bg=self.accent_color,
            fg="#e8f4f8"
        )
        subtitle_label.pack()
        
        # Main container for chat and input - using grid for better control
        main_container = Frame(root, bg=self.bg_color)
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        main_container.grid_rowconfigure(0, weight=1)
        main_container.grid_rowconfigure(1, weight=0)
        main_container.grid_columnconfigure(0, weight=1)
        
        # Chat display area with custom styling
        chat_frame = Frame(main_container, bg=self.chat_bg)
        chat_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
        
        self.chat_area = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            font=("Segoe UI", 11),
            bg=self.chat_bg,
            fg=self.text_color,
            insertbackground=self.accent_color,
            relief=tk.FLAT,
            padx=15,
            pady=15,
            spacing3=8
        )
        self.chat_area.pack(fill=tk.BOTH, expand=True)
        self.chat_area.config(state=tk.DISABLED)
        
        # Configure tags for different message types
        self.chat_area.tag_config("user", foreground="#7dd3fc", font=("Segoe UI", 11, "bold"))
        self.chat_area.tag_config("bot", foreground="#86efac", font=("Segoe UI", 11, "bold"))
        self.chat_area.tag_config("user_msg", foreground=self.text_color, lmargin1=20, lmargin2=20)
        self.chat_area.tag_config("bot_msg", foreground="#e0e0e0", lmargin1=20, lmargin2=20)
        self.chat_area.tag_config("success", foreground="#4ade80")
        self.chat_area.tag_config("error", foreground="#f87171")
        self.chat_area.tag_config("info", foreground="#60a5fa")
        
        # Input area - fixed at bottom
        input_container = Frame(main_container, bg=self.bg_color)
        input_container.grid(row=1, column=0, sticky="ew")
        
        input_frame = Frame(input_container, bg=self.chat_bg, relief=tk.FLAT, bd=2, highlightthickness=1, highlightbackground=self.accent_color)
        input_frame.pack(fill=tk.X, ipady=10)
        
        self.user_input = Entry(
            input_frame,
            font=("Segoe UI", 12),
            bg=self.chat_bg,
            fg=self.text_color,
            insertbackground=self.accent_color,
            relief=tk.FLAT,
            bd=0
        )
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=15, pady=8)
        self.user_input.bind("<Return>", self.send_message)
        self.user_input.focus()
        
        # Send button with hover effect
        self.send_btn = Button(
            input_frame,
            text="Send ➤",
            font=("Segoe UI", 11, "bold"),
            bg=self.button_color,
            fg="white",
            activebackground=self.button_hover,
            activeforeground="white",
            relief=tk.FLAT,
            cursor="hand2",
            padx=25,
            pady=10,
            command=self.send_message
        )
        self.send_btn.pack(side=tk.RIGHT, padx=15)
        
        # Bind hover effects
        self.send_btn.bind("<Enter>", lambda e: self.send_btn.config(bg=self.button_hover))
        self.send_btn.bind("<Leave>", lambda e: self.send_btn.config(bg=self.button_color))
        
        # Welcome message
        welcome_msg = (
            "Hello! 👋 I'm your Windows Automation Assistant.\n\n"
            "I can help you with:\n"
            "• Opening applications (WhatsApp, Calculator, Notepad, etc.)\n"
            "• System information (CPU, memory, battery, storage)\n"
            "• Controlling volume and Bluetooth\n"
            "• Managing files and folders\n"
            "• And much more!\n\n"
            "💡 Type 'help' to see all available commands, or just ask me naturally!\n"
            "Example: 'open calculator' or 'check my battery status'"
        )
        self.add_message("Bot", welcome_msg)

    def add_message(self, sender, message):
        """Add a message to the chat area with styling"""
        self.chat_area.config(state=tk.NORMAL)
        
        if sender == "You":
            self.chat_area.insert(tk.END, "You", "user")
            self.chat_area.insert(tk.END, "\n")
            # Apply emoji-based formatting
            formatted_message = self.format_message(message)
            self.chat_area.insert(tk.END, formatted_message, "user_msg")
        else:
            self.chat_area.insert(tk.END, "🤖 Assistant", "bot")
            self.chat_area.insert(tk.END, "\n")
            formatted_message = self.format_message(message)
            self.chat_area.insert(tk.END, formatted_message, "bot_msg")
        
        self.chat_area.insert(tk.END, "\n\n")
        self.chat_area.yview(tk.END)
        self.chat_area.config(state=tk.DISABLED)
    
    def format_message(self, message):
        """Format message with better readability"""
        # Keep the message as is - emojis and formatting are already good
        return message

    def send_message(self, event=None):
        """Handle sending a message"""
        text = self.user_input.get().strip()
        if not text:
            return
        
        # Disable input while processing
        self.user_input.config(state=tk.DISABLED)
        self.send_btn.config(state=tk.DISABLED, text="Processing...")
        
        # Display user message
        self.add_message("You", text)
        self.user_input.delete(0, tk.END)
        
        # Process command in a separate thread to keep GUI responsive
        def process_command():
            response = parse_command(text)
            
            # Handle special responses
            if response == "EXIT":
                self.add_message("Bot", "👋 Goodbye! Have a great day!")
                self.root.after(1500, self.root.destroy)
                return
            
            if response == "CLEAR":
                self.chat_area.config(state=tk.NORMAL)
                self.chat_area.delete(1.0, tk.END)
                self.chat_area.config(state=tk.DISABLED)
                self.add_message("Bot", "🧹 Chat cleared!")
            else:
                self.add_message("Bot", str(response))
            
            # Re-enable input
            self.user_input.config(state=tk.NORMAL)
            self.send_btn.config(state=tk.NORMAL, text="Send ➤")
            self.user_input.focus()
        
        # Run in thread to prevent GUI freezing
        thread = threading.Thread(target=process_command, daemon=True)
        thread.start()


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatbotGUI(root)
    root.mainloop()
