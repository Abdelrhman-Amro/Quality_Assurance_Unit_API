# Quality Assurance Unit API Documentation

## Overview

This document provides information about all available API endpoints in the Quality Assurance Unit system. The API uses JWT authentication and follows RESTful principles.

## Authentication

### Obtaining Tokens

-   **Endpoint**: `/api/token/`
-   **Method**: POST
-   **Description**: Get JWT access and refresh tokens
-   **Request Body**:
    ```json
    {
        "email": "user@example.com",
        "password": "your_password"
    }
    ```
-   **Response**:
    ```json
    {
        "access": "access_token_string",
        "refresh": "refresh_token_string"
    }
    ```

### Refreshing Tokens

-   **Endpoint**: `/api/token/refresh/`
-   **Method**: POST
-   **Description**: Get a new access token using refresh token
-   **Request Body**:
    ```json
    {
        "refresh": "your_refresh_token"
    }
    ```
-   **Response**:
    ```json
    {
        "access": "new_access_token_string"
    }
    ```

## User Management

### List/Create Users

-   **Endpoint**: `/api/users/`
-   **Methods**: GET, POST
-   **Access**: Admin only
-   **Description**: Get all users or create a new user
-   **Filters**:
    -   `role`: Filter by user role (ADMIN, SUPERVISOR, PROFESSOR, TA)
-   **Ordering**:
    -   `username`, `last_login`, `date_joined`
-   **Search**: Search by `username`

### Get Current User

-   **Endpoint**: `/api/users/me/`
-   **Method**: GET
-   **Access**: Authenticated users
-   **Description**: Get current authenticated user's details

### Get/Update/Delete Single User

-   **Endpoint**: `/api/users/{id}/`
-   **Methods**: GET, PUT, PATCH, DELETE
-   **Access**: Admin only
-   **Description**: Get, update or delete a specific user

## Academic Years

### List/Create Academic Years

-   **Endpoint**: `/api/academic-years/`
-   **Methods**: GET, POST
-   **Access**: GET (authenticated), POST (admin only)
-   **Description**: Get all academic years or create a new one
-   **Filters**:
    -   `status`: Filter by status (ACTIVE, ARCHIVED)
-   **Ordering**:
    -   `start_date`
-   **Search**: Search by `start_date`

### Get/Update/Delete Single Academic Year

-   **Endpoint**: `/api/academic-years/{id}/`
-   **Methods**: GET, PUT, PATCH, DELETE
-   **Access**: GET (authenticated), others (admin only)
-   **Description**: Get, update or delete a specific academic year

## Standards

### List/Create Standards

-   **Endpoint**: `/api/standards/`
-   **Methods**: GET, POST
-   **Access**: GET (authenticated), POST (admin only)
-   **Description**: Get all standards or create a new one
-   **Filters**:
    -   `type`: Filter by type (ACADEMIC, PRAGMATIC)
    -   `academic_year`: Filter by academic year ID
-   **Ordering**:
    -   `created_at`, `title`
-   **Search**: Search by `title`

### Get/Update/Delete Single Standard

-   **Endpoint**: `/api/standards/{id}/`
-   **Methods**: GET, PUT, PATCH, DELETE
-   **Access**: GET (authenticated), others (admin only)
-   **Description**: Get, update or delete a specific standard

## Pointers

### List/Create Pointers

-   **Endpoint**: `/api/pointers/`
-   **Methods**: GET, POST
-   **Access**: GET (authenticated), POST (admin only)
-   **Description**: Get all pointers or create a new one
-   **Filters**:
    -   `standard`: Filter by standard ID
-   **Ordering**:
    -   `created_at`, `title`
-   **Search**: Search by `title`

### Get/Update/Delete Single Pointer

-   **Endpoint**: `/api/pointers/{id}/`
-   **Methods**: GET, PUT, PATCH, DELETE
-   **Access**: GET (authenticated), others (admin only)
-   **Description**: Get, update or delete a specific pointer

## Elements

### List/Create Elements

-   **Endpoint**: `/api/elements/`
-   **Methods**: GET, POST
-   **Access**: GET (authenticated), POST (admin only)
-   **Description**: Get all elements or create a new one
-   **Filters**:
    -   `pointer`: Filter by pointer ID
-   **Ordering**:
    -   `created_at`, `title`
-   **Search**: Search by `title`

### Get/Update/Delete Single Element

-   **Endpoint**: `/api/elements/{id}/`
-   **Methods**: GET, PUT, PATCH, DELETE
-   **Access**: GET (authenticated), others (admin only)
-   **Description**: Get, update or delete a specific element

## Attachments

### List/Create Attachments

-   **Endpoint**: `/api/attachments/`
-   **Methods**: GET, POST
-   **Access**: GET (authenticated), POST (admin only)
-   **Description**: Get all attachments or create a new one
-   **Filters**:
    -   `element`: Filter by element ID
