import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from db import get_unprocessed_news, insert_sentiment

MODEL_NAME = "ProsusAI/finbert"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
model.eval()

def analyze_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    
    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        
        predicted_class = torch.argmax(probs, dim=-1).item()
        score = probs[0][predicted_class].item()
        
    labels = ["negative", "neutral", "positive"]
    label = labels[predicted_class]
    
    return score, label

def process_news_sentiment():
    news_items = get_unprocessed_news()
    
    if not news_items:
        print("No new headlines to process")
        return
    
    print(f"Processing {len(news_items)} headlines...")
    
    results = []
    for item in news_items:
        score, label = analyze_sentiment(item["headline"])
        results.append({"news_id": item["id"], "score": score, "label": label})
    
    insert_sentiment(results)
    print(f"Updated {len(results)} articles")

if __name__ == "__main__":
    process_news_sentiment()
