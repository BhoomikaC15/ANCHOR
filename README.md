## ANCHOR
ANCHOR is a work and study tracking web application designed mainly for students and young professionals. It can also be used for any activity that requires focused time tracking.
It helps users log focused work sessions, track time spent across categories, and compare progress against their own past performance instead of unrealistic benchmarks.
The goal is to promote "consistency, accountability, and self-improvement" without shallow gamification for better focus.


## Current Features
User based session tracking
Categorized focus sessions (study, coding, etc.)
Daily, weekly and monthly time comparisons
Progress evaluation based on personal history
Backend built with Flask and SQLAlchemy


## Tech Stack
Backend: Flask(Python)
Database: SQlite
ORM: SQLAlchemy
Environment: Virtual env
Version Control: Git & GitHub


## Project Structure
/ANCHOR
|__app.py       #Flask application entry point
|__models.py    #Database models
|__venv/        #Virtual Environment
|__README.md


## Database Models
USER:
ID
Username
UserEmail
Userpassword
Created_at

CATEGORIES:
ID
User_ID
Name

SESSIONS:
ID
User_ID
Category_ID
duration_min
date


## APIs
### User APIs
| Method | Endpoint               | Description              |
|--------|------------------------|--------------------------|
| POST   | /users                 | Create a new user        |
| GET    | /users                 | Get all users            |
| GET    | /users/<int:user_id>   | Get user by ID           |
| PUT    | /users/<int:user_id>   | Update user details      |
| DELETE | /users/<int:user_id>   | Delete a user            |

### Category APIs
| Method | Endpoint                        | Description                  |
|--------|---------------------------------|------------------------------|
| POST   | /categories                     | Create a new category        |
| GET    | /users/<int:user_id>/categories | Get all categories by user   |
| GET    | /categories/<int:category_id>   | Get category by ID           |
| PUT    | /categories/<int:category_id>   | Update category details      |
| DELETE | /categories/<int:category_id>   | Delete a category            |


## Setup Instructions
1. Clone the repository:
git clone <repository-url>
cd ANCHOR
2. Create and activate a virtual environment:
python -m venv venv
venv\Scripts\activate           #Windows
3. Install dependencies:
pip install flask flask-sqlalchemy
4. Initialize the database (one-time):
python init_db.py
5. Run the Flask app:
python app.py


## Project Status
In active development
Current Focus: Backend
Frontend and authentication will be added in later stages.


## Need of ANCHOR
Many productivity apps compare users against others, which can be discouraging.
The app never compares you to others.
It only compares you to yourself.


## Author
Bhoomika Choudhury
Computer Science undergraduate (2nd year)