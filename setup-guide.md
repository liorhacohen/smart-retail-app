# 🏪 Inventory Management System

מערכת ניהול מלאי מקצועית עם React frontend ו-Flask backend.

## 🚀 3 דרכי הפעלה

### 🌟 אפשרות 1: מקומי עם React Frontend (מומלץ לפיתוח)
ממשק משתמש מלא + שליטה מלאה

### 🐳 אפשרות 2: Docker Compose (מומלץ לבדיקה מהירה) 
הפעלה מהירה בכמה קליקים

### ☸️ אפשרות 3: Kubernetes (לפרודקשן ולמידה)
deployment מתקדם עם high availability

---

## 🌟 אפשרות 1: הפעלה מקומית (מומלץ)

### דרישות
```bash
python3 --version    # 3.8+
node --version       # 16+
psql --version       # 13+
```

### 5 צעדים מהירים
```bash
# 1. הורדה
git clone https://github.com/YOUR_USERNAME/inventory-system.git
cd inventory-system

# 2. דאטאבייס
psql postgres -c "CREATE USER inventory_user WITH PASSWORD 'inventory_pass';"
psql postgres -c "CREATE DATABASE inventory_db OWNER inventory_user;"

# 3. Backend
pip3 install -r requirements.txt flask-cors python-dotenv psycopg2-binary
echo "DB_HOST=localhost\nDB_PORT=5432\nDB_NAME=inventory_db\nDB_USER=inventory_user\nDB_PASSWORD=inventory_pass" > .env
psql -U inventory_user -d inventory_db -f init.sql
python3 app.py &

# 4. Frontend (טרמינל חדש)
cd frontend && npm install && npm start &

# 5. נתונים לדוגמה
python3 load_sample_data.py
```

**✅ מוכן:** http://localhost:3000 (Dashboard) | http://localhost:5000 (API)

---

## 🐳 אפשרות 2: Docker Compose

### התקנה מהירה
```bash
# בדוק Docker
docker --version

# הפעלה
git clone https://github.com/YOUR_USERNAME/inventory-system.git
cd inventory-system
docker-compose up --build

# בדיקה
curl http://localhost:5000/api/health
```

**✅ מוכן:** http://localhost:5000

### פקודות שימושיות
```bash
docker-compose down        # עצירה
docker-compose logs -f     # לוגים
docker-compose down -v     # מחיקה מלאה
```

---

## ☸️ אפשרות 3: Kubernetes

### התקנה
```bash
# macOS
brew install docker minikube kubectl

# Ubuntu
sudo apt install docker.io kubectl
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

### פריסה
```bash
git clone https://github.com/YOUR_USERNAME/inventory-system.git
cd inventory-system

# הכנת cluster
minikube start
minikube addons enable ingress

# פריסה
cd k8s
kubectl apply -f configs/ secrets/ deployments/ services/ ingress/

# גישה חיצונית (טרמינל נפרד)
minikube tunnel

# בדיקה
curl http://localhost/api/health
```

**✅ מוכן:** http://localhost

### ניהול
```bash
kubectl get pods              # מצב המערכת
kubectl logs -f deployment/flask-deployment  # לוגים
kubectl delete -f k8s/        # מחיקה
minikube delete && minikube start  # איפוס מלא
```

---

## 🎮 מה אפשר לעשות?

### עם React Frontend (אפשרות 1)
- 📊 **Dashboard:** סטטיסטיקות בזמן אמת
- 📦 **Products:** רשימה + חיפוש + פילטרים
- ➕ **Add Product:** טופס הוספה
- 🔄 **Restock:** תוספת מלאי
- 📈 **Analytics:** גרפים וחזותיים
- ⚠️ **Alerts:** התרעות מלאי נמוך

### עם API בלבד (אפשרויות 2-3)
```bash
# יצירת מוצר
curl -X POST http://localhost:5000/api/products \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop", "sku": "LAP001", "stock_level": 15, "price": 999.99}'

# צפייה במוצרים
curl http://localhost:5000/api/products

# analytics
curl http://localhost:5000/api/products/analytics

# מלאי נמוך
curl http://localhost:5000/api/products/low-stock

# תוספת מלאי
curl -X POST http://localhost:5000/api/products/1/restock \
  -H "Content-Type: application/json" \
  -d '{"quantity": 50, "notes": "Weekly restock"}'
```

---

## 🚨 פתרון בעיות מהיר

### אפשרות 1 (מקומי)
```bash
# Backend לא מתחיל
psql -U inventory_user -d inventory_db -c "SELECT 1;"
pip3 install flask-cors python-dotenv psycopg2-binary

# Frontend לא מתחיל  
rm -rf frontend/node_modules && cd frontend && npm install

# אין נתונים
python3 load_sample_data.py
```

### אפשרות 2 (Docker)
```bash
# Port תפוס
docker-compose down && lsof -i :5000

# בעיות memory
docker system prune -a && docker-compose up --build
```

### אפשרות 3 (Kubernetes)
```bash
# Pods לא עולים
kubectl get pods && kubectl describe pod <pod-name>

# לא מצליח לגשת
minikube tunnel  # ברקע

# איפוס מלא
minikube delete && minikube start
```

---

## 📊 מה כלול במערכת?

### Backend (Flask + PostgreSQL)
- ✅ REST API מלא
- ✅ Analytics endpoints  
- ✅ Low stock alerts
- ✅ Restock tracking
- ✅ CORS support

### Frontend (React) - רק באפשרות 1
- ✅ Modern dashboard
- ✅ Responsive design
- ✅ Interactive charts
- ✅ Real-time updates
- ✅ Search & filtering

### Infrastructure
- ✅ Docker containerization
- ✅ Kubernetes manifests
- ✅ Sample data loader
- ✅ Health monitoring

---

## 🎯 איזה אפשרות לבחור?

| צורך | אפשרות מומלצת |
|------|---------------|
| 👨‍💻 **פיתוח ועריכה** | 1️⃣ מקומי |
| 🧪 **בדיקה מהירה** | 2️⃣ Docker |
| 🚀 **למידת Kubernetes** | 3️⃣ Kubernetes |
| 🌐 **פרודקשן** | 3️⃣ Kubernetes |
| 🎨 **ממשק משתמש** | 1️⃣ מקומי |

---

**🎉 בחר אפשרות והתחל! כל האפשרויות כוללות נתונים לדוגמה ותיעוד מלא.**
