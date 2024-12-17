# Micro Blog

A simple Flask-based blog application that allows administrators to create, edit, and manage blog articles. The application provides a clean interface for readers to view articles while maintaining a secure admin dashboard for content management.  

This is one of the exercises at roadmap.sh   
[Link to the project](https://roadmap.sh/projects/personal-blog)

## Features

- Public-facing blog interface for readers
- Secure admin dashboard
- Article management (Create, Read, Update, Delete)
- JSON-based article storage
- Secure authentication system
- Responsive datetime handling

## Prerequisites

- Python 3.x
- Flask
- Werkzeug

## Installation

1. Clone the repository to your local machine:
```bash
git clone <repository-url>
cd microblog
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install the required dependencies:
```bash
pip install flask werkzeug
```

4. Create the necessary directories and files:
```bash
mkdir articles
touch admin.json
```

5. Set up the admin credentials by creating an `admin.json` file with the following structure:
```json
{
    "username": "your_username",
    "password": "your_hashed_password"
}
```

## Project Structure

```
microblog/
├── app.py
├── helpers.py
├── articles/
│   └── article{n}.json
├── templates/
│   ├── admin.html
│   ├── article.html
│   ├── edit.html
│   ├── error.html
│   ├── home.html
│   ├── login.html
│   └── new.html
├── admin.json
└── README.md
```

## Usage

1. Start the application:
```bash
python app.py
```

2. Access the application:
- Home page: `http://localhost:5000`
- Admin login: `http://localhost:5000/login`
- Admin dashboard: `http://localhost:5000/admin` (requires authentication)

## Article Management

### Article Structure
Articles are stored as JSON files with the following structure:
```json
{
    "id": 1,
    "title": "Article Title",
    "date": "17/Dec/2024",
    "content": "Article content goes here"
}
```

### Admin Features
- Create new articles
- Edit existing articles
- Delete articles
- View all articles in the admin dashboard

## Security Features

- Password hashing using Werkzeug's security functions
- Session-based authentication
- Login required decorator for protected routes
- Secure password storage

## Routes

- `/`: Home page displaying all articles
- `/article/<id>`: Display specific article
- `/admin`: Admin dashboard (protected)
- `/new`: Create new article (protected)
- `/edit/<id>`: Edit existing article (protected)
- `/delete/<id>`: Delete article (protected)
- `/login`: Admin login
- `/logout`: Logout current admin session

## Error Handling

The application includes basic error handling for:
- Invalid login credentials
- Missing articles
- Corrupted JSON files
- Missing required form fields