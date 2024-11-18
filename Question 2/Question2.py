"""
These two datasets represent a mock example of ASICS own purchasing data. The sample provides a subsets of Purchase Requests, Purchase Orders and Item Masterdata.

Purchase requisition is basically a formal request to buy a material. This is represented by the field [No]. Purchase order is a legal authorised document created by the buyer for purchasing material. This is represnted by the field [Order number]

The (mock) Item Masterdata presents article name, price information and selling channel detail.

Using the coding language/technique of your choice answer the following questions:

Amount of Oustanding Qty per Article per Month
How many Purchase Orders were deleted
How many Purchase Orders could be for e-Com 4.Summarise the Total Ecom Order Value.

Additionally, provide an insight of your choice.

Selection deleted
"""

import pandas as pd
# Load the data
file_path = 'Question 2. Data Analyst Business Case.xlsx'
data1 = pd.read_excel(file_path, sheet_name='Data1')
data2 = pd.read_excel(file_path, sheet_name='Data2')
# Ensure column names are correctly formatted and match
data1.rename(columns=lambda x: x.strip(), inplace=True)

# Ensure the merging keys are of consistent type
data1['ItemNo'] = data1['ItemNo'].astype(str)
data2['article_id'] = data2['article_id'].astype(str)

# Merge data1 and data2
ecom_merge = pd.merge(data1, data2, left_on='ItemNo', right_on='article_id', how='inner')
ecom_merge = ecom_merge[(ecom_merge['DelFlag'] != 'L')]

# conver prices in euro to usd 

exchange_rate_to_usd = 1.1  # Example rate for EUR to USD
ecom_merge['Price USD'] = ecom_merge.apply(
    lambda row: row['price'] * exchange_rate_to_usd if row['Currency Code'] == 'EUR' else row['price'], axis=1)


# Step 1: Calculate Outstanding Quantity per Article per Month
data1['PoL_Timestamp'] = pd.to_datetime(data1['PoL_Timestamp'], format='%Y%m%d%H%M%S')
data1['Month'] = data1['PoL_Timestamp'].dt.to_period('M').dt.to_timestamp()

outstanding_qty_per_month = data1.groupby(['ItemNo', 'Month'])['Outstanding Quantity'].sum().reset_index()
outstanding_qty_per_month.rename(columns={'ItemNo': 'Article', 'Outstanding Quantity': 'Total Outstanding Qty'}, inplace=True)

# Step 2: Count the number of deleted purchase orders
deleted_po_count = data1[data1['DelFlag'] == 'L']['Order number'].nunique()

# Step 3: Count the number of e-Commerce Purchase Orders, not deleted
ecom_po_count = ecom_merge[(ecom_merge['sellable_online'] == True)]['Order number'].nunique()

# Step 4: Calculate Total e-Commerce Order Value
if 'Quantity' in ecom_merge.columns:
    ecom_merge['TotalValue'] = ecom_merge['Quantity'] * ecom_merge['Price USD']
    ecom_total_value = ecom_merge['TotalValue'].sum()
else:
    ecom_total_value = None


# Summary of results

results = {
    'Deleted Purchase Orders Count': deleted_po_count,
    'e-Commerce Purchase Orders Count': ecom_po_count,
    'Total e-Commerce Order Value': ecom_total_value
}
print('Amount of Oustanding Qty per Article per Month')
print(outstanding_qty_per_month[(outstanding_qty_per_month['Total Outstanding Qty'] > 0)])
print(results)


# Other insights

# Merging Data1 and Data2
df = pd.merge(data1, data2, left_on='ItemNo', right_on='article_id', how='left')

# Remove deleted orders
df =df[(df['DelFlag'] != 'L')]

exchange_rate_to_usd = 1.1  # Example rate for EUR to USD


# 1. Spending Analysis
df['TotalValue_usd'] = df['Quantity'] * df.apply(
    lambda row: row['price'] * exchange_rate_to_usd if row['Currency Code'] == 'EUR' else row['price'], axis=1)
total_spending = df['TotalValue_usd'].sum()
average_spending = df['TotalValue_usd'].mean()
spending_distribution = df['TotalValue_usd'].describe()

# 2. Item Insights
most_purchased_items = (
    df['name']
    .value_counts()
    .head(10)
    .reset_index()
    .rename(columns={'index': 'Item Name', 'name': 'TotalValue_usd'})
)

# Packaging insights into results
spending_insights = {
    "Total Spending (USD)": total_spending,
    "Average Spending per Item (USD)": average_spending,
    "Spending Distribution": spending_distribution.to_dict(),
}
print(spending_insights)

# 3. Channel Performance
sellable_online = df[ (df['sellable_online'] == True)]
sellable_online_sum = sellable_online['TotalValue_usd'].sum()
sellable_online_count = df['sellable_online'].sum()
total_items = df['TotalValue_usd'].sum()
sellable_online_percentage = (sellable_online_sum / total_items) * 100



channel_performance = {
    "Total Items Sellable Online": sellable_online_count,
    "Percentage of Items Sellable Online": sellable_online_percentage,
    "Total Spending on Online-Sellable Items (USD)": sellable_online_sum,
}

print(channel_performance)
