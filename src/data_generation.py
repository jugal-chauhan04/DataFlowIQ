import re 
import numpy as np 
import pandas as pd 
import random
from datetime import timedelta
from faker import Faker 
from config import START_DATE, END_DATE, N_CUSTOMERS, N_PLANS, SEED, DOMAIN, PRODUCTS, PLANS, UPGRADE_PROBABILITY, DISCOUNTS

fake = Faker()

def generate_email(name: str, domain: str, existing: set) -> str:

    """
    Generate a unique email address from a person's name.
    Ensure uniqueness by appending a counter if needed.
    """ 
    base = re.sub(r'[^a-z]','', name.lower())
    email = f"{base}@{domain}"
    counter = 1

    while email in existing:
        email = f"{base}{counter}@{domain}"
        counter += 1

    existing.add(email)
    return email 

def generate_customer(n: int = N_CUSTOMERS, domain: str = DOMAIN) -> pd.DataFrame:
    """
    Generate a synthetic dataset of customer name, email, address, and payment method

    Args:
        n(int): Number of customers to generate.
        domain(str): domain name for email address.
    
    Returns:
        pd.DataFrame: DataFrame with customer information.
    """
    seen_emails = set()

    names = [fake.name() for _ in range(n)]
    emails = [generate_email(name, domain, seen_emails) for name in names]
    addresses = [fake.address().replace("\n", ",") for _ in range(n)]
    payment_methods = np.random.choice(
        ["Credit", "Debit", "Paypal"], size = n, p = [0.5, 0.3, 0.2]
        )
    customers = pd.DataFrame({
        "customer_id": range(1, n + 1),
        "customer_name": names,
        "customer_email": emails,
        "customer_address": addresses,
        "payment_method": payment_methods
    }
    )

    return customers

def generate_products(products: list = None) -> pd.DataFrame:
    """
    Generate a synthetic dataset of products.

    Args:
        products (list, optional): List of product dictionaries with keys 
                                   'product_id', 'product_name', 'product_description'.
                                   If None, defaults to PRODUCTS from config.py.

    Returns:
        pd.DataFrame: DataFrame with product information.
    """
    if products is None:
        products = PRODUCTS

    return pd.DataFrame(products)

def generate_plans() -> pd.DataFrame:


    """
    Return the static list of subscription plans as a DataFrame.

    Plans are defined in config.py to keep business logic separate
    from generation logic.
    
    Returns:
        pd.DataFrame: DataFrame with plan information.
    """
    return pd.DataFrame(PLANS)

def generate_subscription_row(sub_id, customer_id, plan, start_date, status=None):
    """
    Generate a single subscription record.
    """
    if status is None:
        status = random.choice(["active", "cancelled"])
    
    end_date = None if status == "active" else start_date + timedelta(days=random.randint(60, 720))
    if end_date and end_date > END_DATE:
        end_date = END_DATE
    
    cancel_date = end_date if status == "cancelled" else None
    
    return [
        sub_id,
        customer_id,
        plan.plan_id,
        start_date,
        end_date,
        status,
        cancel_date,
    ]


def choose_new_plan(current_plan, plans):
    """
    Given a current plan, choose a new plan for upgrade/downgrade.
    """
    if "Pro" in current_plan.plan_name:
        # Upgrade PRO -> PREMIUM
        return plans[
            (plans["plan_name"].str.contains("Premium"))
            & (plans["product_id"] == current_plan.product_id)
        ].sample(1).iloc[0]
    
    elif "Premium" in current_plan.plan_name:
        # Downgrade PREMIUM -> PRO
        return plans[
            (plans["plan_name"].str.contains("Pro"))
            & (plans["product_id"] == current_plan.product_id)
        ].sample(1).iloc[0]
    
    elif "Free" in current_plan.plan_name:
        # Upgrade FREE -> PRO or PREMIUM
        return plans[
            (plans["plan_name"].str.contains("Pro|Premium"))
            & (plans["product_id"] == current_plan.product_id)
        ].sample(1).iloc[0]
    
    return None


def generate_subscriptions(customers, plans):

    """
    Generate subscription records for each customer.

    Args:
        customers (pd.DataFrame): Customers dataset
        plans (pd.DataFrame): Plans dataset

    Returns:
        pd.DataFrame: Subscriptions dataset
    """
    subscriptions = []
    sub_id = 101
    
    for _, c in customers.iterrows():
        # Assign initial plan + subscription row
        plan = plans.sample(1).iloc[0]
        start_date = START_DATE + timedelta(days=random.randint(0, (END_DATE - START_DATE).days))
        row = generate_subscription_row(sub_id, c.customer_id, plan, start_date)
        subscriptions.append(row)
        sub_id += 1
        
        # Decide if customer switches plans
        if random.random() < UPGRADE_PROBABILITY:
            switch_date = start_date + timedelta(days=random.randint(60, 720))
            if switch_date > END_DATE:
                switch_date = END_DATE
            
            # Close old subscription
            subscriptions[-1][4] = switch_date   # update end_date
            subscriptions[-1][5] = "cancelled"   # update status
            subscriptions[-1][6] = switch_date   # update cancel_date
            
            # Choose new plan
            new_plan = choose_new_plan(plan, plans)
            if new_plan is not None:
                new_row = generate_subscription_row(sub_id, c.customer_id, new_plan, switch_date)
                subscriptions.append(new_row)
                sub_id += 1
    
    return pd.DataFrame(
        subscriptions,
        columns=[
            "subscription_id",
            "customer_id",
            "plan_id",
            "start_date",
            "end_date",
            "status",
            "cancel_date",
        ],
    )

def generate_discounts() -> pd.DataFrame:
    """
    Return the static list of discounts as a DataFrame.

    Discounts are defined in config.py to keep data generation flexible.
    
    Returns:
        pd.DataFrame: DataFrame with discount information.
    """
    return pd.DataFrame(DISCOUNTS)