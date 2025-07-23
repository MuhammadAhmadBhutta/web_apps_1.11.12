import pandas as pd

# Load your dataset
orders_df = pd.read_excel('data/Sample_Superstore.xlsx', sheet_name='Orders')

def get_recommendations(customer_id):
    customer_id = customer_id.strip()
    if customer_id == "":
        return [{"Product Name": "No Customer ID provided."}]

    user_products = orders_df[orders_df['Customer ID'] == customer_id]['Product Name'].unique()
    if len(user_products) == 0:
        return [{"Product Name": "No purchases found for this Customer ID."}]
    
    similar_customers = orders_df[
        (orders_df['Product Name'].isin(user_products)) &
        (orders_df['Customer ID'] != customer_id)
    ]['Customer ID'].unique()

    if len(similar_customers) == 0:
        return [{"Product Name": "No similar customers found."}]
    
    recommended_products = orders_df[
        orders_df['Customer ID'].isin(similar_customers)
    ]
    recommended_products = recommended_products[
        ~recommended_products['Product Name'].isin(user_products)
    ]

    top_products = (
        recommended_products.groupby(['Product Name', 'Category', 'Sub-Category'])
        .size()
        .reset_index(name='count')
        .sort_values('count', ascending=False)
        .head(5)
    )

    if top_products.empty:
        return [{"Product Name": "No new products to recommend."}]
    
    return top_products[['Product Name', 'Category', 'Sub-Category']].to_dict(orient='records')
