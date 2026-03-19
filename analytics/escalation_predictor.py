def predict_escalation(severity):

    if severity > 50:
        return "HIGH"

    if severity > 20:
        return "MEDIUM"

    return "LOW"