def detect_unrest(text):

    keywords = [
        "protest",
        "riot",
        "civil unrest",
        "demonstration"
    ]

    for k in keywords:
        if k in text:
            return True

    return False