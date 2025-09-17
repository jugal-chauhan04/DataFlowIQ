# Designing DataFlowIQ Schema  

DataFlowIQ is a fictional SaaS company that provides a cloud-based productivity suite for small and mid-sized businesses. Its core mission is to help teams automate workflows, analyze performance, and collaborate effectively. They have three products:  

1. AutomateIQ - Lets users connects apps (Slack, Gmail, Hubspot, Salesforce, etc.) and automate repetitive tasks.
2. TeamCollab - A project management and team collaboration hub.
3. InsightIQ - Provides dashboards, data connectors, and reports for sales, marketing, and finance teams.  

All three products have three subscription tiers - Free, Pro, and Premium

### I am tasked to create a centralized, scalable, and accurate data model that tracks revenue KPIs MRR and ARR and interactive dashboard that reflect organization's financial health.

In this project, I am going to follow a typical payment billing schema for a SaaS organization, and start with 10 randomly generated entries as row values and scale the dataset to test the durability and reliability of my data model.  

The end-to-end flow of billing occurs as followed:  

1. A customer subscribes to a plan (which belongs to a product).
2. The subscription produces recurring invoices each billing cycle.
3. Each invoice is broken into invoice_line_items (charges, discounts, taxes).
4. Payments track whether those invoices were successfully collected.
5. Discounts are defined globally and applied at the subscription level through subscription_discount.
6. Active discounts show up on invoices as negative invoice_line_items, lowering the net total due.  

And the schema is design is as shown below:  

## Customers Table

| Column Name      | Data Type (SQL) | Data Type (Python) | Constraints                  | Description                              |
|------------------|-----------------|--------------------|------------------------------|------------------------------------------|
| customer_id      | INT             | int                | Primary Key, NOT NULL        | Unique ID for each customer              |
| customer_name    | VARCHAR         | str                | NOT NULL                     | Full name of the customer                |
| customer_email   | VARCHAR         | str                | UNIQUE, NOT NULL             | Unique email address for each customer   |
| customer_address | VARCHAR         | str                | NULLABLE                     | Mailing address (synthetic from Faker)   |
| payment_method   | VARCHAR         | str (categorical)  | NOT NULL, ENUM (Credit/Debit/Paypal) | Preferred payment method                 |

## Products Table

| Column Name        | Data Type (SQL) | Data Type (Python) | Constraints           | Description                        |
|--------------------|-----------------|--------------------|-----------------------|------------------------------------|
| product_id         | INT             | int                | PRIMARY KEY, NOT NULL | Unique ID for each product         |
| product_name       | VARCHAR         | str                | NOT NULL              | Name of the product                |
| product_description| VARCHAR         | str                | NOT NULL              | Short description of the product   |

