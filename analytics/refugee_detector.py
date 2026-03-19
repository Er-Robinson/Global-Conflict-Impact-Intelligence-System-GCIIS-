def detect_refugee_crisis(text):

    if "refugee" in text or "displaced" in text or "fleeing" in text:
        return True

    return False