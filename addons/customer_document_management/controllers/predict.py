import joblib
import numpy as np

MODEL_FILE = "model.pkl"
TEST_FILE = "new_contract.txt"


def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()


def main():
    model = joblib.load(MODEL_FILE)

    with open(TEST_FILE, "r", encoding="utf-8") as f:
        text = f.read().strip()

    decision_scores = model.decision_function([text])[0]

    probs = softmax(decision_scores)
    best_idx = np.argmax(probs)

    predicted_label = model.classes_[best_idx]
    confidence = probs[best_idx] * 100

    print(f"📄 Loại hợp đồng: {predicted_label}")
    print(f"🎯 Độ tin cậy: {confidence:.2f} %")


if __name__ == "__main__":
    main()
