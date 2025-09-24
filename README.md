# Synthetic SaaS billing dataset for analytics & dbt pipelines  

When I started practicing SaaS metrics (MRR, churn, ARPU, etc.) and data modeling, I quickly realized there’s a lack of publicly available datasets, since real SaaS billing data is sensitive and rarely shared. This project is my attempt to simulate a **realistic SaaS billing system** in python - from customers signing up, upgrading/downgrading, applying discounts, getting invoiced, and making (or failing) payments. Hence making it possible to:  

- Practice building **dbt pipelines** (e.g., MRR, churn, ARPU)
- Create **interactive dashboards** (Power BI, Tableau, Looker)
- Stress test data models by scaling from **15 customers → 100k customers**  


## What it does  

Generates a **linked dataset** across customers, products, plans, subscriptions, discounts, invoices, line items, and payments and loads it into Google BigQuery. The end-to-end flow of billing occurs as followed:  

1. A customer subscribes to a plan (which belongs to a product).
2. The subscription produces recurring invoices each billing cycle.
3. Each invoice is broken into invoice_line_items (charges, discounts).
4. Payments track whether those invoices were successfully collected.
5. Discounts are defined globally and applied at the subscription level through subscription_discount.
6. Active discounts show up on invoices as negative invoice_line_items, lowering the net total due.   

Simulates **real SaaS behaviors**:  
  - Plan upgrades/downgrades
  - Recurring vs one-time discounts
  - Payment successes/failures (configurable probabilities)  

Config-driven, easy to adjust:  
  - Number of customers
  - Pricing and plans
  - Discount rules
  - Payment failure rates  


# About SRC Analytics

SRC Analytics is a fictional SaaS company that provides a cloud-based productivity suite for small and mid-sized businesses. Its core mission is to help teams automate workflows, analyze performance, and collaborate effectively. They have three products:  

1. AutomateSRC - Lets users connects apps (Slack, Gmail, Hubspot, Salesforce, etc.) and automate repetitive tasks.
2. CollabSRC - A project management and team collaboration hub.
3. InsightSRC - Provides dashboards, data connectors, and reports for sales, marketing, and finance teams.  

All three products have three subscription tiers - Free, Pro, and Premium.  


## Schema Design

[The Schema Design is show here](data/schema.md)  

### Current Setup  

At the current configuration, the BigQuery dataset includes:  
- **15 customers**
- **3 products**
- **9 subscription plans** (Free, Pro, Premium across 3 products)
- **~15–20 subscriptions** (with upgrades/downgrades)
- **Discounts applied** to ~50% of subscriptions  

This prototype dataset will be used to build **dbt models** that define SaaS metrics such as **MRR, ARR, churn, and ARPU**.  
These models will feed into **reporting dashboards** (Power BI / Looker) for validation and exploration.  

Static tables (`products`, `plans`, `discounts`) remain unchanged unless manually updated in `config.py`.  
Transactional tables (`customers`, `subscriptions`, `invoices`, etc.) are append-only, ensuring historical records remain intact.  


### Future Setup
- Once end-to-end analytics are in place, the project will be scaled to simulate **ongoing data growth**:  
  - Each weekly run will append *n new customers* and related records.  
  - The dataset will expand incrementally, enabling longitudinal analysis.  
- The full pipeline will then be evaluated across all stages:  
  - **Ingestion pipeline** (data generation & load performance).  
  - **dbt models** (scalability and maintainability).  
  - **Metric definitions** (accuracy, validity checks).  
  - **Dashboard performance** (refresh speed and reliability).  
- Over time, this will evolve into a **production-style dataset** that demonstrates scalable, reliable analytics workflows.  

## Key Highlights
- **Customer lifecycle simulation** → Customers subscribe to plans with randomized start dates, active/cancelled statuses, and end dates.  
- **Plan upgrades & downgrades** → ~40% of customers switch between plans (Free → Pro/Premium, Pro ↔ Premium).  
- **Discount engine** → Discounts (recurring or one-time) are applied dynamically to subscriptions, with rules for expiry and recurrence.  
- **Invoice generation** → Invoices are created for each billing cycle (monthly or yearly) until subscription ends.  
- **Line items** → Each invoice includes base plan charges, plus applied discount items when relevant.  
- **Payments** → Simulated payments for each invoice, with configurable failure probability (e.g., 30% fail, 70% success).  
- **Config-driven** → Dates, upgrade probabilities, and failure rates are controlled in `config.py` for easy tuning.  
- **Relational schema** → All tables are linked via foreign keys (e.g., customers → subscriptions → invoices → payments).  
  

## Limitations and Future Enhancements  

This project currently simplifies some aspects of SaaS billing.
Planned enhancements include:  

- Trial mechanics (e.g., 14-day trials, trial-to-paid conversions).  
- Plan catalog evolution (launch/retire plans dynamically, grandfathering old customers).  
- Richer payments (retries, refunds, chargebacks).  
- Proration for mid-cycle plan changes.  
- Multi-currency and tax support. 
- Usage-based billing models.  
- Revenue recognition (invoiced vs recognized revenue).  

## Ending Note  

This project grew out of the need for a realistic SaaS billing dataset to practice metrics definition and data modeling. It’s small by design today, but fully scalable and I’ll keep expanding it to make it more realistic and useful for SaaS analytics.  