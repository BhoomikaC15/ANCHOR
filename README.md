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
```
/ANCHOR
|__app.py       #Flask application entry point
|__models.py    #Database models
|__venv/        #Virtual Environment
|__README.md
```


## Database Models
```
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
```


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

### Session APIs
| Method | Endpoint                        | Description                             |
|--------|---------------------------------|-----------------------------------------|
| POST   | /sessions                       | Create a new session                    |
| GET    | /sessions                       | Get all categories by user and category |
| GET    | /users/<int:user_id>/sessions   | Get sessions by user                    |
| GET    | /sessions/<int:session_id>      | Get session by ID                       |
| PUT    | /sessions/<int:session_id>      | Update a session details                |
| DELETE | /sessions/<int:session_id>      | Delete a session                        |

### Summary API's
These endpoints provide productivity summaries by comparing a user's focus time across different time ranges. All comparisons are based only on the user's own data.

| Method | Endpoint                      | Description                           |
|--------|-------------------------------|---------------------------------------|
| GET    | /summary/today/<int:user_id>  | Get total focus time for today        |
| GET    | /summary/week/<int:user_id>   | Get total focus time for this week    |
| GET    | /summary/month/<int:user_id>  | Get total focus time for this month   |

### Comparison APIs
These endpoints compare a user's current productivity with their own past performance.
No comparisons with other users are made.

| Method | Endpoint                          | Description                                 |
|-------|-----------------------------------|----------------------------------------------|
| GET   | /compare/<int:user_id>/days       | Compare today vs yesterday focus time        |
| GET   | /compare/<int:user_id>/weeks      | Compare this week vs last week focus time    |
| GET   | /compare/<int:user_id>/months     | Compare this month vs last month focus time  |

### Overview / Stats API

This endpoint provides a high-level overview of a user's productivity data.
It is designed to give a quick snapshot of overall activity without requiring
multiple API calls.

| Method | Endpoint                    | Description                                      |
|--------|-----------------------------|--------------------------------------------------|
| GET    | /overview/<int:user_id>     | Get overall productivity statistics for a user   |



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