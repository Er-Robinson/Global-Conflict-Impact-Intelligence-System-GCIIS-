def detect_weapon(text):

    weapons = [
        "missile",
        "drone",
        "fighter",
        "tank",
        "airstrike",
        "rocket"
    ]

    found = []

    text = text.lower()

    for w in weapons:
        if w in text:
            found.append(w)

    return found