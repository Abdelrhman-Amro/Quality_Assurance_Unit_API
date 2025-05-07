# Standards App API Documentation

This document provides information about the API endpoints available in the Standards app.

## Authentication

All endpoints require JWT authentication. Include the JWT token in the Authorization header:

```
Authorization: Bearer <your_token>
```

## Endpoints

### Academic Years

-   **GET /api/academic-years/** - List all academic years (All authenticated users)
-   **GET /api/academic-years/{id}/** - Retrieve a specific academic year (All authenticated users)
-   **POST /api/academic-years/** - Create a new academic year (Admin only)
-   **PUT/PATCH /api/academic-years/{id}/** - Update an academic year (Admin only)
-   **DELETE /api/academic-years/{id}/** - Delete an academic year (Admin only)

### Standards

-   **GET /api/standards/** - List all standards (All authenticated users)
-   **GET /api/standards/{id}/** - Retrieve a specific standard (All authenticated users)
-   **POST /api/standards/** - Create a new standard (Admin only)
-   **PUT/PATCH /api/standards/{id}/** - Update a standard (Admin only)
-   **DELETE /api/standards/{id}/** - Delete a standard (Admin only)

### Pointers

-   **GET /api/pointers/** - List all pointers (All authenticated users)
-   **GET /api/pointers/{id}/** - Retrieve a specific pointer (All authenticated users)
-   **POST /api/pointers/** - Create a new pointer (Admin only)
-   **PUT/PATCH /api/pointers/{id}/** - Update a pointer (Admin only)
-   **DELETE /api/pointers/{id}/** - Delete a pointer (Admin only)

### Elements

-   **GET /api/elements/** - List all elements (All authenticated users)
-   **GET /api/elements/{id}/** - Retrieve a specific element (All authenticated users)
-   **POST /api/elements/** - Create a new element (Admin only)
-   **PUT/PATCH /api/elements/{id}/** - Update an element (Admin only)
-   **DELETE /api/elements/{id}/** - Delete an element (Admin only)

### Attachments

-   **GET /api/attachments/** - List all attachments (All authenticated users)
-   **GET /api/attachments/{id}/** - Retrieve a specific attachment (All authenticated users)
-   **POST /api/attachments/** - Create a new attachment (Admin or Owner)
-   **PUT/PATCH /api/attachments/{id}/** - Update an attachment (Admin or Owner)
-   **DELETE /api/attachments/{id}/** - Delete an attachment (Admin or Owner)
-   **GET /api/attachments/{id}/download/** - Download an attachment file (Admin, Owner, or Shared With)
-   **POST /api/attachments/{id}/upload/** - Upload a file to an attachment (Admin, Supervisor, or TA)

### Requests

-   **GET /api/requests/** - List all requests (Admin sees all, others see only their own)
-   **GET /api/requests/{id}/** - Retrieve a specific request (Admin, Requester, or Receiver)
-   **POST /api/requests/** - Create a new request (Supervisor or TA)
-   **PUT/PATCH /api/requests/{id}/** - Update a request (Admin, Requester, or Receiver)
-   **DELETE /api/requests/{id}/** - Delete a request (Admin, Requester, or Receiver)
-   **POST /api/requests/{id}/approve/** - Approve a request (Admin or Receiver)
-   **POST /api/requests/{id}/reject/** - Reject a request (Admin or Receiver)
-   **POST /api/requests/{id}/cancel/** - Cancel a request (Admin or Requester)

## User Roles and Permissions

-   **ADMIN**: Full access to all endpoints and actions
-   **SUPERVISOR/TA/PROFESSOR**: Can retrieve and list all resources
-   **SUPERVISOR/TA**: Can upload/download their attachments, manage their requests, and download shared attachments

## Pagination

All list endpoints support pagination with the following query parameters:

-   `page`: Page number (default: 1)
-   `page_size`: Number of items per page (default: 20, max: 50)

Example: `/api/academic-years/?page=2&page_size=10`
