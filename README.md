﻿# **TaskMate API**

**TaskMate** is a simple and efficient To-Do list management API that enables users to create, manage, and track their tasks. Designed for personal productivity, TaskMate includes user authentication, task prioritization, due dates, reminders, and much more.

## **Features**
- **User Management**: Register and authenticate users with JWT tokens.
- **Task Management**: Create, update, delete, and manage tasks.
- **Task Expiration**: Automatically mark tasks as expired if the due date passes.
- **Due Dates**: Assign and track due dates for tasks.

## **Tech Stack**
- **FastAPI**: Modern Python web framework for building APIs.
- **PostgreSQL**: Reliable and scalable relational database.
- **SQLAlchemy**: ORM for interacting with the database.
- **Alembic**: Database migration tool for managing schema changes.
- **Pydantic**: Data validation and parsing using Python type hints.
- **python-jose** Encode and decode JSON Web Tokens (JWT).


6. **Access the API:**
   The API will be accessible at `https://flasktaskmate.onrender.com`.

7. **API Documentation:**
   Explore the interactive API documentation at `https://flasktaskmate.onrender.com/docs`.

## **Endpoints**

### **User Management**
- `POST /users/registration` - Register a new user.
- `POST /users/login` - Log in a user and generate a JWT token.
- `GET /users/me` - Fetch the current authenticated user.

### **Task Management**
- `POST /tasks/` - Create a new task.
- `GET /tasks/` - Get a list of tasks with pagination.
- `GET /tasks/id` - Retrieve task details by ID.
- `PATCH /tasks/id/edit` - Edit a task (title, description, etc.).
- `PATCH /tasks/id/edit/status` - Update task status (pending, in-progress, completed).
- `PATCH /tasks/id/edit/due_date` - Update task due date.
- `DELETE /tasks/id/delete` - Delete a task.

### **Health Check**
- `GET /health` - Check the database connection.


## **Future Improvements**
- **Task Prioritization**: Set task priorities (low, medium, high).
- **Reminders**: Configure reminders to help users meet deadlines.
- **Search and Filter**: Search and filter tasks by status, priority, or due date.
- **Notifications**: Add WebSocket-based real-time task expiration notifications.
- **Task Assignment**: Enable tasks to be shared between multiple users.

---

