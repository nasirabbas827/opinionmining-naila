# Opinionmining_naila  

A lightweight Django web‑application for mining and visualising opinions (sentiment analysis) from user‑generated comments. The project demonstrates end‑to‑end data collection, preprocessing, model inference and a simple dashboard for exploring results.

---

## Overview  

The application lets users submit comments, automatically classifies each comment as **positive**, **negative**, or **neutral**, and stores the results in a SQLite database. An admin interface provides basic CRUD operations, while a public dashboard displays aggregated sentiment statistics.

Key components:

| File / Directory | Purpose |
|------------------|---------|
| `manage.py` | Django management script |
| `myapp/` | Core Django app (models, views, forms, templates) |
| `myapp/templates/` | HTML templates for the UI |
| `myapp/migrations/` | Database schema migrations |
| `Opinion‑Final ( Naila & Misha ).rar` | Dataset & model artefacts used for training |
| `Project File.docx` | Project specification and design notes |

---

## Features  

- **Comment submission** – simple form with validation.  
- **Automatic sentiment classification** – uses a pre‑trained model (included in the archive).  
- **Dashboard** – visual summary of sentiment distribution (counts & percentages).  
- **Admin panel** – Django admin for managing comments and user profiles.  
- **User authentication** – login/logout flow with basic session handling.  

---

## Tech Stack  

| Layer | Technology |
|-------|------------|
| Backend | Python 3.9, Django 4.x |
| Database | SQLite (default) |
| Front‑end | HTML5, CSS (Bootstrap optional) |
| NLP Model | Scikit‑learn / NLTK (model files bundled in the `.rar`) |
| Deployment | Run locally with `runserver`; can be containerised with Docker (not included) |

---

## Installation  

```bash
# 1. Clone the repository
git clone https://github.com/your-username/Opinionmining_naila.git
cd Opinionmining_naila

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt   # If requirements.txt is missing, install Django manually:
pip install Django==4.*  # plus any additional packages you need (e.g., scikit-learn, nltk)

# 4. Extract the model/data archive
unzip "Opinion-Final( Naila & Misha ).rar" -d data   # adjust path as needed

# 5. Apply migrations
python manage.py migrate
```

> **Note:** If you encounter missing packages, add them to `requirements.txt` and re‑run the install step.

---

## Usage  

```bash
# Start the development server
python manage.py runserver
```

1. Open a browser and navigate to `http://127.0.0.1:8000/`.  
2. Register / log in to submit a comment.  
3. After submission, the comment is classified and stored.  
4. Visit `/dashboard/` to see the sentiment overview.  
5. Access the admin interface at `/admin/` (create a superuser with `python manage.py createsuperuser`).

---

## License  

This project is licensed under the **MIT License** – see the `LICENSE` file for details.  

---  

*Happy mining!*