# schema.py

CUSTOMERS_SCHEMA = {
    "customer_id": {
        "type": "INT",
        "python_type": int,
        "constraints": ["PRIMARY KEY", "NOT NULL"],
        "description": "Unique ID for each customer",
    },
    "customer_name": {
        "type": "VARCHAR",
        "python_type": str,
        "constraints": ["NOT NULL"],
        "description": "Full name of the customer",
    },
    "customer_email": {
        "type": "VARCHAR",
        "python_type": str,
        "constraints": ["UNIQUE", "NOT NULL"],
        "description": "Unique email address for each customer",
    },
    "customer_address": {
        "type": "VARCHAR",
        "python_type": str,
        "constraints": ["NULLABLE"],
        "description": "Mailing address (synthetic from Faker)",
    },
    "payment_method": {
        "type": "VARCHAR",
        "python_type": str,
        "constraints": ["NOT NULL", "ENUM('Credit','Debit','Paypal')"],
        "description": "Preferred payment method",
    },
}

PRODUCTS_SCHEMA = {
    "product_id": {
        "type": "INT",
        "python_type": int,
        "constraints": ["PRIMARY KEY", "NOT NULL"],
        "description": "Unique ID for each product",
    },
    "product_name": {
        "type": "VARCHAR",
        "python_type": str,
        "constraints": ["NOT NULL"],
        "description": "Name of the product",
    },
    "product_description": {
        "type": "VARCHAR",
        "python_type": str,
        "constraints": ["NOT NULL"],
        "description": "Short description of the product",
    },
}
