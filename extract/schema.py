# schema.py

customers_schema = {
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

products_schema = {
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

plans_schema = {
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

subscriptions_schema = {
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

discounts_schema = {
    "discount_id": {
        "type": "INT",
        "python_type": int,
        "constraints": ["PRIMARY KEY", "NOT NULL"],
        "description": "Unique ID for each discount or coupon",
    },
    "discount_code": {
        "type": "VARCHAR",
        "python_type": str,
        "constraints": ["UNIQUE", "NOT NULL"],
        "description": "Code entered by customer to apply discount",
    },
    "discount_type": {
        "type": "VARCHAR",
        "python_type": str,
        "constraints": ["NOT NULL", "ENUM('percent','fixed')"],
        "description": "Type of discount: percentage or fixed amount",
    },
    "discount_value": {
        "type": "DECIMAL(10,2)",
        "python_type": float,
        "constraints": ["NOT NULL"],
        "description": "Value of the discount (percent or fixed amount)",
    },
    "valid_from": {
        "type": "DATE",
        "python_type": "datetime.date",
        "constraints": ["NOT NULL"],
        "description": "Start date when discount is valid",
    },
    "valid_to": {
        "type": "DATE",
        "python_type": "datetime.date",
        "constraints": ["NOT NULL"],
        "description": "End date when discount expires",
    },
    "product_id": {
        "type": "INT",
        "python_type": int,
        "constraints": ["FOREIGN KEY REFERENCES products(product_id)", "NULLABLE"],
        "description": "Product the discount applies to (NULL = all products)",
    },
    "plan_id": {
        "type": "INT",
        "python_type": int,
        "constraints": ["FOREIGN KEY REFERENCES plans(plan_id)", "NULLABLE"],
        "description": "Plan the discount applies to (NULL = all plans)",
    },
    "is_recurring": {
        "type": "BOOLEAN",
        "python_type": bool,
        "constraints": ["NOT NULL"],
        "description": "Whether the discount applies on every billing cycle",
    },
}

subscription_discounts_schema = {
    "sub_discount_id": {
        "type": "INT",
        "python_type": int,
        "constraints": ["PRIMARY KEY", "NOT NULL"],
        "description": "Unique ID for each subscription-discount relationship",
    },
    "subscription_id": {
        "type": "INT",
        "python_type": int,
        "constraints": ["FOREIGN KEY REFERENCES subscriptions(subscription_id)", "NOT NULL"],
        "description": "The subscription this discount is applied to",
    },
    "discount_id": {
        "type": "INT",
        "python_type": int,
        "constraints": ["FOREIGN KEY REFERENCES discounts(discount_id)", "NOT NULL"],
        "description": "The discount applied to the subscription",
    },
    "applied_date": {
        "type": "DATE",
        "python_type": "datetime.date",
        "constraints": ["NOT NULL"],
        "description": "Date when discount was applied (usually subscription start date)",
    },
    "expiry_date": {
        "type": "DATE",
        "python_type": "datetime.date",
        "constraints": ["NULLABLE"],
        "description": "Date when discount expired (usually subscription end date)",
    },
}

invoices_schema = {
    "invoice_id": {
        "type": "INT", 
        "python_type": int, 
        "constraints": ["PRIMARY KEY", "NOT NULL"], 
        "description": "Unique invoice ID"
    },
    "subscription_id": {
        "type": "INT", 
        "python_type": int, 
        "constraints": ["FOREIGN KEY REFERENCES subscriptions(subscription_id)", "NOT NULL"],
        "description": "The subscription associated with this invoice"
    },
    "invoice_date": {
        "type": "DATE", 
        "python_type": "datetime.date",
        "constraints": ["NOT NULL"],
        "description": "Date of the invoice"
    },
    "total_due": {
        "type": "DECIMAL(10,2)",
        "python_type": float,
        "constraints": ["NOT NULL"],
        "description": "Total amount due for the invoice"
    },
    "invoice_status": {
        "type": "VARCHAR",
        "python_type": str,
        "constraints": ["NOT NULL", "ENUM('paid','pending')"],
        "description": "Invoice payment status"
    },
}

line_items_schema = {
    "line_item_id": {
        "type": "INT",
        "python_type": int,
        "constraints": ["PRIMARY KEY", "NOT NULL"],
        "description": "Unique line item ID"
    },
    "invoice_id": {
        "type": "INT",
        "python_type": int,
        "constraints": ["FOREIGN KEY REFERENCES invoices(invoice_id)", "NOT NULL"],
        "description": "Invoice associated with this line item"
    },
    "plan_id": {
        "type": "INT",
        "python_type": int,
        "constraints": ["FOREIGN KEY REFERENCES plans(plan_id)", "NULLABLE"],
        "description": "Plan ID (NULL for discounts)"
    },
    "description": {
        "type": "VARCHAR",
        "python_type": str,
        "constraints": ["NOT NULL"],
        "description": "Description of the line item"
    },
    "amount": {
        "type": "DECIMAL(10,2)",
        "python_type": float,
        "constraints": ["NOT NULL"],
        "description": "Amount for this line item (negative for discounts)"
    },
    "line_type": {
        "type": "VARCHAR",
        "python_type": str,
        "constraints": ["NOT NULL", "ENUM('charge','discount')"],
        "description": "Type of line item"
    },
}

payments_schema = {
    "payment_id": {
        "type": "INT",
        "python_type": int,
        "constraints": ["PRIMARY KEY", "NOT NULL"],
        "description": "Unique payment ID"
    },
    "invoice_id": {
        "type": "INT",
        "python_type": int,
        "constraints": ["FOREIGN KEY REFERENCES invoices(invoice_id)", "NOT NULL"],
        "description": "Invoice associated with the payment"
    },
    "payment_date": {
        "type": "DATE",
        "python_type": "datetime.date",
        "constraints": ["NOT NULL"],
        "description": "Date of payment attempt"
    },
    "amount_paid": {
        "type": "DECIMAL(10,2)",
        "python_type": float,
        "constraints": ["NOT NULL"],
        "description": "Amount actually paid"
    },
    "payment_status": {
        "type": "VARCHAR",
        "python_type": str,
        "constraints": ["NOT NULL", "ENUM('success','failed')"],
        "description": "Payment status"
    },
    "payment_method": {
        "type": "VARCHAR",
        "python_type": str,
        "constraints": ["NOT NULL", "ENUM('Credit','Debit','Paypal','N/A')"],
        "description": "Payment method used"
    },
}


