# Fake Data API with Locale Support

## Overview

This project is a FastAPI-based RESTful API designed to provide fake/generated data for various entities such as users, products, orders, and more. It leverages the [Faker](https://faker.readthedocs.io/en/stable/) library to generate realistic dummy data, which is highly useful for testing, prototyping, or demonstration purposes.

The API supports dynamic data generation with customizable parameters (like the number of items) and filtering options. Additionally, it incorporates locale settings to generate data in different languages and regional formats.

## Key Features

* **Users API**: Retrieve lists of fake users with details like name, email, address, and more.
* **Products API**: Generate fake products with attributes including name, category, price, stock, vendor, and images.
* **Orders API**: Manage fake orders composed of products with quantities and totals.
* An much more (e.g., **cryptos**, **expenses**, **incomes**, etc.).
* **Locale Support**: Generate localized data by specifying a language code (e.g., `en_US`, `fr_FR`, `it_IT`). The `locale` query parameter or the `Accept-Language` HTTP header can be used. The default locale is `en_US`.
* **On-demand Regeneration**: Dedicated API endpoints (`/regenerate` with `?length=integer`) allow dynamic refreshing of data sets.
* **Efficient State Management**: Generated data is temporarily stored in the application's in-memory state for quick access and reuse.
* **Filtering and Pagination**: Most list endpoints support query parameters for filtering (`?field=value`) and pagination (`?page=1&page_size=50`).

## Usage

The API is accessible via standard HTTP requests.

**Examples:**

* **List users in French:**
    ```bash
    GET /users/?locale=fr_FR
    ```
* **List 10 products:**
    ```bash
    GET /products/?length=10
    ```
* **List users filtered by city (example):**
    ```bash
    GET /users/?city=Paris
    ```
* **Regenerate all user data (requires a POST request):**
    ```bash
    POST /users/regenerate?length=500
    ```

Interactive API documentation (Swagger UI & ReDoc) is available at `http://localhost:8000/docs` or `http://localhost:8000/redoc`once the application is running.

## Limitations

* **Locale Support: Single Mode Only**
    The API is designed to generate data for a **single locale** at a time. While the `locale` parameter is supported, using multiple locales simultaneously or expecting multi-locale "fallback" behavior (where Faker would try different locales) is **not functional** and may lead to `NotImplementedError` due to limitations in certain Faker providers regarding multi-locale compatibility.
    Always use a **single locale string** (e.g., `"fr_FR"`, `"en_US"`) for stable operation (if locale support is enabled).

* **No Persistent Storage**
    All generated data is stored in memory within the application state. It will be **reset upon each application restart**. There is no integration with a database or other persistent storage mechanism.

* **Limited Image Support**
    Product images are generated via stable URLs from placeholder image services (e.g., Unsplash, Lorem Picsum). The API does not store or serve image files.

## Installation

To set up and run the project locally:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Stefan-ci/Data-Faker-API
    cd Data-Faker-API
    ```

2.  **Install dependencies:**
    Create and activate a virtual environment, then install the necessary dependencies:
    ```bash
    python -m venv venv
    # On Windows:
    # venv\Scripts\activate
    # On macOS/Linux:
    # source venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Run the application:**
    ```bash
    uvicorn main:app --reload
    ```
    The API will be accessible at `http://localhost:8000`. The `--reload` flag allows for automatic code changes detection. You may also specify the port with `--port PORT_NUMBER_HERE`.

## Contributing

Contributions are welcome! Please feel free to open issues for bug reports or feature suggestions, or submit pull requests. Kindly adhere to conventional coding practices and document your changes clearly.
