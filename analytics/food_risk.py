def detect_food_risk(text):

    keywords = [
        "grain",
        "wheat",
        "food shortage",
        "famine",
        "crop damage"
    ]

    for k in keywords:
        if k in text:
            return True

    return False