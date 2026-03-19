def compute_war_severity(casualties, text):

    score = 0

    text = text.lower()

    # casualty impact
    if casualties > 0:
        score += min(casualties / 10, 5)

    high_keywords = [
        "war",
        "missile",
        "bomb",
        "attack",
        "airstrike",
        "invasion",
        "military"
    ]

    medium_keywords = [
        "conflict",
        "troops",
        "strike",
        "defense"
    ]

    for word in high_keywords:
        if word in text:
            score += 2

    for word in medium_keywords:
        if word in text:
            score += 1

    return min(score, 10)