import pyttsx3

# Create engine only once (best practice)
engine = pyttsx3.init()

# Optional: control voice speed and volume
engine.setProperty("rate", 170)      # speed (default ~200)
engine.setProperty("volume", 1.0)    # volume 0.0 to 1.0


def speak(text: str):
    """
    Convert text to speech using offline pyttsx3.
    """
    if not text:
        return

    # Avoid speaking very large outputs (systeminfo/ipconfig etc.)
    if len(text) > 250:
        text = text[:250] + " ... Output trimmed."

    engine.say(text)
    engine.runAndWait()
