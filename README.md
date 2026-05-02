# ProjectManager - Django Task & Project Management Application

A full-featured Django web application for managing projects and tasks with team collaboration, role-based access control, and both REST API and template-based web interfaces.

## 🎯 Features

### Authentication & User Management

- **Email-based Authentication**: Custom user model using email instead of username
- **Session-based Login**: Secure login/logout with Django sessions
- **JWT Token Support**: REST API endpoints with JWT authentication (1-hour access, 7-day refresh tokens)
- **User Registration**: Self-registration with email and password validation

### Project Management

- **Create & Manage Projects**: Create new projects with descriptions
- **Team Collaboration**: Add team members to projects with role assignment
- **Role-Based Permissions**: Two-tier permission system (Admin/Member)
  - **Admin**: Can create tasks, manage team members, edit/delete tasks
  - **Member**: Can view tasks and update only tasks assigned to them

### Task Management

- **Task CRUD Operations**: Create, read, update, and delete tasks
- **Task Status Tracking**: Track tasks with statuses (To-Do, In Progress, Done)
- **Task Assignment**: Assign tasks to team members
- **Due Dates**: Set and track task deadlines
- **Task Filtering**: View tasks by status, project, and assignment

### Dashboard & Metrics

- **Task Overview**: View total, completed, pending, and overdue tasks
- **Progress Tracking**: Calculate project completion rates
- **Overdue Alerts**: Identify tasks past their due dates
- **Performance Metrics**: Completion rates and overdue percentages

### User Interface

- **Responsive Web Interface**: Mobile-friendly design with CSS grid layouts
- **Dashboard Page**: Quick overview of all tasks and projects
- **Project Management Page**: View and manage all projects
- **Task Forms**: Create and edit tasks with validation
- **Team Management**: Add/remove team members from projects

## 🛠 Tech Stack

### Backend

- **Django** 6.0.4 - Web framework
- **Django REST Framework** 3.14.0 - REST API development
- **SimpleJWT** 5.3.2 - JWT authentication
- **SQLite** - Database (default)

### Frontend

- **Django Templates** - Server-side rendering
- **HTML5** - Markup
- **CSS3** - Styling with responsive design
- **JavaScript** - Client-side interactivity (minimal)

## 📦 Project Structure

```
ProjectManager/
├── ProjectManager/           # Main Django configuration
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL router
│   ├── wsgi.py              # WSGI application
│   └── asgi.py              # ASGI application
├── accounts/                # User authentication app
│   ├── models.py            # CustomUser model
│   ├── views.py             # Auth views (API & Template)
│   ├── serializers.py       # DRF serializers
│   ├── admin.py             # Admin interface
│   ├── urls.py              # Auth routes
│   └── migrations/          # Database migrations
├── projects/                # Project management app
│   ├── models.py            # Project & ProjectMember models
│   ├── views.py             # Project CRUD & template views
│   ├── serializers.py       # DRF serializers
│   ├── admin.py             # Admin interface
│   ├── urls.py              # Project routes
│   └── migrations/          # Database migrations
├── tasks/                   # Task management app
│   ├── models.py            # Task model
│   ├── views.py             # Task CRUD & template views
│   ├── serializers.py       # DRF serializers
│   ├── admin.py             # Admin interface
│   ├── urls.py              # Task routes
│   └── migrations/          # Database migrations
├── dashboard/               # Dashboard app
│   ├── views.py             # Dashboard API & template views
│   ├── urls.py              # Dashboard routes
│   └── admin.py             # Admin interface
├── templates/               # Django HTML templates
│   ├── base.html            # Base template (navbar, footer)
│   ├── login.html           # Login page
│   ├── signup.html          # Registration page
│   ├── dashboard.html       # Dashboard with metrics
│   ├── projects.html        # Projects list
│   ├── project_form.html    # Create/edit project
│   ├── project_detail.html  # Project details & tasks
│   ├── task_form.html       # Create/edit task
│   └── add_member.html      # Add team member form
├── static/                  # Static files
│   └── css/
│       └── style.css        # Main stylesheet
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (not in repo)
├── db.sqlite3               # SQLite database
└── README.md                # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Installation

1. **Clone or navigate to the project directory**

```bash
cd d:\PlacementStuff\EtharAi\TestCode
```

1. **Create a virtual environment**

```bash
python -m venv venv
venv\Scripts\activate  # On Windows
```

1. **Install dependencies**

```bash
pip install -r requirements.txt
```

1. **Create environment file (.env)**

```bash
# Create .env file in the project root
SECRET_KEY=your-secret-key-here
DEBUG=True
```

1. **Run migrations**

```bash
python manage.py migrate
```

1. **Create superuser (admin account)**

```bash
python manage.py createsuperuser
```

1. **Run development server**

```bash
python manage.py runserver
```

1. **Access the application**

- Web Interface: `http://localhost:8000`
- Admin Panel: `http://localhost:8000/admin`

