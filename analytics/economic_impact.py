def estimate_economic_impact(text):

    impact = {
        "oil_risk": False,
        "food_risk": False,
        "trade_risk": False
    }

    if "oil" in text or "pipeline" in text or "energy" in text:
        impact["oil_risk"] = True

    if "grain" in text or "food" in text or "wheat" in text:
        impact["food_risk"] = True

    if "sanction" in text or "trade ban" in text:
        impact["trade_risk"] = True

    return impact