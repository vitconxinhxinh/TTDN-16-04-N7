"""
Script để train model phân loại văn bản từ tên file
"""
import joblib
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
import numpy as np

# Dữ liệu training mẫu - có thể mở rộng sau
TRAINING_DATA = [
    # Labor contracts
    ("hợp đồng lao động 2024", "labor_contract"),
    ("hợp_dong_lao_dong", "labor_contract"),
    ("labor contract", "labor_contract"),
    ("employment agreement", "labor_contract"),
    ("hợp đồng làm việc", "labor_contract"),
    ("quyết định tuyển dụng", "labor_contract"),
    
    # Sales contracts
    ("hợp đồng mua bán", "sales_contract"),
    ("hop_dong_mua_ban", "sales_contract"),
    ("sales contract", "sales_contract"),
    ("sales agreement", "sales_contract"),
    ("purchase agreement", "sales_contract"),
    ("hợp đồng bán hàng", "sales_contract"),
    ("đơn đặt hàng", "sales_contract"),
    
    # Service contracts
    ("hợp đồng dịch vụ", "service_contract"),
    ("hop_dong_dich_vu", "service_contract"),
    ("service contract", "service_contract"),
    ("service agreement", "service_contract"),
    ("hợp đồng cung cấp dịch vụ", "service_contract"),
    
    # Lease contracts
    ("hợp đồng thuê", "lease_contract"),
    ("hop_dong_thue", "lease_contract"),
    ("lease contract", "lease_contract"),
    ("rental agreement", "lease_contract"),
    ("hợp đồng thuê nhà", "lease_contract"),
    ("hợp đồng cho thuê", "lease_contract"),
    
    # NDA contracts
    ("hợp đồng bảo mật", "nda_contract"),
    ("hop_dong_bao_mat", "nda_contract"),
    ("nda agreement", "nda_contract"),
    ("non-disclosure agreement", "nda_contract"),
    ("confidentiality agreement", "nda_contract"),
    ("thỏa thuận bảo mật", "nda_contract"),
    
    # Quotations
    ("báo giá", "quotation"),
    ("bao_gia", "quotation"),
    ("quotation", "quotation"),
    ("quote", "quotation"),
    ("giá chào", "quotation"),
    ("dự toán", "quotation"),
    
    # Legal documents
    ("tài liệu pháp lý", "legal"),
    ("tai_lieu_phap_ly", "legal"),
    ("legal document", "legal"),
    ("hướng dẫn pháp lý", "legal"),
    ("điều khoản", "legal"),
    ("chính sách", "legal"),
]

def train_and_save_model():
    """Train model và lưu thành file pkl"""
    
    # Tách text và label
    texts = [item[0] for item in TRAINING_DATA]
    labels = [item[1] for item in TRAINING_DATA]
    
    # Tạo vectorizer và model
    vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(2, 3), lowercase=True)
    svm = LinearSVC(max_iter=2000, random_state=42, dual=False)
    
    # Vectorize text
    X = vectorizer.fit_transform(texts)
    y = labels
    
    # Train model
    svm.fit(X, y)
    
    # Lưu model và vectorizer
    script_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(script_dir, 'model.pkl')
    vectorizer_path = os.path.join(script_dir, 'vectorizer.pkl')
    
    joblib.dump(svm, model_path)
    joblib.dump(vectorizer, vectorizer_path)
    
    print(f"✓ Model saved to {model_path}")
    print(f"✓ Vectorizer saved to {vectorizer_path}")
    
    # Test model
    print("\nTesting model:")
    test_cases = [
        "hợp đồng lao động",
        "hợp đồng mua bán", 
        "hợp đồng dịch vụ",
        "hợp đồng thuê",
        "hợp đồng bảo mật",
        "báo giá",
    ]
    
    for text in test_cases:
        X_test = vectorizer.transform([text])
        pred = svm.predict(X_test)[0]
        confidence = max(svm.decision_function(X_test)[0])
        print(f"  '{text}' -> {pred}")

if __name__ == "__main__":
    train_and_save_model()
