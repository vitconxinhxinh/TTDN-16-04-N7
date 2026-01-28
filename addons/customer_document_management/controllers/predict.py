import joblib
import numpy as np
import sys
import os
import json

# Lấy đường dẫn của thư mục chứa script này
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_FILE = os.path.join(SCRIPT_DIR, "model.pkl")
VECTORIZER_FILE = os.path.join(SCRIPT_DIR, "vectorizer.pkl")


def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()


def main():
    if len(sys.argv) < 2:
        print("other")
        return
    
    text = sys.argv[1].strip()
    if not text:
        print("other")
        return

    try:
        # Load model và vectorizer
        if not os.path.exists(MODEL_FILE):
            print("other")
            return
        if not os.path.exists(VECTORIZER_FILE):
            print("other")
            return
            
        model = joblib.load(MODEL_FILE)
        vectorizer = joblib.load(VECTORIZER_FILE)
        
        # Vectorize text
        text_vectorized = vectorizer.transform([text])
        
        # Predict
        decision_scores = model.decision_function(text_vectorized)[0]
        probs = softmax(decision_scores)
        best_idx = np.argmax(probs)
        
        predicted_label = model.classes_[best_idx]
        confidence = float(probs[best_idx])
        
        # Giới hạn confidence trong khoảng 0-1 và convert sang phần trăm
        confidence = max(0.0, min(1.0, confidence)) * 100
        
        # In kết quả dưới dạng JSON để Odoo có thể parse
        result = {
            'label': predicted_label,
            'confidence': round(confidence, 2)
        }
        print(json.dumps(result, ensure_ascii=False))
        
    except Exception as e:
        # In lỗi để debug
        import traceback
        error_msg = traceback.format_exc()
        # Fallback: in nhãn other nếu có lỗi
        print("other")


if __name__ == "__main__":
    main()

