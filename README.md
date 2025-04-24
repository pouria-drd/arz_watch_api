# ArzWatch API

A Django-based API for monitoring and tracking currency exchange rates and market data, with built-in web scraping capabilities.

## Table of Contents

-   [Project Structure](#project-structure)
-   [Features](#features)
-   [Prerequisites](#prerequisites)
-   [Installation](#installation)
-   [Contact](#contact)

## Project Structure

```
arz_watch_api/
├── api_keys/           # API key management
├── arz_watch_api/      # Django project configuration
├── scrapers/           # Web scraping modules
│   ├── admin/         # Admin interface configurations
│   ├── migrations/    # Database migrations
│   ├── modules/       # Scraping modules
│   ├── serializers/   # API serializers
│   ├── views/         # API views
│   ├── management/    # Custom management commands
│   ├── tests.py       # Test cases
│   ├── apps.py        # App configuration
│   └── urls.py        # URL routing
├── scrapers_output/    # Output directory for scraped data
├── logs/              # Application logs
├── telegram/          # Telegram bot integration
├── .env               # Environment variables
├── manage.py          # Django management script
├── requirements.txt   # Python dependencies
└── ArzWatchAPI_DB.sqlite3  # SQLite database file
```

## Features

-   Django REST Framework based API
-   Web scraping capabilities for currency data
-   TGJU (Tehran Gold and Jewelry Union) data integration
-   Logging system for tracking operations
-   Admin interface for data management
-   CORS support for cross-origin requests
-   Environment variable configuration
-   JWT Authentication
-   API Throttling
-   Email notifications
-   Comprehensive logging system

## Prerequisites

-   Python 3.x
-   SQLite3
-   Virtual environment (recommended)
-   Git

## Installation

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/pouria-drd/arz_watch_api.git
    cd arz_watch_api
    ```

2. **Create and Activate a Virtual Environment:**

    ```bash
    python -m venv .venv
    # On Windows:
    .venv\Scripts\activate
    # On Unix or MacOS:
    source .venv/bin/activate
    ```

3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up Environment Variables:**

    Create a `.env` file in the project root and add the following:

    ```ini
    # Base Configuration
    DEBUG=True
    SECRET_KEY=your_secret_key_here
    TIME_ZONE=UTC
    USE_TZ=True
    USE_I18N=True

    # Static and Media Files
    STATIC_URL=static/
    STATIC_ROOT=static
    MEDIA_URL=/media/
    MEDIA_ROOT=media

    # Host Configuration
    ALLOWED_HOSTS=localhost,127.0.0.1
    INTERNAL_IPS=127.0.0.1

    # CORS Configuration
    CORS_ALLOW_CREDENTIALS=True
    CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
    CSRF_TRUSTED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

    # API Throttling
    USER_THROTTLE_RATE=20/minute
    ANON_THROTTLE_RATE=10/minute


    # Scrapers Schedulers Configuration
    INITIAL_RUN="False"
    INTERVAL_TRIGGER_MINUTES="10"

    # Email Configuration
    EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
    EMAIL_HOST=smtp.gmail.com
    EMAIL_PORT=587
    EMAIL_USE_TLS=True
    EMAIL_HOST_USER=your-email@example.com
    EMAIL_HOST_PASSWORD=your-email-password
    DEFAULT_FROM_EMAIL=no-reply@example.com
    ```

5. **Run Migrations:**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6. **Create a Superuser:**

    ```bash
    python manage.py createsuperuser
    ```

7. **Run the Development Server:**

    ```bash
    python manage.py runserver
    ```

    Your project should now be running at `http://127.0.0.1:8000/`.

## Usage

The API will be available at `http://127.0.0.1:8000/`. You can access:

-   Admin interface at `http://127.0.0.1:8000/admin/`
-   API endpoints at `http://127.0.0.1:8000/api/`
-   API documentation at `http://127.0.0.1:8000/api/docs/`

## Dependencies

The project uses several key Python packages:

-   Django 5.2
-   Django REST Framework
-   BeautifulSoup4
-   Selenium
-   Requests
-   Python-dotenv
-   Django CORS Headers
-   Django Debug Toolbar
-   Gunicorn (for production)

## API Documentation

The API endpoints are configured in `arz_watch_api/urls.py` and `scrapers/urls.py`. For detailed API documentation, please refer to the API documentation section in the admin interface.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries, please contact [pouriadrd@gmail.com](mailto:pouriadrd@gmail.com).
