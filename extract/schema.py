# schema.py
from google.cloud import bigquery

schemas = {
    "customers": [
        bigquery.SchemaField("customer_id", "INTEGER", mode="REQUIRED", description="Unique ID for each customer"),
        bigquery.SchemaField("customer_name", "STRING", mode="REQUIRED", description="Full name of the customer"),
        bigquery.SchemaField("customer_email", "STRING", mode="REQUIRED", description="Unique email address for each customer"),
        bigquery.SchemaField("customer_address", "STRING", mode="NULLABLE", description="Mailing address (synthetic from Faker)"),
        bigquery.SchemaField("payment_method", "STRING", mode="REQUIRED", description="Preferred payment method"),
    ],
    "products": [
        bigquery.SchemaField("product_id", "INTEGER", mode="REQUIRED", description="Unique ID for each product"),
        bigquery.SchemaField("product_name", "STRING", mode="REQUIRED", description="Name of the product"),
        bigquery.SchemaField("product_description", "STRING", mode="REQUIRED", description="Short description of the product"),
    ],
    "plans": [
        bigquery.SchemaField("plan_id", "INTEGER", mode="REQUIRED", description="Unique ID for each plan"),
        bigquery.SchemaField("product_id", "INTEGER", mode="REQUIRED", description="ID of the product this plan belongs to"),
        bigquery.SchemaField("plan_name", "STRING", mode="REQUIRED", description="Name of the plan (e.g., Free, Pro, Premium)"),
        bigquery.SchemaField("plan_price", "FLOAT", mode="REQUIRED", description="Price of the plan"),
        bigquery.SchemaField("recurring", "STRING", mode="REQUIRED", description="Billing frequency of the plan"),
    ],
    "subscriptions": [
        bigquery.SchemaField("subscription_id", "INTEGER", mode="REQUIRED", description="Unique ID for each subscription record"),
        bigquery.SchemaField("customer_id", "INTEGER", mode="REQUIRED", description="The customer associated with this subscription"),
        bigquery.SchemaField("plan_id", "INTEGER", mode="REQUIRED", description="The plan this subscription belongs to"),
        bigquery.SchemaField("start_date", "DATE", mode="REQUIRED", description="Date when the subscription started"),
        bigquery.SchemaField("end_date", "DATE", mode="NULLABLE", description="Date when the subscription ended"),
        bigquery.SchemaField("status", "STRING", mode="REQUIRED", description="Current status of the subscription"),
        bigquery.SchemaField("cancel_date", "DATE", mode="NULLABLE", description="Date when the subscription was cancelled"),
    ],
    "discounts": [
        bigquery.SchemaField("discount_id", "INTEGER", mode="REQUIRED", description="Unique ID for each discount or coupon"),
        bigquery.SchemaField("discount_code", "STRING", mode="REQUIRED", description="Code entered by customer to apply discount"),
        bigquery.SchemaField("discount_type", "STRING", mode="REQUIRED", description="Type of discount: percentage or fixed amount"),
        bigquery.SchemaField("discount_value", "FLOAT", mode="REQUIRED", description="Value of the discount (percent or fixed amount)"),
        bigquery.SchemaField("valid_from", "DATE", mode="REQUIRED", description="Start date when discount is valid"),
        bigquery.SchemaField("valid_to", "DATE", mode="REQUIRED", description="End date when discount expires"),
        bigquery.SchemaField("product_id", "INTEGER", mode="NULLABLE", description="Product the discount applies to"),
        bigquery.SchemaField("plan_id", "INTEGER", mode="NULLABLE", description="Plan the discount applies to"),
        bigquery.SchemaField("is_recurring", "BOOLEAN", mode="REQUIRED", description="Whether the discount applies on every billing cycle"),
    ],
    "subscription_discounts": [
        bigquery.SchemaField("sub_discount_id", "INTEGER", mode="REQUIRED", description="Unique ID for each subscription-discount relationship"),
        bigquery.SchemaField("subscription_id", "INTEGER", mode="REQUIRED", description="The subscription this discount is applied to"),
        bigquery.SchemaField("discount_id", "INTEGER", mode="REQUIRED", description="The discount applied to the subscription"),
        bigquery.SchemaField("applied_date", "DATE", mode="REQUIRED", description="Date when discount was applied"),
        bigquery.SchemaField("expiry_date", "DATE", mode="NULLABLE", description="Date when discount expired"),
    ],
    "invoices": [
        bigquery.SchemaField("invoice_id", "INTEGER", mode="REQUIRED", description="Unique invoice ID"),
        bigquery.SchemaField("subscription_id", "INTEGER", mode="REQUIRED", description="The subscription associated with this invoice"),
        bigquery.SchemaField("invoice_date", "DATE", mode="REQUIRED", description="Date of the invoice"),
        bigquery.SchemaField("total_due", "FLOAT", mode="REQUIRED", description="Total amount due for the invoice"),
        bigquery.SchemaField("invoice_status", "STRING", mode="REQUIRED", description="Invoice payment status"),
    ],
    "line_items": [
        bigquery.SchemaField("line_item_id", "INTEGER", mode="REQUIRED", description="Unique line item ID"),
        bigquery.SchemaField("invoice_id", "INTEGER", mode="REQUIRED", description="Invoice associated with this line item"),
        bigquery.SchemaField("plan_id", "INTEGER", mode="NULLABLE", description="Plan ID (NULL for discounts)"),
        bigquery.SchemaField("description", "STRING", mode="REQUIRED", description="Description of the line item"),
        bigquery.SchemaField("amount", "FLOAT", mode="REQUIRED", description="Amount for this line item"),
        bigquery.SchemaField("line_type", "STRING", mode="REQUIRED", description="Type of line item"),
    ],
    "payments": [
        bigquery.SchemaField("payment_id", "INTEGER", mode="REQUIRED", description="Unique payment ID"),
        bigquery.SchemaField("invoice_id", "INTEGER", mode="REQUIRED", description="Invoice associated with the payment"),
        bigquery.SchemaField("payment_date", "DATE", mode="REQUIRED", description="Date of payment attempt"),
        bigquery.SchemaField("amount_paid", "FLOAT", mode="REQUIRED", description="Amount actually paid"),
        bigquery.SchemaField("payment_status", "STRING", mode="REQUIRED", description="payment status"),
        bigquery.SchemaField("payment_method", "STRING", mode="REQUIRED", description="Payment method used"),
    ],
}
