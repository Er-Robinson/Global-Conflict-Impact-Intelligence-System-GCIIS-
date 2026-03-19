def detect_location(text):

    locations = [
        "strait of hormuz",
        "black sea",
        "south china sea",
        "gaza",
        "ukraine",
        "iran",
        "israel"
    ]

    text = text.lower()

    for loc in locations:
        if loc in text:
            return loc

    return "Unknown"