import re 
import numpy as np 
import pandas as pd 
from faker import Faker 
from config import START_DATE, END_DATE, N_CUSTOMERS, N_PLANS, SEED, DOMAIN, PRODUCTS

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
