# Pair Programming Backend

This repository contains the backend for the Pair Programming project, built with **FastAPI** and Python.  
Follow the instructions below to set up the project locally.

---

## 🚀 Installation & Setup

### **1. Clone the Repository**
```bash
git clone https://github.com/hizinberg/pair-programming-backend/
cd pair-programming-backend
```

---

## 🐍 Virtual Environment Setup

### **2. Create a Virtual Environment**
```bash
python -m venv pair-programming-venv
```

### **3. Activate the Virtual Environment**

#### **Windows**
```bash
pair-programming-venv\Scripts\activate
```

#### **macOS / Linux**
```bash
source pair-programming-venv/bin/activate
```

---

## 📦 Install Dependencies

### **4. Install Required Packages**
```bash
pip install -r requirements.txt
```

---

## ▶️ Run the FastAPI Server

### **5. Start the Development Server**

Run this command **inside the backend directory**:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The server will start on:

👉 **http://localhost:8000**

You can view the interactive API docs at:

- **Swagger UI:** http://localhost:8000/docs  

---

## 📁 Project Structure
```
pair-programming-backend/
│── app/
│   ├── __init__.py
│   ├── routers/
│   ├── services/
│   ├── db.py
│   ├── logger.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
│── requirements.txt
└── README.md
```
