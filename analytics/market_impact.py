def detect_market_impact(text):

    keywords = [
        "stock market",
        "market crash",
        "inflation",
        "currency fall"
    ]

    for k in keywords:
        if k in text:
            return True

    return False