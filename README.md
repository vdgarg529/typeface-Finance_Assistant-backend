 

# Personal Finance Assistant API

A FastAPI-based backend service for managing personal finances, including transaction tracking, receipt scanning, and financial insights.

## Features
- **User Authentication**: JWT-based secure user registration and login
- **Transaction Management**: Create and manage income/expense transactions
- **Receipt Processing**: Upload and extract data from receipt images using OCR
- **PDF Statement Processing**: Parse transaction data from bank statement PDFs
- **Financial Analytics**: Generate category and date-based spending summaries
- **RESTful API**: Clean API design with proper HTTP status codes and error handling

## Technology Stack
- **Backend Framework**: FastAPI
- **Database**: SQLite (with SQLAlchemy ORM)
- **Authentication**: JWT tokens
- **File Processing**: pytesseract (OCR), pdfplumber (PDF extraction)
- **Containerization**: Docker
- **Deployment**: Render

### [Detailed Tesseract OCR Installation Guide](#detailed-tesseract-ocr-installation-guide)


# Local Development Setup

## 1. Clone the Repository
```bash
git clone https://github.com/vdgarg529/typeface-Finance_Assistant-backend.git
cd typeface-Finance_Assistant-backend
```

## 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

## 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## 4. Environment Configuration
Create a `.env` file in the root directory:

```env
DATABASE_URL=sqlite:///./finance_assistant.db
SECRET_KEY=your-asdfghjkl;
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

## 5. Initialize Database
```bash
# This will create the SQLite database with all tables
python -c "
from app.db.base import Base
from app.db.session import engine
Base.metadata.create_all(bind=engine)
print('Database initialized successfully')
"
```

## 6. Run the Application
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
The API will be available at [http://localhost:8000](http://localhost:8000)

# Docker Setup

## 1. Build and Run with Docker Compose
```bash
docker-compose up --build
```

## 2. Access the Application
The API will be available at [http://localhost:8000](http://localhost:8000)

## API Documentation
Once the application is running, access the interactive API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Environment Variables
| Variable                  | Description                | Default                                       |
|---------------------------|----------------------------|-----------------------------------------------|
| DATABASE_URL               | Database connection string | sqlite:///./finance_assistant.db              |
| SECRET_KEY                 | JWT secret key             | asdfghjkl;                                    |
| ALGORITHM                  | JWT algorithm              | HS256                                         |
| ACCESS_TOKEN_EXPIRE_MINUTES | Token expiration time      | 30                                            |
| ALLOWED_ORIGINS            | CORS allowed origins       | http://localhost:3000,http://localhost:8000    |

## API Usage Examples

### Health Check
```bash
curl -X GET http://localhost:8000/health
```

### Authentication
```bash
# Register a user
curl -X POST http://localhost:8000/auth/register   -H "Content-Type: application/json"   -d '{"username":"testuser","password":"testpass"}'

# Login and get token
curl -X POST http://localhost:8000/auth/login   -H "Content-Type: application/x-www-form-urlencoded"   -d "username=testuser&password=testpass"
```

### Transactions
```bash
# Create a transaction (replace YOUR_JWT_TOKEN_HERE)
curl -X POST http://localhost:8000/transactions/   -H "Content-Type: application/json"   -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"   -d '{"amount": 250, "type": "expense", "category": "Food", "date": "2024-02-01"}'

# Get transactions with filters
curl -X GET "http://localhost:8000/transactions/?start_date=2024-01-01&end_date=2024-02-28&page=1&limit=10"   -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"

# Get category summary
curl -X GET "http://localhost:8000/transactions/summary/category?start_date=2024-01-01&end_date=2024-02-28"   -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```

### Receipts
```bash
# Upload a receipt image
curl -X POST http://localhost:8000/receipts/upload   -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"   -F "file=@/path/to/receipt.jpg"

