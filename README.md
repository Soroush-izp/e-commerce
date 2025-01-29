# E-Commerce Backend API (Beta)

This is the beta version of the E-Commerce Backend API.

## Beta Version Notes
- This is a pre-release version
- Features may be incomplete or subject to change
- Not recommended for production use
- Please report any issues

## Quick Start
```bash
# Clone the repository
git clone https://github.com/yourusername/e-commerce.git
cd e-commerce

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your settings

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

A Django REST Framework-based e-commerce backend with comprehensive features for product management, user authentication, order processing, and payment integration.

## Features

### Authentication
- JWT-based authentication
- User registration and login
- Role-based access control (Admin, Staff, Regular users)
- Profile management

### Product Management
- Brand management with media support (photos, videos)
- Category hierarchy
- Product variants (SKUs)
- Dynamic attribute management
- Product reviews with rich media content
- Structured product details

### Order System
- Shopping cart functionality
- Wishlist management
- Order processing with status tracking
- Soft delete support for cart items
- Order history

### Payment Integration
- Zarinpal payment gateway integration
- Payment status tracking
- Payment history
- Secure transaction handling

### Location Management
- Address management
- Iranian cities integration
- Province and city selection

### Core Features
- Request logging middleware
- Custom exception handling
- Redis caching integration
- File validation
- Comprehensive test coverage
- API documentation with drf-spectacular

## Technical Stack

- Python 3.11+
- Django 4.2+
- Django REST Framework 3.14+
- PostgreSQL 15+
- Redis 7+ (optional, for caching)
- JWT Authentication
- drf-spectacular (API documentation)
- Zarinpal Payment Gateway
- Iranian Cities Database

## Project Structure
```
e_commerce/
├── accounts/        # User management
├── catalog/         # Product management
├── core/           # Core functionality
├── locations/      # Address management
├── orders/         # Order processing
├── payments/       # Payment handling
└── e-commerce/     # Project settings
```

## Setup

1. Clone the repository
2. Create and activate a virtual environment
3. Install dependencies:
```bash
# Core dependencies
pip install -r requirements.txt

# Additional required packages
pip install python-dotenv
pip install psycopg2-binary  # For PostgreSQL
pip install redis            # For Redis caching
pip install Pillow          # For image handling
```

4. Set up environment variables:
```bash
cp .env.example .env
```
Edit `.env` with your configuration:
```
# Database settings
DATABASE_NAME=your_db_name
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password
DATABASE_HOST=localhost
DATABASE_PORT=5432

# Redis settings
REDIS_URL=redis://localhost:6379

# Django settings
DJANGO_SECRET_KEY=your_secret_key
DEBUG=True

# Zarinpal settings
ZARINPAL_MERCHANT_ID=your_merchant_id
SANDBOX=True
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

## API Documentation

Access the API documentation at:
- Swagger UI: `/api/docs/`
- ReDoc: `/api/redoc/`
- OpenAPI Schema: `/api/schema/`

## Testing

Run the test suite:
```bash
python manage.py test
```

## Permissions

The API implements role-based access control:
- Admin users have full access
- Staff users have limited administrative access
- Regular users can manage their own data
- Some endpoints are publicly accessible

## Caching

Redis caching is implemented for:
- Product listings
- Category trees
- Brand information
- Other frequently accessed data

## Error Handling

Custom exception handling provides:
- Consistent error responses
- Detailed error messages in development
- Sanitized messages in production
- Request logging for debugging

## Contributing

Please read our [Contributing Guidelines](CONTRIBUTING.md) before submitting a Pull Request.

### Development Process
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

MIT License

Copyright (c) 2024 Soroush Izadpanah
