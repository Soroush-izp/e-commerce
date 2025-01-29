# E-Commerce Platform

A robust e-commerce platform built with Django REST Framework, featuring product management, shopping cart functionality, order processing, and secure payment integration.

## Features

- **User Authentication & Authorization**: Secure user registration and login.
- **Product Catalog Management**: Admins can manage products, categories, and brands.
- **Shopping Cart System**: Users can add products to their shopping cart and manage items.
- **Order Processing**: Users can place orders and track their status.
- **Payment Integration**: Secure payment processing through Zarinpal.
- **Address & Location Management**: Users can manage their addresses.
- **Admin Dashboard**: Admins can manage users, orders, products, and more.
- **API Documentation**: Automatically generated API documentation using Swagger/ReDoc.

## Prerequisites

- Python 3.8+
- PostgreSQL
- Virtual Environment
- Git (for version control)

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd e-commerce
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file**:
   Copy the `.env.example` file to `.env` and update the values according to your setup. Ensure you include:
   - Django settings
   - Database settings
   - Email settings
   - Payment gateway settings

5. **Setup the database**:
   Make sure PostgreSQL is running and create a database:
   ```bash
   createdb shoe_shope
   ```

6. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

7. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```

8. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

## File Structure

```

## API Documentation

Access the API documentation at:
- Swagger UI: `/api/docs/`
- ReDoc: `/api/redoc/`

## API Endpoints

### Authentication
- `POST /api/account/register/`: User registration
- `POST /api/account/login/`: User login

### Products
- `GET /api/catalog/products-list/`: List all products
- `GET /api/catalog/product/<id>/`: Get product details

### Orders
- `GET /api/orders/shopping-cart/`: View shopping cart
- `POST /api/orders/shopping-cart/`: Add to cart
- `GET /api/orders/user/orders/`: List user orders

### Payments
- `POST /api/payments/request/`: Create payment request
- `GET /api/payments/verify/`: Verify payment

## Testing

Run tests with:
```bash
python manage.py test
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

### Additional Notes

- **Environment Variables**: Ensure that sensitive information is stored in the `.env` file and not hardcoded in the codebase.
- **Database Configuration**: Make sure PostgreSQL is properly configured and running.
- **Email Configuration**: Update the email settings in the `.env` file to use your actual email credentials.