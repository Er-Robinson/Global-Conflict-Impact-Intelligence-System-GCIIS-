def detect_energy_risk(text):

    keywords = [
        "oil",
        "gas",
        "pipeline",
        "energy crisis",
        "fuel shortage"
    ]

    for k in keywords:
        if k in text:
            return True

    return False