## 📱 Usage Guide

### User Registration & Login

1. Navigate to `/signup/` to create a new account
2. Enter your email, name, and password
3. Login via `/login/` with your credentials

### Creating a Project

1. After login, click "New Project" on the dashboard
2. Enter project name and description
3. You'll automatically become the project admin

### Managing Team Members

1. Go to project details
2. Click "Add Member"
3. Enter team member's email and assign role (Admin/Member)

### Creating Tasks

1. Navigate to project detail page
2. Click "Create Task"
3. Fill in task details:
   - Title (required)
   - Description
   - Status (To-Do, In Progress, Done)
   - Assign to team member
   - Set due date

### Updating Tasks

- **Admins**: Can edit title, description, status, assignment, and due date
- **Assigned Users**: Can only update task status
- All users: See assigned tasks in their project view

### Dashboard

- View overall task metrics
- See all your projects
- Quick access to task statistics

## 🔐 Authentication & Authorization

### Authentication Methods

1. **Session-based** (Web UI): Uses Django sessions for login
2. **JWT Token** (REST API): Bearer token authentication for API endpoints

### Permission System

The application uses a centralized `PermissionChecker` class for role-based access:

| Action | Admin | Member |
|--------|-------|--------|
| Create Project | Yes | Yes |
| Edit Project | Yes | No |
| Delete Project | Yes | No |
| Add Members | Yes | No |
| Remove Members | Yes | No |
| Create Task | Yes | No |
| Update Task | Yes | Yes (own status) |
| Delete Task | Yes | No |
| View Tasks | Yes | Yes |

## 🔗 API Endpoints

### Authentication Endpoints

```
POST   /api/auth/signup/              - Register new user
POST   /api/auth/login/               - Login (returns access & refresh tokens)
GET    /api/auth/me/                  - Get current user info
POST   /api/auth/token/refresh/       - Refresh JWT token
```

### Project Endpoints

```
GET    /api/projects/                 - List all projects
POST   /api/projects/                 - Create new project
GET    /api/projects/<id>/            - Get project details
DELETE /api/projects/<id>/            - Delete project
POST   /api/projects/<id>/add-member/ - Add team member
DELETE /api/projects/<id>/members/<member_id>/ - Remove member
```

### Task Endpoints

```
GET    /api/tasks/projects/<project_id>/tasks/     - List project tasks
POST   /api/tasks/projects/<project_id>/tasks/     - Create task
GET    /api/tasks/tasks/<id>/                      - Get task details
PATCH  /api/tasks/tasks/<id>/                      - Update task
DELETE /api/tasks/tasks/<id>/                      - Delete task
```

### Dashboard Endpoints

```
GET    /api/dashboard/summary/        - Get dashboard metrics
```

## 🌐 Web Routes

### Authentication Routes

```
GET  /signup/                          - Registration page
POST /signup/                          - Submit registration form
GET  /login/                           - Login page
POST /login/                           - Submit login form
GET  /logout/                          - Logout user
```

### Dashboard & Project Routes

```
GET  /dashboard/                       - Dashboard page
GET  /projects/                        - List all projects
GET  /projects/new/                    - Create project form
POST /projects/new/                    - Submit new project
GET  /projects/<id>/                   - Project details page
GET  /projects/<id>/add-member/        - Add member form
POST /projects/<id>/add-member/        - Submit add member form
```

### Task Routes

