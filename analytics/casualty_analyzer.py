import re

def extract_casualties(text):

    casualties = {
        "soldiers_killed":0,
        "civilians_killed":0,
        "children_killed":0,
        "women_killed":0,
        "injured":0
    }

    numbers = re.findall(r'\d+', text)

    if "soldier" in text or "troop" in text:
        if numbers:
            casualties["soldiers_killed"] = int(numbers[0])

    if "civilian" in text:
        if numbers:
            casualties["civilians_killed"] = int(numbers[0])

    if "child" in text:
        if numbers:
            casualties["children_killed"] = int(numbers[0])

    if "woman" in text or "women" in text:
        if numbers:
            casualties["women_killed"] = int(numbers[0])

    if "injured" in text or "wounded" in text:
        if numbers:
            casualties["injured"] = int(numbers[0])

    return casualties