# Django Project Setup Guide

A comprehensive guide to setting up and running the Django project locally.

---

## Prerequisites

Ensure the following are installed on your system:

- **Python 3.8+** (recommended)
  - Verify with: `python --version` or `python3 --version`
- **Git** (for version control)
- **Python Virtual Environment** (`venv` module included with Python 3)

---

## Project Setup

### 1. Clone the Repository

Clone the project to your local machine:

```bash
git clone <URL_DEL_REPOSITORIO>
```

### 2. Virtual Environment Setup

Create and activate a virtual environment to isolate project dependencies.

```bash
python -m venv venv
```

#### Activate the Virtual Environment
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```
Your terminal prompt should now show (venv) to indicate the active environment.

### 3. Install Dependencies
Install all required packages from **requirements.txt**:

```bash
pip install -r requirements.txt
```

### 4. Database Configuration

Generate and apply database migrations:

```bash	
# Create migration files
python manage.py makemigrations

# Apply migrations to the database
python manage.py migrate
```
This sets up the database schema using Django's migration system. By default, Django uses SQLite.

---

## Useful Commands

### Run the Development Server

```bash
python manage.py runserver
```
- Access the site at http://localhost:8000

- To stop the server, press `Ctrl + C`
