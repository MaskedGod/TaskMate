# **TaskMate API**

**TaskMate** is a simple and efficient To-Do list management API that allows users to create, manage, and track their tasks with ease. Designed for personal productivity, TaskMate includes user authentication, task prioritization, due dates, reminders, and more.

## **Features**
- **User Management**: Create and manage users with authentication.
- **Task Management**: Create, update, delete, and organize tasks.
- **Prioritization**: Set task priorities (low, medium, high).
- **Due Dates**: Track tasks by due dates and retrieve overdue tasks.
- **Reminders**: Set reminders to keep up with deadlines.
- **Search and Filters**: Search tasks and filter by status, priority, or due date.

## **Endpoints**
- `GET /` - API information
### **User Authentication**
- `POST /users/registration` - Register a new user.
- `POST /users/login` - Log in a user and generate a JWT token.


## **Tech Stack**
- **FastAPI** for the backend framework.
- **PostgreSQL** for database management.
- **Alembic** for database migrations.
- **Pydantic** for data validation.
- **FastAPIUsers** registration and authentication system.
