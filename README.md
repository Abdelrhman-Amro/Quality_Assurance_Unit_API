# Quality Assurance Unit - Project Documentation

## Project Overview

The Quality Assurance Unit (QAU) API is a comprehensive system designed to manage quality assurance processes in educational institutions. It enables administrators, supervisors, professors, and teaching assistants to collaborate on standards, share documents, and manage courses.

## Key Features

-   **User Management**: Role-based access control with four roles (Admin, Supervisor, Professor, TA)
-   **Standards Management**: Create and manage academic and pragmatic standards
-   **Document Management**: Upload, share, and request access to attachments
-   **Course Management**: Track courses, course files, and related documents
-   **Academic Year Management**: Organize standards and courses by academic years
-   **API-First Design**: RESTful API with JWT authentication

## System Architecture

### Core Apps

-   **Users App**:

    -   Custom user model with role-based permissions
    -   Authentication using JWT tokens
    -   User profile management

-   **Standards App**:

    -   Academic year management (Active/Archived)
    -   Standards management (Academic/Pragmatic)
    -   Hierarchical structure: Standard → Pointer → Element → Attachment
    -   Request system for file sharing

-   **Courses App**:
    -   Course management linked to professors and academic years
    -   Course files and attachments
    -   Permission-based access to files

### Technology Stack

-   **Backend**: Django 5.2 with Django REST Framework 3.16
-   **Database**: PostgreSQL 16
-   **Authentication**: JWT using Simple JWT
-   **API Documentation**: drf-spectacular (OpenAPI 3.0)
-   **Containerization**: Docker & Docker Compose
-   **Data Filtering**: django-filter

## Database Schema

### Users App

-   `User`: Custom user model extending Django's AbstractUser
    -   Fields: id (UUID), email, role, username, password, etc.

### Standards App

-   `AcademicYear`: Academic year with active/archived status
    -   Fields: id, status, start_date, end_date
-   `Standard`: Standard associated with an academic year
    -   Fields: id, academic_year, title, type, assigned_to (many-to-many with User)
-   `Pointer`: Component of a standard
    -   Fields: id, standard, title
-   `Element`: Component of a pointer
    -   Fields: id, pointer, title
-   `Attachment`: File attached to an element
    -   Fields: id, element, file, title, uploaded_by, shared_with (many-to-many with User)
-   `Request`: Access request for an attachment
    -   Fields: id, requester, receiver, made_on (attachment), status

### Courses App

-   `Course`: Course associated with an academic year and professor
    -   Fields: id, academic_year, professor, title, code, level, semester, credit_hours
-   `CourseFile`: File associated with a course
    -   Fields: id, course, title
-   `CourseAttachment`: File attached to a course file
    -   Fields: id, course_file, file

## Environment Setup

### Prerequisites

-   Python
-   Docker and Docker Compose
-   Git
-   A code editor (e.g., VS Code)

### Local Development Setup

1. **Clone the repository**:

    ```bash
    git clone [repository-url]
    cd Quality_Assurance_Unit_API
    ```

2. **Create environment file**:

    - Create `.env` file in the root directory of the project.
        ```bash
        touch .env
        ```
    - Copy the contents of `.env.example` in section (Ready variables for testing) to `.env`.

3. **Start the application**:

    ```bash
    docker-compose up -d
    ```

4. **Access the application**:
    - API: http://localhost:8000/api/
    - API documentation: http://localhost:8000/api/schema/swagger-ui/
    - Admin panel: http://localhost:8000/admin/

## Security Considerations

-   JWT tokens expire after 15 minutes
-   Refresh tokens expire after 7 days
-   Role-based access control for all endpoints
-   File access is controlled through permissions
-   User passwords are properly hashed

## For More Details

For more information on the Project, please refer to the following link: [Deatiled Documentation](https://www.notion.so/QAU_Puplic_Docs-2034c4b365c980ab8477ed6bdf639fd6?source=copy_link)
