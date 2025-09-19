## Task Manager

Task Manager – a task management system. It allows you to set tasks, assign performers and change their statuses. You can:
- create tasks, 
- statuses for them and labels,
- appoint executors.

Using the service requires authorization.

### Dependencies

    - asgiref,
    - Django,
    - dotenv,
    - gunicorn,
    - packaging,
    - python-dotenv,
    - sqlparse,
    - typing_extensions,
    - django-bootstrap5,
    - django-filter,
    - flake8,
    - isort,
    - autopep8.

### Installation

Clone the repository:

    git clone https://github.com/0pilione/python-project-52.git
cd python-project-52

Create and activate virtual environment:

    python -m venv .venv
    source .venv/bin/activate

Install the required dependencies using uv: 

    make install

Configure environment variables (create .env file):

    SECRET_KEY=your-secret-key
    DATABASE_URL=sqlite:///db.sqlite3

Apply migrations:

    python manage.py migrate

### Run

    make start

### Hexlet tests and linter status:
[![Actions Status](https://github.com/0pilione/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/0pilione/python-project-52/actions)
[link](https://task-manager-1dz1.onrender.com)