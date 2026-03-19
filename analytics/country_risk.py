def compute_country_risk(severity, economic_risk):

    risk = severity

    if economic_risk["oil_risk"]:
        risk += 10

    if economic_risk["food_risk"]:
        risk += 8

    if economic_risk["trade_risk"]:
        risk += 6

    return risk