# Upload a PDF statement
curl -X POST http://localhost:8000/receipts/upload-pdf   -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"   -F "file=@/path/to/statement.pdf"
```

## Project Structure
```
finance_assistant/
├── app/
│   ├── core/           # Configuration and security utilities
│   ├── models/         # SQLAlchemy database models
│   ├── schemas/        # Pydantic models for request/response
│   ├── routers/        # API route handlers
│   ├── services/       # Business logic
│   ├── utils/          # OCR and PDF parsing utilities
│   └── db/            # Database session management
├── tests/              # Test cases
├── Dockerfile          # Container configuration
├── docker-compose.yml  # Multi-container setup
├── render.yaml         # Render deployment configuration
└── requirements.txt    # Python dependencies
```



# Detailed Tesseract OCR Installation Guide

## Windows Installation

### Method 1: Using Installer (Recommended)
**Download the installer:**
- Go to the [UB Mannheim Tesseract page](https://github.com/UB-Mannheim/tesseract/wiki)
- Download the Windows installer for the latest version (e.g., `tesseract-ocr-w64-setup-5.3.3.20231005.exe`)

**Run the installer:**
- Double-click the downloaded file
- Follow the installation wizard
- Note the installation directory (typically `C:\Program Files\Tesseract-OCR\`)
- Make sure to check "Additional language data" during installation

**Add to System PATH:**
- Press **Win + R**, type `sysdm.cpl`, and press Enter
- Click on "Environment Variables"
- Under "System variables", find and select the "Path" variable, then click "Edit"
- Click "New" and add:
  - `C:\Program Files\Tesseract-OCR\`
  - `C:\Program Files\Tesseract-OCR\tessdata`

**Verify installation:**
```cmd
tesseract --version
```

### Method 2: Using Chocolatey (Package Manager)
**Install Chocolatey (if not already installed):**
```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

**Install Tesseract:**
```powershell
choco install tesseract
choco install tesseract-languages
```

**Verify installation:**
```powershell
tesseract --version
```

---

## macOS Installation

### Method 1: Using Homebrew (Recommended)
**Install Homebrew (if not already installed):**
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**Install Tesseract:**
```bash
brew install tesseract
brew install tesseract-lang
```

**Verify installation:**
```bash
tesseract --version
```

### Method 2: Using MacPorts
**Install MacPorts (if not already installed):**
- Download from [macports.org](https://www.macports.org/install.php)

**Install Tesseract:**
```bash
sudo port install tesseract
sudo port install tesseract-eng
```

---

## Linux Installation (Ubuntu/Debian)

### Method 1: Using apt (Recommended)
**Update package list:**
```bash
sudo apt update
```

**Install Tesseract:**
```bash
sudo apt install tesseract-ocr
```

**Install language packs:**
```bash
sudo apt install tesseract-ocr-eng  # English
sudo apt install tesseract-ocr-all  # All languages
sudo apt install tesseract-ocr-fra  # French
sudo apt install tesseract-ocr-deu  # German
sudo apt install tesseract-ocr-spa  # Spanish
```

**Verify installation:**
```bash
tesseract --version
```

### Method 2: Compiling from Source
**Install dependencies:**
```bash
sudo apt update
sudo apt install autoconf automake libtool pkg-config libpng-dev libjpeg-dev libtiff-dev zlib1g-dev libicu-dev libpango1.0-dev libcairo2-dev
```

**Download and compile Tesseract:**
```bash
git clone https://github.com/tesseract-ocr/tesseract.git
cd tesseract
./autogen.sh
./configure
make
sudo make install
sudo ldconfig
```

**Download language data:**
```bash
wget https://github.com/tesseract-ocr/tessdata/raw/main/eng.traineddata
sudo mv eng.traineddata /usr/local/share/tessdata/
```

---

## Configuring Tesseract for the Finance Assistant

**Install Python bindings:**
```bash
pip install pytesseract pillow
```

**Update the OCR parser configuration:**
```python
# For Windows (if Tesseract is installed in a non-standard location)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# For Linux/macOS (usually in PATH, so this line can be commented out)
# pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
```

**Test the installation:**
```python
import pytesseract
from PIL import Image, ImageDraw, ImageFont
import os

# Test Tesseract installation
print("Tesseract version:", pytesseract.get_tesseract_version())

# Create a test image
img = Image.new('RGB', (200, 50), color='white')
d = ImageDraw.Draw(img)
d.text((10, 10), "Test 123", fill='black')
img.save('test.png')

# Extract text
text = pytesseract.image_to_string(Image.open('test.png'))
print("Extracted text:", text)

# Clean up
os.remove('test.png')
```
