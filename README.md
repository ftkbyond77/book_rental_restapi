# 📚 Rental Book Store – Django Web Application

## 📝 Abstract

The **Rental Book Store** is a web-based platform developed using the Django framework to streamline the process of renting books online. This application is designed to simulate a modern library or rental shop environment, where users can browse books, make rental transactions, and track their activity over time. The project was built with both user experience and administrative efficiency in mind, making it suitable for small-scale libraries, student projects, or as a prototype for a scalable SaaS rental service.

## 🎯 Objective

The primary goal of this project is to provide a functional and user-friendly interface for managing book rentals. It focuses on:

- Enabling users to search, view, and rent books conveniently.
- Allowing administrators to manage inventory and track rental records.
- Demonstrating Django’s capabilities in handling user authentication, form handling, and database interactions.

## 🛠️ Technology Stack

- **Framework**: Django (Python)
- **Database**: SQLite (default) or PostgreSQL (recommended for production)
- **Frontend**: Django Templates + Bootstrap (or customize as needed)
- **Authentication**: Django's built-in authentication system

## 🚀 Key Features

- 👥 User registration and login system
- 📚 Book browsing with detail views
- 🛒 Rent/return functionality
- 📆 Rental history and due dates
- 🛠️ Admin panel with full CRUD operations
- 📊 Dashboard for monitoring rentals and availability

## 🧪 Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/rental_book_store.git
   cd rental_book_store
   ```
2. **Create and activate a virtual environment**:
    ```bash 
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4. **Apply database migrations**:
    ```bash
    python manage.py migrate
    ```
5. **Create a superuser**:
    ```bash
    python manage.py createsuperuser
    ```
6. **Run the development server**:
    ```bash
    python manage.py runserver
    ```
7. **Access the app in your web browser**:
    ```bash
    http://127.0.0.1:8000
    ```

