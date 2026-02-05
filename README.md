# Django Product API & Management

A Django-based application acting as a REST API and a simple web interface for managing product data. It includes a management command to sync data from an external API using dynamic authentication.

## Features

-   **Data Synchronization**: Fetches product data from an external API with dynamic credentials (Date/Time based).
-   **REST API**: Endpoints for Products, Categories, and Statuses using Django Rest Framework.
-   **Web UI**: Simple, clean Bootstrap interface for CRUD operations.
-   **Validation**: Server-side validation for product names and prices.
-   **PostgreSQL**: Robust database backend.

## Prerequisites

-   Python 3.10+
-   PostgreSQL
-   Git

## Installation

1.  **Clone the repository** (if applicable) or navigate to the project directory:
    ```bash
    https://github.com/ARSK-11/django
    ```

2.  **Create and Activate Virtual Environment**:
    ```bash
    python -m venv venv
    venv\Scripts\activate  # Windows
    ```

3.  **Install Dependencies**:
    ```bash
    pip install django djangorestframework psycopg2-binary requests
    ```

4.  **Database Configuration**:
    -   Ensure PostgreSQL is running and you have created a database (e.g., `api_product_db`).
    -   Open `api_product/settings.py` and locate the `DATABASES` dictionary (around line 77).
    -   Update the `USER` and `PASSWORD` fields with your PostgreSQL credentials:
        ```python
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': 'api_product_db',
                'USER': 'your_postgres_username',  # e.g., 'postgres'
                'PASSWORD': 'your_postgres_password', # e.g., 'admin123'
                'HOST': 'localhost',
                'PORT': '5432',
            }
        }
        ```

5.  **Run Migrations**:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

## Data Synchronization & Migration

The project includes a custom management command to migrate data from the legacy API to the PostgreSQL database.

### API Configuration
The data source is `https://recruitment.fastprint.co.id/tes/api_tes_programmer`.
Authentication credentials are **generated dynamically** based on the current server time:
-   **Username**: `tesprogrammer` + `ddMMyy` + `C` + `HH` (e.g., `tesprogrammer050226C19`)
-   **Password**: `bisacoding-` + `dd-MM-yy` (MD5 hashed)

### Migration Logic (`products/management/commands/sync_products.py`)
Run the command to start migration:
```bash
python manage.py sync_products
```

**File Location:** `products/management/commands/sync_products.py`

**Process:**
1.  **Auth**: Generates dynamic credentials and authenticates with the external API.
2.  **Fetch**: Retrieves the list of products in JSON format.
3.  **Mapping**:
    -   **Kategori**: Creating new categories if they don't exist. IDs are generated using a hash of the category name since the API doesn't provide them.
    -   **Status**: Creating status entries similarly to categories.
    -   **Produk**: Maps `nama_produk`, `harga`, and links them to the respective `Kategori` and `Status` objects.
4.  **Idempotency**: Uses `update_or_create` to prevent duplicates. Running the command multiple times will update existing records rather than creating new ones.

## Login Credentials

A superuser has been created for administrative access:
-   **Username**: `admin`
-   **Password**: `admin123`

## Running the Application

Start the development server:

```bash
python manage.py runserver
```

Access the application at: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## API Endpoints

You can browse the API directly or use tools like Postman:

-   **Products**: `/api/produk/`
-   **Categories**: `/api/kategori/`
-   **Status**: `/api/status/`

## Project Structure

-   `api_product/`: Main project configuration.
-   `products/`: Main application containing Models, Views, Serializers, and Templates.
-   `products/management/commands/sync_products.py`: Logic for external API synchronization.
