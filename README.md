# Library-Management-System

## Features
1. CRUD operations for books and members.
2. Search functionality for books.
3. Pagination.
4. Token-based authentication for user sessions.
5. Role-based permissions (admin and user).

## How to Run
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/library-management.git
   cd library-management
Install Python dependencies:
```bash
pip install -r requirements.txt

Run the application:
```bash
Copy code
python app.py
# Design Choices
Blueprints: Modularized routes for scalability.
SQLite: Lightweight database for easy setup.
Session-based auth: Simple token-free user management.
# Assumptions and Limitations
Only admins can manage books.
Users can only modify their profiles.
No advanced password recovery system implemented.
