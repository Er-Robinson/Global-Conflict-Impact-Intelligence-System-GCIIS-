from transformers import pipeline

sentiment_model = pipeline("sentiment-analysis")

def get_sentiment(text):
    try:
        result = sentiment_model(text[:512])[0]
        return result["label"], result["score"]
    except:
        return "NEUTRAL", 0