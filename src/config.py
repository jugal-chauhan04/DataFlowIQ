# PROJECT CONFIGURATION FILE

import datetime

# TIMEFRAME FOR DATA GENERATION
START_DATE = "2022-01-01"
END_DATE = "2024-12-31"

# DATASET SIZES
N_CUSTOMERS = 10
N_PLANS = 9 

# RANDOM SEED
SEED = 44

# EMAIL DOMAIN
DOMAIN = "dataflowiq.com"  

# UPGRADE PROBABILITY
UPGRADE_PROBABILITY = 0.40 

# SUBSCRIPTION DISCOUNT START ID
SUB_DISCOUNT_ID = 401

# DATAFLOWIQ PRODUCTS CATALOG 
PRODUCTS = [
    {"product_id": 1, "product_name": "AutomateIQ", "product_description": "Workflow automation tool"},
    {"product_id": 2, "product_name": "TeamCollab", "product_description": "Team collaboration platform"},
    {"product_id": 3, "product_name": "InsightIQ", "product_description": "Business analytics platform"},
]

# PLANS
PLANS = [
    {"plan_id": 101, "product_id": 1, "plan_name": "Free",    "plan_price": 0,    "recurring": "monthly"},
    {"plan_id": 102, "product_id": 1, "plan_name": "Pro",     "plan_price": 100,  "recurring": "monthly"},
    {"plan_id": 103, "product_id": 1, "plan_name": "Premium", "plan_price": 1000, "recurring": "yearly"},
    {"plan_id": 201, "product_id": 2, "plan_name": "Free",    "plan_price": 0,    "recurring": "monthly"},
    {"plan_id": 202, "product_id": 2, "plan_name": "Pro",     "plan_price": 50,   "recurring": "monthly"},
    {"plan_id": 203, "product_id": 2, "plan_name": "Premium", "plan_price": 400,  "recurring": "yearly"},
    {"plan_id": 301, "product_id": 3, "plan_name": "Free",    "plan_price": 0,    "recurring": "monthly"},
    {"plan_id": 302, "product_id": 3, "plan_name": "Pro",     "plan_price": 200,  "recurring": "monthly"},
    {"plan_id": 303, "product_id": 3, "plan_name": "Premium", "plan_price": 2000, "recurring": "yearly"},
]

DISCOUNTS = [
    {
        "discount_id": 1,
        "discount_code": "WELCOME20",
        "discount_type": "percent",   # percent or fixed
        "discount_value": 20,         # 20% off
        "valid_from": datetime(2022, 1, 1),
        "valid_to": datetime(2024, 12, 31),
        "product_id": None,           # None = applies to all products
        "plan_id": None,              # None = applies to all plans
        "is_recurring": False,        # applies only once
    }
]
