import pandas as pd
from log.logging_config import setup_logging
from load.load_to_bq import load_to_biquery
from data_generation import (
    generate_customers,
    generate_products,
    generate_plans,
    generate_subscriptions,
    generate_discounts,
    generate_subscription_discounts,
    generate_payments_invoice,
)

def main():
    # 1. Generate base data
    customers = generate_customers(5)
    products = generate_products()
    plans = generate_plans()

    # 2. Generate subscriptions
    subscriptions = generate_subscriptions(customers, plans)

    # 3. Discounts and applied subscription discounts
    discounts = generate_discounts()
    subscription_discounts = generate_subscription_discounts(subscriptions, plans, discounts)

    # 4. Invoices, line items, and payments
    invoices, line_items, payments = generate_payments_invoice(subscriptions, plans, discounts, subscription_discounts)

    # 5. Store results (CSVs)
    customers.to_csv("../data/customers.csv", index=False)
    products.to_csv("../data/products.csv", index=False)
    plans.to_csv("../data/plans.csv", index=False)
    subscriptions.to_csv("../data/subscriptions.csv", index=False)
    discounts.to_csv("../data/discounts.csv", index=False)
    subscription_discounts.to_csv("../data/subscription_discounts.csv", index=False)
    invoices.to_csv("../data/invoices.csv", index=False)
    line_items.to_csv("../data/line_items.csv", index=False)
    payments.to_csv("../data/payments.csv", index=False)

    print("Data generation complete, CSVs saved in /data")

    # 6. Load to Bigquery (Appends data instead of overwriting)
    load_to_biquery(customers, "customers")
    load_to_biquery(products, "products")
    load_to_biquery(plans, "plans")
    load_to_biquery(subscriptions, "subscriptions")
    load_to_biquery(discounts, "discounts")
    load_to_biquery(subscription_discounts, "subscription_discounts")
    load_to_biquery(invoices, "invoices")
    load_to_biquery(line_items, "line_items")
    load_to_biquery(payments, "payments")

    print("Data generation and bigquery load complete")

if __name__ == "__main__":
    main()
