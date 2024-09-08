# Authentication Interface Project

This project implements a comprehensive authentication system with a user interface built using NiceGUI. It provides a full suite of authentication features, including signup, signin, signout, password management, and OAuth integration.

## Features

The authentication service (`AuthService`) in `src/modules/auth/services/auth_service.py` offers the following functionalities:

- User signup with email verification
- User signin
- User signout
- Password reset (forgot password)
- OAuth authentication (with Google support)
- Account activation
- Session management

## Routes

The project includes the following routes:

- `/auth`: Redirects to signin page
- `/auth/signin`: User login
- `/auth/signup`: User registration
- `/auth/forgot-password`: Forgot password
- `/auth/reset-password`: Password reset
- `/auth/activate`: Account activation
- `/auth/google/callback`: Google OAuth callback
- `/auth/signout`: User logout
- `/admin`: Redirects to admin dashboard
- `/admin/dashboard`: Admin dashboard (protected route)

## Technology Stack

- Backend: Python
- Frontend: NiceGUI
- Database: SQLAlchemy (ORM) with SQLite
- Authentication: Custom implementation with OAuth support
- Email: Custom email service
- Testing: pytest

## Project Structure

The project is organized into the following main directories:

- `src/`: Contains the main source code of the application
  - `app/`: Implements the frontend using NiceGUI
    - `components/`: UI components for authentication and admin interfaces
    - `decorators/`: Authentication and authorization decorators
    - `handlers/`: Request handlers for authentication-related operations
    - `pages/`: Page definitions for authentication and admin routes
    - `validations/`: Input validation functions
  - `config/`: Application configuration files
  - `modules/`: Contains the core business logic and services
    - `auth/`: Authentication module
      - `models/`: Database models for authentication-related entities
      - `repositories/`: Data access layer for auth entities
      - `schemas/`: Data validation schemas
      - `services/`: Business logic for authentication operations
    - `shared/`: Shared utilities and services
      - `di/`: Dependency injection container
      - `services/`: Shared services like email and logging
      - `sql/`: SQL-related utilities and base classes
      - `templates/`: Email templates
      - `translations/`: Internationalization files
    - `user/`: User management module
      - `models/`: User-related database models
      - `repositories/`: Data access layer for user entities
      - `services/`: User-related business logic
- `tests/`: Contains test files for the project

The `app` directory implements the frontend using NiceGUI, providing a user interface for authentication and admin functionalities. The `modules` directory contains the core business logic, separated into different modules such as `auth`, `shared`, and `user`. Each module has its own set of models, repositories, and services.

The `tests` directory contains unit and integration tests for various components of the application, ensuring the reliability and correctness of the implemented features.

## Setup and Configuration

1. Clone the repository:

   ```
   git clone git@github.com:medinamarquezp/pyauth.git
   cd pyauth
   ```

2. Create a virtual environment and activate it:

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the root directory and add the following variables:

   ```
   DATABASE_URL=sqlite:///app.db
   FRONTEND_URL=http://localhost:8080
   EMAIL_SMTP_SERVER=your_smtp_server
   EMAIL_SMTP_PORT=your_smtp_port
   EMAIL_SMTP_USERNAME=your_email@example.com
   EMAIL_SMTP_PASSWORD=your_email_password
   EMAIL_SMTP_FROM=noreply@example.com
   OAUTH_GOOGLE_CLIENT_ID=your_google_client_id
   OAUTH_GOOGLE_CLIENT_SECRET=your_google_client_secret
   OAUTH_GOOGLE_REDIRECT_URI=http://localhost:8080/auth/google/callback
   ```

5. Set up the database:
   ```
   alembic upgrade head
   ```

## Running the Project

To run the project:
`python src/app/main.py`

The application will be available at `http://localhost:8080`.

## Running Tests

To run the tests:

```
pytest
```

This will run all the tests in the `tests/` directory.

## Development

- The project uses Alembic for database migrations. To create a new migration:

  ```
  alembic revision --autogenerate -m "Description of the changes"
  ```

- To apply migrations:

  ```
  alembic upgrade head
  ```

- The `src/modules/shared/translations/` directory contains translation files for internationalization.

## Security Notes

- Ensure that `OAUTHLIB_INSECURE_TRANSPORT` is set to `0` in production environments.
- Review and update the password validation rules in `src/app/validations/auth_validations.py` as needed.
- Make sure to use HTTPS in production for secure communication.
