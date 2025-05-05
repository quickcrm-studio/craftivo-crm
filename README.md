# Craftivo CRM

A Django-based CRM system for managing handmade goods online store operations.

## Project Structure

```
.
└── backend/           # Django backend application
```

## Tech Stack

- Backend: Django 4.x + Django REST Framework
- Database: PostgreSQL
- Caching: Redis
- Containerization: Docker

## Getting Started

### Prerequisites

- Python 3.11+
- Docker and Docker Compose
- Git

### Development Setup

1. Clone the repository:
   ```bash
   git clone [repository-url]
   cd craftivo-crm
   ```

2. Set up the backend:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Start the development environment with Docker:
   ```bash
   docker-compose up -d
   ```

4. Access the Django admin interface at:
   ```
   http://localhost:8000/admin/
   ```

5. To run tests:
   ```bash
   cd backend
   python run_tests.py
   ```

## Contributing

Please read [CONTRIBUTING.md](docs/CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 
