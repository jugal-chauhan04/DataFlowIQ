# Synthetic SaaS billing dataset for analytics & dbt pipelines  

When I started practicing SaaS metrics (MRR, churn, ARPU, etc.) and data modeling, I quickly realized there’s a lack of publicly available datasets, since real SaaS billing data is sensitive and rarely shared. This project is my attempt to simulate a **realistic SaaS billing system** in python - from customers signing up, upgrading/downgrading, applying discounts, getting invoiced, and making (or failing) payments. Hence making it possible to:  

- Practice building **dbt pipelines** (e.g., MRR, churn, ARPU)
- Create **interactive dashboards** (Power BI, Tableau, Looker)
- Stress test data models by scaling from **10 customers → 100k customers**  

---

## What it does  

Generates a **linked dataset** across customers, products, plans, subscriptions, discounts, invoices, line items, and payments. The end-to-end flow of billing occurs as followed:  

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

---

# About DataFlowIQ

DataFlowIQ is a fictional SaaS company that provides a cloud-based productivity suite for small and mid-sized businesses. Its core mission is to help teams automate workflows, analyze performance, and collaborate effectively. They have three products:  

1. AutomateIQ - Lets users connects apps (Slack, Gmail, Hubspot, Salesforce, etc.) and automate repetitive tasks.
2. TeamCollab - A project management and team collaboration hub.
3. InsightIQ - Provides dashboards, data connectors, and reports for sales, marketing, and finance teams.  

All three products have three subscription tiers - Free, Pro, and Premium.  

---

## Schema Design

[The Schema Design is show here](data/schema.md)  

---  

## How to use  

1. Clone the repo  
2. From the `src/` folder, run:
   ```bash
   python main.py  
3. CSV files will be generated inside /data/
4. Edit config.py to scale up the dataset or change behaviours  

---  

## Current Configuration  

At the current configuration, the dataset includes:
- **10 customers.**
- **3 products.**
- **9 subscription plans** (Free, Pro, Premium across 3 products).
- **~15–20 subscriptions** (with upgrades/downgrades).
- **Discounts applied** to ~50% of subscriptions.
- **Hundreds of invoices, line items, and payments** depending on subscription length and billing cycles.  

This basic config will allow me to build a dbt pipeline and define metrics like MRR. Then, once that’s stable, I’ll scale it up (10k+ customers, 100k+ invoices) to test the durability and performance of my data models and dashboards.  

---

## Key Highlights
- **Customer lifecycle simulation** → Customers subscribe to plans with randomized start dates, active/cancelled statuses, and end dates.  
- **Plan upgrades & downgrades** → ~40% of customers switch between plans (Free → Pro/Premium, Pro ↔ Premium).  
- **Discount engine** → Discounts (recurring or one-time) are applied dynamically to subscriptions, with rules for expiry and recurrence.  
- **Invoice generation** → Invoices are created for each billing cycle (monthly or yearly) until subscription ends.  
- **Line items** → Each invoice includes base plan charges, plus applied discount items when relevant.  
- **Payments** → Simulated payments for each invoice, with configurable failure probability (e.g., 30% fail, 70% success).  
- **Config-driven** → Dates, upgrade probabilities, and failure rates are controlled in `config.py` for easy tuning.  
- **Relational schema** → All tables are linked via foreign keys (e.g., customers → subscriptions → invoices → payments).  

---  

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

---



