def classify_conflict(text):

    text = text.lower()

    if any(w in text for w in ["missile","attack","bomb","strike","drone"]):
        return "Military"

    if any(w in text for w in ["oil","gas","trade","sanctions","shipping"]):
        return "Economic"

    if any(w in text for w in ["refugee","displaced","evacuated"]):
        return "Humanitarian"

    if any(w in text for w in ["election","government","policy"]):
        return "Political"

    return "General"