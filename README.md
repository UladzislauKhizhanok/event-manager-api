# Event Manager API

This project is a RESTful API built with Django Rest Framework for managing events.
It includes user authentication, event creation, registration, and more.

## Table of Contents

-  [Installation](#installation)
-  [Usage](#usage)
-  [Running Tests](#running-tests)
-  [API Documentation](#api-documentation)
-  [Environment Variables](#environment-variables)

## Installation

To get started with the project, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/event-manager.git
   cd event-manager
   ```

2. **Build and run the Docker containers:**

   ```bash
   docker-compose up --build
   # or
   make up
   ```

   This will build the Docker image and start the containers.

## Usage

Once the containers are up and running, you can access the API at `http://localhost:8000`.

### API Endpoints

#### Users
-  **User Registration:** `POST /api/users/register/`
-  **User Login:** `POST /api/users/login/`
-  **Token Refresh:** `POST /api/users/refresh/`
-  **Verify Token:** `POST /api/users/verify/`
-  **Get Current User:** `GET /api/users/me/`

#### Events
-  **List Events /w filters:** `GET /api/events/`
-  **Create Event:** `POST /api/events/`
-  **Retrieve Event:** `GET /api/events/{id}/`
-  **Update Event:** `PUT /api/events/{id}/`
-  **Partial Update Event:** `PATCH /api/events/{id}/`
-  **Delete Event:** `DELETE /api/events/{id}/`
-  **Register for Event:** `POST /api/events/{id}/register/`
-  **Unregister from Event:** `POST /api/events/{id}/unregister/`

## Running Tests

To run the tests, use the following command:

```bash
docker compose run --rm web test
# or
make test
```

This will build the Docker image and run the tests inside the container.

## API Documentation

The API documentation is available at `http://localhost:8000/api/docs/`.

When you navigate to the root URL (`http://localhost:8000/`), you will be redirected to the API documentation.

<img src="/docs/swagger_ui.png" width="50%">

## Environment Variables

The following environment variables are used in the project:

-  `SECRET_KEY`: The secret key for Django.
-  `DEBUG`: Set to `1` to enable debug mode, `0` to disable.
-  `ALLOWED_HOSTS`: A comma-separated list of allowed hosts.
-  `DATABASE_NAME`: The path to the SQLite database file.
