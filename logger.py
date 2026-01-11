from datetime import datetime


LOG_FILE = "logs.txt"


def log_event(user_input: str, response: str):
    """
    Save user command and bot response into a log file.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # trim very large responses (like systeminfo)
    if len(response) > 1200:
        response = response[:1200] + "\n...OUTPUT TRIMMED..."

    log_text = (
        f"\n[{timestamp}]\n"
        f"User: {user_input}\n"
        f"Bot: {response}\n"
        f"{'-'*60}\n"
    )

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_text)
