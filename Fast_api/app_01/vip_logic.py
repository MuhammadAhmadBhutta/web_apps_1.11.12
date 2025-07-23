# vip_logic.py

import pandas as pd

ORDERS_DF = pd.read_excel("Sample_Superstore.xlsx", sheet_name="Orders")

def compute_vip_score(customer_id: str) -> dict:
    customer_orders = ORDERS_DF[ORDERS_DF['Customer ID'] == customer_id]

    if customer_orders.empty:
        return {"error": "Customer ID not found"}

    total_spend = customer_orders['Sales'].sum()
    num_orders = customer_orders['Order ID'].nunique()
    recency_days = (ORDERS_DF['Order Date'].max() - customer_orders['Order Date'].max()).days

    vip_score = 0
    if total_spend > 5000:
        vip_score += 0.4
    if num_orders > 10:
        vip_score += 0.3
    if recency_days <= 30:
        vip_score += 0.3

    is_vip = vip_score >= 0.5

    customer_name = customer_orders['Customer Name'].iloc[0] if not customer_orders['Customer Name'].empty else "N/A"

    product_names = customer_orders['Product Name'].unique().tolist()

    return {
        "customer_id": customer_id,
        "customer_name": customer_name,
        "products": product_names,
        "total_spend": round(total_spend, 2),
        "num_orders": int(num_orders),
        "recency_days": int(recency_days),
        "vip_score": round(vip_score, 2),
        "is_vip": is_vip
    }
