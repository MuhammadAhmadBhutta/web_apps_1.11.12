from .data_loader import load_data

def forecast_demand():
    df = load_data()
    total_sales = df['Sales'].sum()
    total_profit = df['Profit'].sum()
    return {
        "total_sales": round(total_sales, 2),
        "total_profit": round(total_profit, 2)
    }
