# Calorie Tracker 🍎🔥

Calorie Tracker is a **Django-based web application** deployed on **AWS Elastic Beanstalk**. It allows users to track their daily calorie intake and manage a healthy lifestyle while showcasing a **full DevOps pipeline** with deployment automation and backups.

---

## 🚀 Features

* 👤 **User Management** – Register, login, and manage profiles.
* 🍽 **Food & Calorie Logging** – Add, update, and delete food items with calorie counts.
* 📊 **Dashboard** – Visualize total calorie intake and history.
* 💾 **Database Backup** – Supports SQL and JSON backup files.
* ☁️ **Cloud Deployment** – Automated deployment on **AWS Elastic Beanstalk**.
* 🛠 **DevOps Ready** – Includes EB config, Procfile, and scripts for CI/CD.

---

## 🛠 Tech Stack

* **Framework**: Django (Python)
* **Frontend**: HTML, CSS, Bootstrap
* **Database**: SQLite (dev), PostgreSQL (production)
* **Deployment**: AWS Elastic Beanstalk
* **Version Control**: Git & GitHub

---

## 📂 Project Structure

```
calorietracker/
│── calorie_tracker/         # Django app code
│── templates/               # HTML templates
│── static/                  # CSS, JS, Images
│── db.sqlite3               # Local database (ignored in prod)
│── Procfile                 # For AWS deployment
│── fix_ebs.sh               # EB configuration fix script
│── requirements.txt         # Python dependencies
│── backup.sql               # SQL backup
│── backup.json              # JSON backup
│── .elasticbeanstalk/       # AWS EB configs
│── .ebextensions/           # EB extensions configs
└── README.md                # Documentation
```

---

## ⚡ Getting Started

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/adithyanaren/calorietracker.git
cd calorietracker
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate   # Mac/Linux
.venv\Scripts\activate      # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run Migrations

```bash
python manage.py migrate
```

### 5️⃣ Start Development Server

```bash
python manage.py runserver
```

Visit 👉 `http://127.0.0.1:8000`

---

## 🌍 Deployment (AWS Elastic Beanstalk)

1. Initialize EB:

```bash
eb init
```

2. Create environment:

```bash
eb create calorietracker-env
```

3. Deploy:

```bash
eb deploy
```

The app will be available at your EB environment URL.

---

## ✅ Backup & Restore

* **Export SQL backup**:

```bash
python manage.py dumpdata > backup.json
```

* **Restore SQL backup**:

```bash
python manage.py loaddata backup.json
```

---

## 📸 Screenshots

*Add screenshots here:*

* 📊 Dashboard view
* 🍽 Add food entry form
* 🔐 Login & Registration page
* ☁️ AWS EB Deployment console

---

## 🤝 Contribution

1. Fork the repo
2. Create feature branch (`git checkout -b feature-name`)
3. Commit changes (`git commit -m "Added feature"`)
4. Push branch (`git push origin feature-name`)
5. Open Pull Request

---

## 📜 License

This project is licensed under the **MIT License**.

---

## 👨‍💻 Author

* **Adithya Naren**
  🌐 [LinkedIn](https://www.linkedin.com/in/adhithya0616/) | 💻 [GitHub](https://github.com/adithyanaren)

---

✨ *Calorie Tracker – Track your health, powered by Django & AWS.*
