# E-Commerce CRM

A Django-based CRM system for managing handmade goods online store operations.

## Project Structure

```
.
├── backend/           # Django backend application
├── frontend/          # Next.js frontend application
├── infrastructure/    # Docker, deployment, and infrastructure configurations
├── docs/             # Project documentation
└── tests/            # End-to-end and integration tests
```

## Tech Stack

- Backend: Django 4.x + Django REST Framework
- Frontend: React with Next.js
- Database: PostgreSQL
- Caching: Redis
- Containerization: Docker
- CI/CD: GitHub Actions

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker and Docker Compose
- Git

### Development Setup

1. Clone the repository:
   ```bash
   git clone [repository-url]
   cd e-commerce-crm
   ```

2. Set up the backend:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Set up the frontend:
   ```bash
   cd frontend
   npm install
   ```

4. Start the development environment:
   ```bash
   docker-compose up -d
   ```

## Contributing

Please read [CONTRIBUTING.md](docs/CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 