# Craftivo CRM Backend

This is the Django backend for the Craftivo CRM system, a customer relationship management system for handmade goods online stores.

## Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL (configured in docker-compose)
- Redis (configured in docker-compose)

### Installation

1. Clone the repository

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure your environment variables in a `.env` file:
   ```
   # Django settings
   DEBUG=True
   SECRET_KEY=your-secret-key-here
   ALLOWED_HOSTS=localhost,127.0.0.1

   # Database settings
   DATABASE_URL=postgres://postgres:postgres@db:5432/crm_db
   ```

5. Apply migrations:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

7. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Docker Setup

You can use Docker to run the entire application stack:

1. Start the containers:
   ```bash
   docker-compose up -d
   ```

2. Access the backend at http://localhost:8000

## Testing

### Running Tests

This project includes comprehensive tests for all apps. To run the tests:

```bash
# Run all tests
python run_tests.py

# Run tests for a specific app
python run_tests.py users

# Run tests with higher verbosity
python run_tests.py -v 2

# Run tests without coverage
python run_tests.py --no-coverage
```

### Coverage Report

After running tests with coverage, you can view the HTML coverage report:

```bash
# Open the coverage report
open htmlcov/index.html  # On Windows: start htmlcov/index.html
```

## Project Structure

- `config/`: Project configuration and settings
- `users/`: User authentication and management
- `customers/`: Customer data and management
- `products/`: Product catalog and inventory
- `orders/`: Order processing and tracking

## API Documentation

The API documentation is available at `/api/schema/swagger-ui/` when the server is running.

## License

This project is licensed under the MIT License. 