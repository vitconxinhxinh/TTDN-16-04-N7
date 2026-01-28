<h2 align="center">
    <a href="https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin">
    🎓 Faculty of Information Technology (DaiNam University)
    </a>
</h2>

<h2 align="center">
   HỆ THỐNG QUẢN LÝ NHÂN SỰ - KHÁCH HÀNG - VĂN BẢN
</h2>

<div align="center">
    <p align="center">
        <img src="docs/aiotlab_logo.png" alt="AIoTLab Logo" width="170"/>
        <img src="docs/fitdnu_logo.png" alt="FIT DNU Logo" width="180"/>
        <img src="docs/dnu_logo.png" alt="DaiNam University Logo" width="200"/>
    </p>

[![AIoTLab](https://img.shields.io/badge/AIoTLab-green?style=for-the-badge)](https://www.facebook.com/DNUAIoTLab)
[![Faculty of Information Technology](https://img.shields.io/badge/Faculty%20of%20Information%20Technology-blue?style=for-the-badge)](https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin)
[![DaiNam University](https://img.shields.io/badge/DaiNam%20University-orange?style=for-the-badge)](https://dainam.edu.vn)

</div>

---

## 📖 1. Giới thiệu

Hệ thống **ERP (Enterprise Resource Planning)** được xây dựng trên nền tảng **Odoo 17**, tối ưu hóa quản lý với ba module chính:

### 🧑‍💼 Module Nhân sự
Quản lý toàn diện nguồn nhân lực doanh nghiệp:
- **Quản lý cơ cấu tổ chức**: Phòng ban, chức vụ, cấp bậc
- **Quản lý nhân viên**: Hồ sơ, hợp đồng lao động, lịch sử công tác
- **Hệ thống chấm công**: Tự động với các ca làm việc linh hoạt
- **Tính lương**: Tự động tính lương, phụ cấp, khấu trừ, thưởng phạt
- **Báo cáo**: Thống kê nhân sự, công, lương theo đa chiều

### 👥 Module Khách hàng
Quản lý quan hệ khách hàng hiệu quả:
- **Thông tin khách hàng**: Hồ sơ, liên hệ, địa chỉ
- **Phân loại khách hàng**: Loại khách hàng, nhóm khách hàng
- **Lịch sử giao dịch**: Theo dõi đơn hàng, thanh toán
- **Tương tác**: Quản lý email, ghi chú, hoạt động
- **Báo cáo CRM**: Phân tích khách hàng, doanh thu

### 📄 Module Quản lý Văn bản
Quản lý tài liệu và văn bản tự động phân loại:
- **Quản lý tài liệu**: Lưu trữ, tổ chức tài liệu
- **Phân loại tự động**: AI phân loại văn bản (Nhân sự/Khách hàng/Văn bản)
- **Quy trình phê duyệt**: Workflow duyệt văn bản
- **Tìm kiếm nâng cao**: Search toàn văn bản
- **Lịch sử thay đổi**: Theo dõi version, audit log

---

## 🛠️ 2. Công nghệ & Kiến trúc hệ thống

### Stack công nghệ chính

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Odoo-17.0-714B67?style=for-the-badge&logo=odoo&logoColor=white"/>
  <img src="https://img.shields.io/badge/PostgreSQL-14-316192?style=for-the-badge&logo=postgresql&logoColor=white"/>
  <img src="https://img.shields.io/badge/Docker-Latest-2496ED?style=for-the-badge&logo=docker&logoColor=white"/>
  <img src="https://img.shields.io/badge/Machine_Learning-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white"/>
  <img src="https://img.shields.io/badge/Scikit_Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white"/>
</p>

### Kiến trúc hệ thống
- **Backend**: Odoo Framework (Python) - ORM, MVC Pattern
- **Frontend**: Odoo Web Client (JavaScript/XML/QWeb)  
- **Database**: PostgreSQL với indexing tối ưu
- **Machine Learning**: Scikit-learn, Pandas, NumPy (Phân loại văn bản)
- **Deployment**: Docker, Docker Compose
- **Automation**: Cron Jobs, Background Jobs

### Tính năng nổi bật
✨ **Tích hợp liền mạch** giữa 3 module (Nhân sự - Khách hàng - Văn bản)  
🤖 **AI phân loại văn bản** tự động theo loại  
📊 **Dashboard trực quan** với biểu đồ và thống kê  
🔄 **Tự động hóa** quy trình nghiệp vụ  
🔐 **Phân quyền chi tiết** theo vai trò người dùng  

---

## 📸 3. Hình ảnh giao diện hệ thống

### Module nhân sự
<p align="center">
  <img src="docs/dashnhansu.png" alt="" width="800"/>
  <br/>
  <em>Dashboard nhân sự</em>
</p>
<p align="center">
  <img src="docs/themnhanvien.png" alt="" width="800"/>
  <br/>
  <em>Thêm nhân viên</em>
</p>
<p align="center">
  <img src="docs/chamcong.png" alt="" width="800"/>
  <br/>
  <em>Chấm công</em>
</p>
<p align="center">
  <img src="docs/tinhluong.png" alt="" width="800"/>
  <br/>
  <em>Tính lương</em>
</p>

### Module khách hàng và văn bản
<p align="center">
  <img src="docs/dashkhachhang.png" alt="" width="800"/>
  <br/>
  <em>Dashboard Khách hàng</em>
</p>
<p align="center">
  <img src="docs/themkhachhang.png" alt="" width="800"/>
  <br/>
  <em>Thêm khách hàng</em>
</p>
<p align="center">
  <img src="docs/dashvanban.png" alt="" width="800"/>
  <br/>
  <em>Dashboard Quản lý Văn bản</em>
</p>
<p align="center">
  <img src="docs/themhopdong1.png" alt="" width="800"/>
  <br/>
  <em>Thêm văn bản</em>
</p>
<p align="center">
  <img src="docs/AI.png" alt="" width="800"/>
  <br/>
  <em>Tích hợp AI phân loại văn bản</em>
</p>

---

## 🚀 4. Hướng dẫn cài đặt & Sử dụng

### 📋 Yêu cầu hệ thống

#### Phần mềm yêu cầu
- **Python**: 3.10 hoặc cao hơn
- **PostgreSQL**: 12+ (khuyến nghị 14 hoặc 15)
- **Docker & Docker Compose**: Latest version (nếu dùng Docker)
- **Git**: Để clone repository
- **Web Browser**: Chrome, Firefox, hoặc Edge (phiên bản mới nhất)

---

### 🐳 Cài đặt nhanh với Docker (Khuyến nghị)

Đây là cách đơn giản nhất để chạy hệ thống:

```bash
# 1. Clone repository
git clone <repository-url>
cd odoo-fitdnu

# 2. Khởi động Docker containers
docker-compose up -d

# 3. Kiểm tra logs
docker-compose logs -f

# 4. Đợi khoảng 2-3 phút để Odoo khởi động hoàn tất
```

**Truy cập hệ thống:**
- URL: `http://localhost:8069`
- Database: `odoo`
- Email: `admin`
- Password: `admin`

**Quản lý Docker:**
```bash
# Dừng hệ thống
docker-compose down

# Khởi động lại
docker-compose restart

# Xem logs
docker-compose logs -f odoo

# Xóa toàn bộ (bao gồm data)
docker-compose down -v
```

---

### 💻 Cài đặt thủ công (Development)

#### Bước 1: Cài đặt PostgreSQL

**Trên Windows:**
```powershell
# Download và cài PostgreSQL từ https://www.postgresql.org/download/windows/
# Sau khi cài đặt, tạo database và user:

# Mở psql hoặc pgAdmin
CREATE USER odoo WITH PASSWORD 'odoo';
CREATE DATABASE odoo OWNER odoo;
GRANT ALL PRIVILEGES ON DATABASE odoo TO odoo;
```

**Trên Linux/Ubuntu:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib

# Tạo user và database
sudo -u postgres createuser -s odoo
sudo -u postgres psql -c "ALTER USER odoo WITH PASSWORD 'odoo';"
sudo -u postgres createdb -O odoo odoo
```

#### Bước 2: Clone Repository và cài đặt Python

```bash
# Clone project
git clone https://github.com/vitconxinhxinh/TTDN-16-04-N7
cd odoo-fitdnu

# Tạo virtual environment (khuyến nghị)
python -m venv venv

# Kích hoạt virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Cài đặt dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

#### Bước 3: Cài đặt Machine Learning packages

```bash
# Di chuyển đến module Văn bản
cd addons/customer_document_management

# Windows:
.\install_ml_packages.sh
# hoặc cài thủ công:
pip install scikit-learn pandas numpy joblib matplotlib seaborn

# Linux/Mac:
bash install_ml_packages.sh

cd ../..
```

#### Bước 4: Cấu hình Odoo

```bash
# Copy file cấu hình mẫu (nếu có)
cp odoo.conf.template odoo.conf

# Hoặc tạo file odoo.conf mới
```

**File `odoo.conf` cần điều chỉnh:**

```ini
[options]
# Database Configuration
db_host = localhost
db_port = 5432
db_user = odoo
db_password = odoo
# db_name = False  # Để False cho phép chọn DB từ giao diện
list_db = True

# Admin Password (để quản lý databases)
admin_passwd = your_strong_password_here

# Server Configuration
http_interface = 0.0.0.0
http_port = 8069

# Addons Path
addons_path = ./addons,./custom-addons

# Data Directory
data_dir = ./db_data

# Performance & Resources
workers = 0  # 0 để chạy dev mode, production dùng 4-8
max_cron_threads = 2

# Logging
logfile = ./odoo.log
log_level = info
log_handler = :INFO

# Security (Production)
# proxy_mode = True
# db_filter = ^odoo$

# Development
# dev_mode = reload,qweb,werkzeug,xml
```

**Lưu ý quan trọng:**
- `admin_passwd`: Mật khẩu master để tạo/xóa database (đổi thành mật khẩu mạnh)
- `workers = 0`: Dùng cho development, production nên dùng 4-8 workers
- `db_filter`: Uncomment trong production để giới hạn database
- `addons_path`: Đảm bảo đường dẫn đúng với thư mục addons và custom-addons

**Đối với Windows, điều chỉnh đường dẫn:**
```ini
addons_path = E:\odoo-fitdnu\addons,E:\odoo-fitdnu\custom-addons
data_dir = E:\odoo-fitdnu\db_data
logfile = E:\odoo-fitdnu\odoo.log
```

#### Bước 5: Khởi động Odoo

```bash
# Khởi động Odoo với database mới
python odoo-bin -c odoo.conf -d odoo -i base --without-demo=all

# Sau lần đầu, chỉ cần:
python odoo-bin -c odoo.conf
```

#### Bước 6: Cài đặt Custom Modules

1. Truy cập `http://localhost:8069`
2. Đăng nhập với `admin` / `admin`
3. Vào **Apps** → Bật **Developer Mode**
4. Click **Update Apps List**
5. Tìm và cài đặt theo thứ tự:
   - `Quản lý Nhân sự` (hr_management)
   - `Quản lý Khách hàng` (crm_management)
   - `Quản lý Văn bản` (customer_document_management)

---

# 🤖 Training AI Model (Phân loại Hợp đồng)

Module sử dụng Machine Learning để phân loại các loại hợp đồng tiếng Việt.

## Chuẩn bị dữ liệu

```bash
# Tiền xử lý dữ liệu
python preprocess.py
```

## Training Model

```bash
# Chạy script training
python train.py

# Test model
python predict.py
```

## Các loại hợp đồng được hỗ trợ

- **labor_contract** - Hợp đồng lao động
- **service_contract** - Hợp đồng dịch vụ
- **sales_contract** - Hợp đồng bán hàng
- **lease_contract** - Hợp đồng thuê
- **nda_contract** - Hợp đồng bảo mật

## Cấu trúc thư mục

```
d:\AI\
├── data/
│   ├── raw/              # File hợp đồng gốc (.txt)
│   ├── dataset.csv       # Dataset sau xử lý
│   └── labels.csv        # File nhãn
├── train.py              # Script training
├── preprocess.py         # Tiền xử lý dữ liệu
├── predict.py            # Dự đoán loại hợp đồng
├── model.pkl             # Model đã train
└── vectorizer.pkl        # TF-IDF vectorizer
```

## Yêu cầu

- Python 3.7+
- pandas, scikit-learn, joblib, numpy

## Lưu ý

- Sử dụng TfidfVectorizer (max 5000 features, ngram 1-2)
- LogisticRegression với `class_weight="balanced"`

---

### 📱 Truy cập hệ thống

Sau khi cài đặt thành công:

| Thông tin | Giá trị |
|-----------|---------|
| **URL** | http://localhost:8069 |
| **Database** | odoo |
| **Admin Email** | admin |
| **Admin Password** | admin |

**Đổi mật khẩu admin:**
1. Đăng nhập với admin
2. Vào **Settings** → **Users**
3. Chọn user **Administrator**
4. Click **Change Password**

---

## 📚 5. Cấu trúc dự án

```
odoo-fitdnu/
├── addons/                              # Custom modules
│   ├── nhan_su/                         # Module Nhân sự
│   │   ├── models/                      # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── employee.py              # Model nhân viên
│   │   │   ├── department.py            # Model phòng ban
│   │   │   ├── contract.py              # Model hợp đồng
│   │   │   ├── attendance.py            # Model chấm công
│   │   │   └── payroll.py               # Model tính lương
│   │   ├── views/                       # UI templates
│   │   │   ├── employee_views.xml
│   │   │   ├── department_views.xml
│   │   │   ├── contract_views.xml
│   │   │   ├── attendance_views.xml
│   │   │   ├── payroll_views.xml
│   │   │   └── menu.xml
│   │   ├── wizard/                      # Wizards
│   │   │   ├── import_employees.py
│   │   │   └── generate_payroll.py
│   │   ├── security/                    # Access rights
│   │   │   └── ir.model.access.csv
│   │   ├── data/                        # Master & demo data
│   │   │   ├── department_data.xml
│   │   │   ├── employee_data.xml
│   │   │   └── demo_data.xml
│   │   ├── reports/                     # Custom reports
│   │   │   ├── payroll_report.py
│   │   │   └── attendance_report.xml
│   │   ├── __init__.py
│   │   └── __manifest__.py              # Module manifest
│   │
│   └── customer_document_management/   # Module Văn bản
│       ├── models/                      # Business logic
│       │   ├── __init__.py
│       │   ├── document.py              # Model tài liệu
│       │   ├── document_type.py         # Model loại tài liệu
│       │   ├── document_category.py     # Model danh mục
│       │   └── document_approval.py     # Model phê duyệt
│       ├── views/                       # UI templates
│       │   ├── document_views.xml
│       │   ├── document_type_views.xml
│       │   ├── document_category_views.xml
│       │   ├── dashboard_views.xml
│       │   └── menu.xml
│       ├── controllers/                 # Controllers
│       │   ├── __init__.py
│       │   ├── predict.py               # AI prediction controller
│       │   └── document_controller.py
│       ├── ml_models/                   # AI models
│       │   ├── model.pkl                # Trained model
│       │   ├── vectorizer.pkl           # TF-IDF vectorizer
│       │   ├── train_classifier.py      # Training script
│       │   └── preprocessing.py         # Data preprocessing
│       ├── data/                        # Master & demo data
│       │   ├── document_type_data.xml
│       │   ├── document_category_data.xml
│       │   └── demo_documents.xml
│       ├── tests/                       # Unit tests
│       │   ├── __init__.py
│       │   ├── test_document.py
│       │   └── test_classifier.py
│       ├── static/                      # Static files
│       │   ├── css/
│       │   └── js/
│       ├── __init__.py
│       └── __manifest__.py              # Module manifest
│
├── odoo/                                # Odoo core
├── docs/                                # Documentation & images
│   ├── README.md
│   ├── INSTALL.md
│   ├── nhan_su.png
│   ├── van_ban.png
│   ├── ai_classify.png
│   └── api_docs.md
├── odoo-bin                             # Odoo executable
├── odoo.conf                            # Configuration
├── docker-compose.yml                   # Docker setup
├── Dockerfile                           # Docker image definition
├── requirements.txt                     # Python dependencies
├── .gitignore
└── README.md                            
```
---

## 📌 6. Liên hệ & Hỗ trợ

Nếu có bất kỳ thắc mắc hoặc cần hỗ trợ, vui lòng liên hệ:

- Họ và tên: Tạ Việt Anh
- Lớp: CNTT16-04
- Khoa: Công nghệ thông tin - Trường Đại học Đại Nam
- Email: tavietanh1012004@gmail.com

© 2025 AIoTLab, Faculty of Information Technology, DaiNam University. All rights reserved.

