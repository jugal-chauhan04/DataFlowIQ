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

## Plans Table

| Column Name | Data Type (SQL) | Data Type (Python) | Constraints                                           | Description                               |
|-------------|-----------------|--------------------|-------------------------------------------------------|-------------------------------------------|
| plan_id     | INT             | int                | PRIMARY KEY, NOT NULL                                 | Unique ID for each plan                   |
| product_id  | INT             | int                | FOREIGN KEY REFERENCES products(product_id), NOT NULL | ID of the product this plan belongs to    |
| plan_name   | VARCHAR         | str                | NOT NULL                                              | Name of the plan (Free, Pro, Premium)     |
| plan_price  | DECIMAL(10,2)   | float              | NOT NULL                                              | Price of the plan                         |
| recurring   | VARCHAR         | str                | NOT NULL, ENUM('monthly','yearly')                    | Billing frequency of the plan             |

## Subscriptions Table

| Column Name     | Data Type (SQL) | Data Type (Python)  | Constraints                                                   | Description                                        |
|-----------------|-----------------|---------------------|---------------------------------------------------------------|----------------------------------------------------|
| subscription_id | INT             | int                 | PRIMARY KEY, NOT NULL                                         | Unique ID for each subscription record             |
| customer_id     | INT             | int                 | FOREIGN KEY REFERENCES customers(customer_id), NOT NULL        | The customer associated with this subscription     |
| plan_id         | INT             | int                 | FOREIGN KEY REFERENCES plans(plan_id), NOT NULL                | The plan this subscription belongs to              |
| start_date      | DATE            | datetime.date       | NOT NULL                                                      | Date when the subscription started                 |
| end_date        | DATE            | datetime.date       | NULLABLE                                                      | Date when the subscription ended (if cancelled or switched) |
| status          | VARCHAR         | str                 | NOT NULL, ENUM('active','cancelled')                          | Current status of the subscription                 |
| cancel_date     | DATE            | datetime.date       | NULLABLE                                                      | Date when the subscription was cancelled (if applicable) |

## Discounts Table

| Column Name   | Data Type (SQL) | Data Type (Python) | Constraints                                                   | Description                                          |
|---------------|-----------------|--------------------|---------------------------------------------------------------|------------------------------------------------------|
| discount_id   | INT             | int                | PRIMARY KEY, NOT NULL                                         | Unique ID for each discount or coupon                |
| discount_code | VARCHAR         | str                | UNIQUE, NOT NULL                                              | Code entered by customer to apply discount           |
| discount_type | VARCHAR         | str                | NOT NULL, ENUM('percent','fixed')                             | Type of discount: percentage or fixed amount         |
| discount_value| DECIMAL(10,2)   | float              | NOT NULL                                                      | Value of the discount (percent or fixed amount)      |
| valid_from    | DATE            | datetime.date      | NOT NULL                                                      | Start date when discount is valid                    |
| valid_to      | DATE            | datetime.date      | NOT NULL                                                      | End date when discount expires                       |
| product_id    | INT             | int                | FOREIGN KEY REFERENCES products(product_id), NULLABLE          | Product the discount applies to (NULL = all products)|
| plan_id       | INT             | int                | FOREIGN KEY REFERENCES plans(plan_id), NULLABLE                | Plan the discount applies to (NULL = all plans)      |
| is_recurring  | BOOLEAN         | bool               | NOT NULL                                                      | Whether the discount applies on every billing cycle  |

## Subscription_Discounts Table

| Column Name             | Data Type (SQL) | Data Type (Python) | Constraints                                                               | Description                                                 |
|--------------------------|-----------------|--------------------|---------------------------------------------------------------------------|-------------------------------------------------------------|
| sub_discount_id | INT             | int                | PRIMARY KEY, NOT NULL                                                     | Unique ID for each subscription-discount relationship       |
| subscription_id          | INT             | int                | FOREIGN KEY REFERENCES subscriptions(subscription_id), NOT NULL           | The subscription this discount is applied to                |
| discount_id              | INT             | int                | FOREIGN KEY REFERENCES discounts(discount_id), NOT NULL                   | The discount applied to the subscription                    |
| applied_date             | DATE            | datetime.date      | NOT NULL                                                                  | Date when discount was applied (usually subscription start) |
| expiry_date              | DATE            | datetime.date      | NULLABLE                                                                  | Date when discount expired (usually subscription end date)  |