-   **Ordering**:
    -   `created_at`, `title`
-   **Search**: Search by `title`

### Get/Update/Delete Single Attachment

-   **Endpoint**: `/api/attachments/{id}/`
-   **Methods**: GET, PUT, PATCH, DELETE
-   **Access**: GET (authenticated), others (admin only)
-   **Description**: Get, update or delete a specific attachment

### Upload Attachment File

-   **Endpoint**: `/api/attachments/{id}/upload/`
-   **Method**: POST
-   **Access**: Users assigned to the standard or admins
-   **Description**: Upload a file to an attachment
-   **Request**: Form data with `file` field

### Remove Attachment File

-   **Endpoint**: `/api/attachments/{id}/remove/`
-   **Method**: DELETE
-   **Access**: Users assigned to the standard or admins
-   **Description**: Remove a file from an attachment

### Download Attachment File

-   **Endpoint**: `/api/attachments/{id}/download/`
-   **Method**: GET
-   **Access**: Users assigned to the standard, users in shared_with list, or admins
-   **Description**: Download an attachment file

## Requests

### List/Create Requests

-   **Endpoint**: `/api/requests/`
-   **Methods**: GET, POST
-   **Access**: Authenticated users
-   **Description**: Get all requests or create a new one
-   **Filters**:
    -   `status`: Filter by status (PENDING, APPROVED, REJECTED, CANCELED)
    -   `requester`: Filter by requester user ID
    -   `receiver`: Filter by receiver user ID
-   **Ordering**:
    -   `created_at`
-   **Search**: Search by `requester__username`, `receiver__username`

### Get/Update/Delete Single Request

-   **Endpoint**: `/api/requests/{id}/`
-   **Methods**: GET, PUT, PATCH, DELETE
-   **Access**: GET (authenticated), others (admin only)
-   **Description**: Get, update or delete a specific request

### Approve Request

-   **Endpoint**: `/api/requests/{id}/approve/`
-   **Method**: POST
-   **Access**: Request receiver or admin
-   **Description**: Approve a pending request

### Reject Request

-   **Endpoint**: `/api/requests/{id}/reject/`
-   **Method**: POST
-   **Access**: Request receiver or admin
-   **Description**: Reject a pending request

### Cancel Request

-   **Endpoint**: `/api/requests/{id}/cancel/`
-   **Method**: POST
-   **Access**: Request requester or admin
-   **Description**: Cancel a pending request

## Courses

### List/Create Courses

-   **Endpoint**: `/api/courses/`
-   **Methods**: GET, POST
-   **Access**: GET (authenticated), POST (admin only)
-   **Description**: Get all courses or create a new one
-   **Filters**:
    -   `academic_year`: Filter by academic year ID
    -   `level`: Filter by level (1, 2, 3, 4)
    -   `semester`: Filter by semester (1, 2)
-   **Ordering**:
    -   `created_at`, `title`, `credit_hours`
-   **Search**: Search by `title`, `code`

### Get/Update/Delete Single Course

-   **Endpoint**: `/api/courses/{id}/`
-   **Methods**: GET, PUT, PATCH, DELETE
-   **Access**: GET (authenticated), others (admin only)
-   **Description**: Get, update or delete a specific course

## Course Files

### List/Create Course Files

-   **Endpoint**: `/api/course-files/`
-   **Methods**: GET, POST
-   **Access**: GET (authenticated), POST (admin only)
-   **Description**: Get all course files or create a new one
-   **Filters**:
    -   `course`: Filter by course ID
-   **Ordering**:
    -   `created_at`, `title`
-   **Search**: Search by `title`

### Get/Update/Delete Single Course File

-   **Endpoint**: `/api/course-files/{id}/`
-   **Methods**: GET, PUT, PATCH, DELETE
-   **Access**: GET (authenticated), others (admin only)
-   **Description**: Get, update or delete a specific course file

## Course Attachments

### List/Create Course Attachments

-   **Endpoint**: `/api/course-attachments/`
-   **Methods**: GET, POST
-   **Access**: GET (authenticated), POST (course professor or admin)
-   **Description**: Get all course attachments or create a new one
-   **Filters**:
    -   `course_file`: Filter by course file ID
-   **Ordering**:
    -   `created_at`

### Get/Update/Delete Single Course Attachment

-   **Endpoint**: `/api/course-attachments/{id}/`
-   **Methods**: GET, PUT, PATCH, DELETE
-   **Access**: GET (authenticated), others (course professor or admin)
-   **Description**: Get, update or delete a specific course attachment

### Download Course Attachment File

-   **Endpoint**: `/api/course-attachments/{id}/download/`
-   **Method**: GET
-   **Access**: Authenticated users
-   **Description**: Download a course attachment file

## API Documentation

-   **OpenAPI Schema**: `/api/schema/`
-   **Swagger UI**: `/api/schema/swagger-ui/`
-   **ReDoc**: `/api/schema/redoc/`
