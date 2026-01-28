"""
Script để test model có đang hoạt động đúng không
"""
import joblib
import numpy as np
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_FILE = os.path.join(SCRIPT_DIR, "model.pkl")
VECTORIZER_FILE = os.path.join(SCRIPT_DIR, "vectorizer.pkl")

def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()

# Load model
model = joblib.load(MODEL_FILE)
vectorizer = joblib.load(VECTORIZER_FILE)

print("="*60)
print("MODEL INFORMATION")
print("="*60)
print(f"Model type: {type(model)}")
print(f"Model classes: {model.classes_}")
print(f"Vectorizer type: {type(vectorizer)}")
print()

# Test cases
test_cases = [
    "hợp đồng lao động",
    "hợp đồng mua bán",
    "hợp đồng dịch vụ",
    "hợp đồng thuê",
    "hợp đồng bảo mật",
    "báo giá",
    "tài liệu pháp lý",
]

print("="*60)
print("TEST RESULTS")
print("="*60)
for text in test_cases:
    X = vectorizer.transform([text])
    pred = model.predict(X)[0]
    scores = model.decision_function(X)[0]
    probs = softmax(scores)
    confidence = max(probs) * 100
    
    print(f"\nText: '{text}'")
    print(f"  Prediction: {pred}")
    print(f"  Confidence: {confidence:.2f}%")
    print(f"  Scores: {scores}")
    print(f"  Probs: {probs}")
