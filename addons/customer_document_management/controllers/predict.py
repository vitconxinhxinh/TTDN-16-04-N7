import joblib
import numpy as np
import sys
import os

# Lấy đường dẫn của thư mục chứa script này
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_FILE = os.path.join(SCRIPT_DIR, "model.pkl")
VECTORIZER_FILE = os.path.join(SCRIPT_DIR, "vectorizer.pkl")

# Map từ nhãn model sang nhãn Odoo
LABEL_MAP = {
    'labor_contract': 'contract',
    'lease_contract': 'contract',
    'sales_contract': 'contract',
    'service_contract': 'contract',
    'nda_contract': 'legal',
}


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
        model = joblib.load(MODEL_FILE)
        vectorizer = joblib.load(VECTORIZER_FILE)
        
        # Vectorize text
        text_vectorized = vectorizer.transform([text])
        
        # Predict
        decision_scores = model.decision_function(text_vectorized)[0]
        probs = softmax(decision_scores)
        best_idx = np.argmax(probs)
        predicted_label = model.classes_[best_idx]
        
        # Map sang nhãn Odoo
        odoo_label = LABEL_MAP.get(predicted_label, 'other')
        print(odoo_label)
    except Exception as e:
        # In ra lỗi để debug nếu cần (có thể comment lại sau)
        # print(f"Error: {e}", file=sys.stderr)
        print("other")


if __name__ == "__main__":
    main()
