## 🚀 Task Manager

[![Actions Status](https://github.com/AlishaEvergreen/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/AlishaEvergreen/python-project-52/actions)
[![Python CI](https://github.com/AlishaEvergreen/python-project-52/actions/workflows/pyci.yml/badge.svg)](https://github.com/AlishaEvergreen/python-project-52/actions/workflows/pyci.yml)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=AlishaEvergreen_python-project-52&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=AlishaEvergreen_python-project-52)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=AlishaEvergreen_python-project-52&metric=coverage)](https://sonarcloud.io/summary/new_code?id=AlishaEvergreen_python-project-52)

**Task Manager** is a production-ready web application for task management with user authentication, status tracking, and label organization. Built with Django following modern development practices.

### Production Build:
[![Live Demo](https://img.shields.io/badge/Live_Demo-Available-blue)](https://python-project-52-2h58.onrender.com)

### Requirements
```
- Python 3.13+
- PostgreSQL 15+
- [uv](https://github.com/astral-sh/uv) package manager
```

### Installation  & Launching
1. Clone the repo:
```bash
git clone https://github.com/AlishaEvergreen/python-project-52.git
cd python-project-52
```
2. Install dependencies:
```bash
make install
```
3. Create `.env` file in the root directory:
```bash
SECRET_KEY=your_secret_key
DEBUG=True  # Set to False in production
DATABASE_URL=postgresql://username:password@localhost:5432/dbname
```
Replace username, password, dbname, and your_secret_key with your own values.

4. Build & Run the application:
```bash
make build
make start
```

The application will be available at: http://localhost:8000

### ❤️ Acknowledgements
Thanks for stopping by, buddy! If you find this tool helpful, don't forget to give it a ⭐ on GitHub!