```
GET  /projects/<project_id>/tasks/create/  - Create task form
POST /projects/<project_id>/tasks/create/  - Submit create task
GET  /tasks/<id>/edit/                     - Edit task form
POST /tasks/<id>/edit/                     - Submit edit task
GET  /tasks/<id>/delete/                   - Delete task (confirmation)
POST /tasks/<id>/delete/                   - Confirm task deletion
```

## 📊 Database Models

### CustomUser

```python
- email (unique)
- name
- password (hashed)
- created_at
- is_active
- is_admin
```

### Project

```python
- name
- description
- created_by (FK to CustomUser)
- created_at
- updated_at
```

### ProjectMember

```python
- user (FK to CustomUser)
- project (FK to Project)
- role (admin/member)
- joined_at
- unique_together: (user, project)
```

### Task

```python
- project (FK to Project)
- title
- description
- status (todo/in_progress/done)
- assigned_to (FK to CustomUser, nullable)
- due_date (nullable)
- created_by (FK to CustomUser)
- created_at
- updated_at
```

## 🎨 Styling

The application uses a custom CSS stylesheet (`static/css/style.css`) featuring:

- **Responsive Grid Layout**: Mobile-first design with grid-2 and grid-3 layouts
- **Card-based UI**: Modern card components with shadows and hover effects
- **Status Badges**: Color-coded task status indicators
- **Progress Bars**: Visual task completion progress
- **Navbar**: Navigation with auth links
- **Forms**: Centered, clean form layout
- **Color Scheme**: Professional blue/white with status colors (green/orange/red)

## 🔧 Configuration

### Environment Variables (.env)

```
SECRET_KEY=your-django-secret-key
DEBUG=True  # Set to False in production
DATABASE_URL=sqlite:///db.sqlite3  # Optional
```

### Key Settings (settings.py)

- **AUTH_USER_MODEL**: `accounts.CustomUser`
- **DATABASES**: SQLite by default
- **STATIC_FILES_DIRS**: `static/` folder
- **TEMPLATES_DIR**: `templates/` folder
- **JWT Settings**:
  - Access Token Lifetime: 1 hour
  - Refresh Token Lifetime: 7 days
  - Token Rotation: Enabled

## 🧪 Admin Interface

Access the Django admin at `/admin/` with superuser credentials:

- View and manage users
- Create/edit projects and tasks
- Manage project members
- View task assignments

## 🐛 Troubleshooting

### Common Issues

**Issue**: "No such table: accounts_customuser"

- **Solution**: Run migrations: `python manage.py migrate`

**Issue**: "Permission denied" when accessing project

- **Solution**: Ensure you're a member of the project or admin

**Issue**: Static files not loading (CSS/images)

- **Solution**: Run `python manage.py collectstatic` and check STATIC_URL/STATIC_ROOT settings

**Issue**: Task assignment to non-member

- **Solution**: User must be added as project member before task assignment

## 📝 Development Notes

### Adding New Features

1. Create models in the appropriate app
2. Create serializers for API validation
3. Create views for both API (APIView) and templates (View)
4. Add URLs to app's urls.py
5. Run migrations: `python manage.py makemigrations && python manage.py migrate`

### Creating Custom Permissions

Add methods to the `PermissionChecker` class in `permissions.py`:

```python
@staticmethod
def can_do_something(user, object):
    # Your permission logic
    return user.is_admin
```

## 📚 Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [SimpleJWT Documentation](https://django-rest-framework-simplejwt.readthedocs.io/)

## 📄 License

This project is provided as-is for educational and commercial use.

## 👥 Contributing

For bug reports or feature requests, please document the issue clearly with:

- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details

## 🚀 Deployment

For production deployment:

1. Set `DEBUG=False` in `.env`
2. Update `SECRET_KEY` with a secure value
3. Update `ALLOWED_HOSTS` with your domain
4. Use a production database (PostgreSQL recommended)
5. Use a production WSGI server (Gunicorn, uWSGI)
6. Enable HTTPS/SSL
7. Set `SECURE_SSL_REDIRECT=True`

## 📞 Support

For issues or questions:

1. Check the troubleshooting section above
2. Review Django and DRF documentation
3. Check admin panel for data integrity issues
4. Review application logs for error details

---

**Last Updated**: May 2, 2026
**Version**: 1.0.0
**Django Version**: 6.0.4
**Python Version**: 3.8+
