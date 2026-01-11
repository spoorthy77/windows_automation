import os
from command_parser import parse_command
from logger import log_event
from voice import speak


def main():
    print("=" * 60)
    print("🤖 WINDOWS AUTOMATION CHATBOT")
    print("=" * 60)
    print("💬 Chat naturally with me to automate your Windows tasks!")
    print("📖 Type 'help' or '7' to see commands | Type 'exit' or '8' to quit")
    print("=" * 60)
    print()

    # Voice settings
    voice_enabled = True
    speak_only_greeting = True   # ✅ Only greeting will speak

    # Speak greeting only
    if voice_enabled:
        speak("Windows Automation Chatbot Ready")

    # Pending confirmation states
    pending_action = None

    while True:
        user_input = input("\n💬 You: ").strip()
        
        if not user_input:
            continue
            
        response = parse_command(user_input)

        # EXIT
        if response == "EXIT":
            print("\n🤖 Bot: Goodbye! Have a great day! 👋")
            log_event(user_input, "Goodbye! (Program Exit)")
            break

        # CLEAR
        if response == "CLEAR":
            os.system("cls")
            print("🤖 Bot: Screen cleared ✨")
            log_event(user_input, "Screen cleared")
            continue

        # VOICE CONTROLS
        if response == "VOICE_ON":
            voice_enabled = True
            print("🤖 Bot: 🔊 Voice output enabled.")
            log_event(user_input, "Voice enabled")
            continue

        if response == "VOICE_OFF":
            voice_enabled = False
            print("🤖 Bot: 🔇 Voice output disabled.")
            log_event(user_input, "Voice disabled")
            continue

        if response == "VOICE_TOGGLE":
            voice_enabled = not voice_enabled
            status = "enabled 🔊" if voice_enabled else "disabled 🔇"
            print(f"🤖 Bot: Voice output {status}.")
            log_event(user_input, f"Voice toggled: {status}")
            continue

        # SHUTDOWN/RESTART CONFIRMATIONS
        if response == "CONFIRM_SHUTDOWN":
            pending_action = "shutdown"
            print("🤖 Bot: ⚠️  Are you sure you want to SHUTDOWN? Type 'yes' to confirm or 'no' to cancel.")
            log_event(user_input, "Shutdown confirmation requested")
            continue

        if response == "CONFIRM_RESTART":
            pending_action = "restart"
            print("🤖 Bot: ⚠️  Are you sure you want to RESTART? Type 'yes' to confirm or 'no' to cancel.")
            log_event(user_input, "Restart confirmation requested")
            continue

        # Handle confirmation responses
        if pending_action:
            if user_input.lower() in ["yes", "y"]:
                if pending_action == "shutdown":
                    from actions import shutdown_pc
                    result = shutdown_pc()
                    print(f"🤖 Bot: {result}")
                    log_event(user_input, result)
                elif pending_action == "restart":
                    from actions import restart_pc
                    result = restart_pc()
                    print(f"🤖 Bot: {result}")
                    log_event(user_input, result)
                pending_action = None
                continue
            elif user_input.lower() in ["no", "n", "cancel"]:
                print("🤖 Bot: ✅ Action cancelled. Your system is safe!")
                log_event(user_input, f"{pending_action.capitalize()} cancelled by user")
                pending_action = None
                continue

        # NORMAL RESPONSE
        print(f"🤖 Bot: {response}")
        log_event(user_input, str(response))


if __name__ == "__main__":
    main()
