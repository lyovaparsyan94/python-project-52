### Hexlet tests and linter status:
[![Actions Status](https://github.com/MrMAx-26/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/MrMAx-26/python-project-52/actions)
[![Continuous Integration](https://github.com/MrMAx-26/python-project-52/actions/workflows/ci.yml/badge.svg)](https://github.com/MrMAx-26/python-project-52/actions/workflows/ci.yml)
[![Maintainability](https://qlty.sh/gh/MrMAx-26/projects/python-project-52/maintainability.svg)](https://qlty.sh/gh/MrMAx-26/projects/python-project-52)
### Coverage
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=MrMAx-26_python-project-52&metric=coverage)](https://sonarcloud.io/summary/new_code?id=MrMAx-26_python-project-52)


# Task Manager
A modern, robust task management system built with Django and Python. This application provides a comprehensive solution for organizing, tracking, and managing tasks in a collaborative environment. The system implements user authentication, role-based access control, and flexible task organization using statuses and labels.

## Project Features

### User Management
- **Secure Authentication**: Complete user registration, login, and logout functionality
- **Profile Management**: Users can update their profile information
- **User Protection**: Users associated with tasks cannot be deleted, preventing data integrity issues
- **Access Control**: Role-based permissions ensure users can only modify their own information

### Task Management
- **Comprehensive Task Details**: Tasks include name, description, status, assignee, and labels
- **Task Ownership**: Each task has an owner who created it and an executor who is assigned to it
- **Advanced Filtering**: Filter tasks by status, executor, label, or by tasks created by the current user
- **CRUD Operations**: Create, view, update, and delete tasks with appropriate permissions

### Status Management
- **Custom Workflow States**: Create and manage task statuses to reflect your workflow needs
- **Status Protection**: Statuses in use by tasks cannot be deleted, maintaining data integrity
- **Status Tracking**: Each status tracks creation and update timestamps

### Label Management
- **Flexible Categorization**: Organize tasks with custom labels
- **Multiple Labels**: Assign multiple labels to each task for precise organization
- **Label Protection**: Labels used by tasks cannot be deleted, preserving task categorization

### Internationalization
- **Multilingual Support**: Interface available in multiple languages
- **Localized Content**: Date formats and messages adapt to the user's locale

## Technology Stack

### Backend
- **Python 3.10+**: Modern Python version with enhanced features
- **Django 5.2**: Latest stable Django framework for robust web development
- **Django ORM**: Sophisticated object-relational mapping for database interactions
- **PostgreSQL**: Production-grade relational database for data reliability
- **SQLite**: Lightweight database for development and testing

### Frontend
- **HTML5**: Modern markup language for web content
- **Bootstrap 5**: Responsive design framework with modern UI components
- **Django Templates**: Server-side rendering with Django's template engine

### Security
- **Authentication System**: Django's built-in authentication system with custom user model
- **Permission Checks**: Custom mixins ensuring proper access control
- **CSRF Protection**: Cross-Site Request Forgery protection
- **Environment Variables**: Secure configuration using environment variables
- **Password Hashing**: Secure password storage with Django's authentication system

### Testing
- **Django Test Framework**: Comprehensive testing tools for Django applications
- **Pytest**: Advanced testing framework for Python
- **Coverage Reports**: Test coverage analysis to ensure code quality

### CI/CD
- **GitHub Actions**: Automated testing, linting, and deployment workflows
- **SonarQube Integration**: Code quality and security analysis

### Monitoring & Error Tracking
- **Rollbar**: Real-time error tracking and monitoring

### Development Tools
- **Makefile**: Project automation for common tasks
- **UV**: Modern dependency management for Python
- **Ruff**: Code linting to maintain code quality
- **Whitenoise**: Static file serving for production
- **Gunicorn**: Production-ready WSGI server

## Production Deployment

### Prerequisites
- Python 3.10 or higher
- PostgreSQL database server
- Gunicorn WSGI server
- Environment variables properly configured

### Deployment Steps
1. Clone the repository
2. Install dependencies with `make build`
3. Configure environment variables
4. Run database migrations with `make migrate`
5. Collect static files with `make collectstatic`
6. Start the server with `make render-start` (production) or `make run` (development)

### Environment Variables
The application requires the following environment variables:

```
# Django settings
SECRET_KEY=yoursecretkeyhere
DEBUG=True  # Set to False in production
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com

# Rollbar settings (optional)
ROLLBAR_ACCESS_TOKEN=youraccesstokenhere

# Database settings (for PostgreSQL)
DATABASE_URL=postgres://user:password@localhost:5432/dbname
```

## Development Setup

### Local Setup

1. Clone the repository
```bash
git clone https://github.com/MrMAx-26/python-project-52.git
cd python-project-52
```

2. Install dependencies
```bash
make build
```

3. Create `.env` file with required environment variables (see above)

4. Apply migrations and start the development server
```bash
make migrate
make run
```