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

PLANS_SCHEMA = {
    "plan_id": {
        "type": "INT",
        "python_type": int,
        "constraints": ["PRIMARY KEY", "NOT NULL"],
        "description": "Unique ID for each plan",
    },
    "product_id": {
        "type": "INT",
        "python_type": int,
        "constraints": ["FOREIGN KEY REFERENCES products(product_id)", "NOT NULL"],
        "description": "ID of the product this plan belongs to",
    },
    "plan_name": {
        "type": "VARCHAR",
        "python_type": str,
        "constraints": ["NOT NULL"],
        "description": "Name of the plan (e.g., Free, Pro, Premium)",
    },
    "plan_price": {
        "type": "DECIMAL(10,2)",
        "python_type": float,
        "constraints": ["NOT NULL"],
        "description": "Price of the plan",
    },
    "recurring": {
        "type": "VARCHAR",
        "python_type": str,
        "constraints": ["NOT NULL", "ENUM('monthly','yearly')"],
        "description": "Billing frequency of the plan",
    },
}

SUBSCRIPTIONS_SCHEMA = {
    "subscription_id": {
        "type": "INT",
        "python_type": int,
        "constraints": ["PRIMARY KEY", "NOT NULL"],
        "description": "Unique ID for each subscription record",
    },
    "customer_id": {
        "type": "INT",
        "python_type": int,
        "constraints": ["FOREIGN KEY REFERENCES customers(customer_id)", "NOT NULL"],
        "description": "The customer associated with this subscription",
    },
    "plan_id": {
        "type": "INT",
        "python_type": int,
        "constraints": ["FOREIGN KEY REFERENCES plans(plan_id)", "NOT NULL"],
        "description": "The plan this subscription belongs to",
    },
    "start_date": {
        "type": "DATE",
        "python_type": "datetime.date",
        "constraints": ["NOT NULL"],
        "description": "Date when the subscription started",
    },
    "end_date": {
        "type": "DATE",
        "python_type": "datetime.date",
        "constraints": ["NULLABLE"],
        "description": "Date when the subscription ended (if cancelled or switched)",
    },
    "status": {
        "type": "VARCHAR",
        "python_type": str,
        "constraints": ["NOT NULL", "ENUM('active','cancelled')"],
        "description": "Current status of the subscription",
    },
    "cancel_date": {
        "type": "DATE",
        "python_type": "datetime.date",
        "constraints": ["NULLABLE"],
        "description": "Date when the subscription was cancelled (if applicable)",
    },
}

