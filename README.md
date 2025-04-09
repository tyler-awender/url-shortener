# URL Shortener

A Flask application that lets you convert long URLs into short, links. Built with Python, SQLite, and Flask 

---


## Requirements

- Python 3.8 or higher  
- pip

---

# Setup

---

## 1. Clone the Repository

```bash
git clone https://github.com/your-username/url-shortener.git
cd url-shortener
```

---

## 2. Create a venv

```bash
python -m venv venv
```

---

## 3. Activate the Virtual Environment

- **macOS / Linux:**

```bash
source venv/bin/activate
```

- **Windows (Command Prompt):**

```cmd
venv\Scripts\activate
```

---

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 5. Create a `.env` File

In the root folder of the project, create a file named `.env` and add:

```env
DATABASE_URL=urls.db
```

This tells the app where to store your SQLite database.

---

## 6. Run the App

```bash
python app.py
```

You should see output like:

```
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

---

## 7. Open the App in Your Browser

Go to:  
[http://127.0.0.1:5000](http://127.0.0.1:5000)
