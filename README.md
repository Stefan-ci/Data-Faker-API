# Fake Data API with Locale Support

## Overview

This project is a FastAPI-based RESTful API designed to provide fake/generated data for various entities such as users, products, orders, and more. It leverages the [Faker](https://faker.readthedocs.io/en/stable/) library to generate realistic dummy data, which is useful for testing, prototyping, or demo purposes.

The API supports dynamic data generation with customizable parameters such as the number of items to generate and filtering options. Additionally, it incorporates locale settings to generate data in different languages and regional formats.

## Features

- **Users API**: Retrieve lists of fake users with details like name, email, address, and more.
- **Products API**: Generate fake products with attributes including name, category, price, stock, vendor, and images.
- **Orders API**: Manage fake orders composed of products with quantities and totals.
- **Locale Support**: Generate localized data based on user-specified language codes (e.g., `en_US`, `fr_FR`, `it_IT`).
- **On-demand Regeneration**: Endpoints to regenerate data sets dynamically.
- **State Management**: Uses application state to cache and reuse generated data efficiently.

## Usage

- **Locale Selection**  
    The API allows selecting a locale via a query parameter (`locale`) or by sending the `Accept-Language` HTTP header. If no locale is specified, it defaults to `en_US`.  
    Example:
    ```bash
    GET /users/?locale=fr_FR
    ```


- **Data Generation Parameters**  
Most endpoints support query parameters to control the number of items generated (`length`) and filtering criteria (e.g., filter users by city).

## Limitations

- **Partial Multi-locale Support**  
Although the API accepts locale parameters and attempts to generate localized data, it does **not** fully support multi-locale scenarios.  
Specifically, the underlying Faker library's multi-locale mode is known to raise `NotImplementedError` on certain method calls, as some Faker providers do not yet implement full multi-locale compatibility.  
As a result, passing multiple locales or expecting seamless multi-locale fallback behavior **is not operational** and can cause runtime errors.  
For stable operation, only single-locale strings (e.g., `"en_US"`) should be used.

- **No Persistent Storage**  
Data generated is stored temporarily in application state and will reset on application restart. There is no database or persistent storage integration.

- **Limited Image Support**  
Product images are generated via stable URLs to placeholder image services (e.g., Unsplash). No local image files are stored or served.

## Installation

1. Clone the repository:
```bash
git clone THE_CURRENT_REPO_URL_HERE && cd DIRECTORY_ALSO_NAME_HERE
```

2. Install dependencies:

Create you virtual environment, activate it and install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn main:app --reload
```

## Contributing

Contributions are welcome! Please open issues or submit pull requests for bug fixes and feature improvements. Please follow conventional coding practices and document your changes clearly.
