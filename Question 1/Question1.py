import pandas as pd
import numpy as np
from statsmodels.tsa.holtwinters import SimpleExpSmoothing
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Load the data from the first sheet to understand its structure and content
data = pd.read_excel('Question 1 Dataset.xlsx', sheet_name='Sheet1')

# Display the first few rows of the data to explore its structure


""" 1. Is there an data hierarchy present in the shown data. Yes or No. Please justify your answer with reasoning. """

# Validate hierarchy: Check if each "Item-Color" corresponds uniquely to an "Item" and "Color"
hierarchy_check = data.groupby(['Item-Color', 'Item', 'Color']).size().reset_index(name='Counts')

# If each Item-Color corresponds uniquely to an Item and Color, the group size should match the data rows.
hierarchy_valid = len(hierarchy_check) == len(data['Item-Color'].unique())


###Check if Each Color Belongs to Only One Item:
color_to_item = data.groupby('Color')['Item'].nunique()
is_color_nested = (color_to_item <= 1).all()
print("if Each Color Belongs to Only One Item?: " + str(is_color_nested))  # returns False = no hierarchy

# Aggregate sales by Date and Item-Color to check trends
sales_trends = data.groupby(['Dates', 'Item-Color'])['Qty Sold'].sum().reset_index()

hierarchy_valid, sales_trends.head()
print("is there a data hierarchy?: "+ str(hierarchy_valid)+ ", as each 'Item-Color' corresponds uniquely to an 'Item' and 'Color'")


""" 2. Create a forecast based on this data for the upcoming 12months. 
a. Create a bottoms up forecast and provide the reasoning for the same

b. Create a top down forecast and with a target of 10 million."""
# Constants
forecast_periods = 12
total_target_sales = 10000000  # Target for top-down forecast


# Clean and prepare data for forecasting
# Convert "Dates" to datetime and sort
data['Dates'] = pd.to_datetime(data['Dates'])
data = data.sort_values(by='Dates')
sales_trends = data.groupby('Dates')['Qty Sold'].sum().reset_index()
total_sales = sales_trends['Qty Sold']

# Fit a Simple Exponential Smoothing model (no seasonality)
simple_model = SimpleExpSmoothing(total_sales).fit()
trend_forecast = simple_model.forecast(forecast_periods)

forecast_data = data.pivot(index='Dates', columns='Item-Color', values='Qty Sold').fillna(0)

# Bottom-Up Forecast (No Seasonality)
bottom_up_forecasts = {}

for item_color in forecast_data.columns:
    series = forecast_data[item_color]
    if series.sum() > 0:  # Forecast only if there is historical data
        model = SimpleExpSmoothing(series).fit()
        bottom_up_forecasts[item_color] = round(model.forecast(forecast_periods))
    else:
        bottom_up_forecasts[item_color] = [0] * forecast_periods

# Combination of Bottom-Up Forecasts
bottom_up_forecast_df = pd.DataFrame(bottom_up_forecasts, 
                                     index=pd.date_range(start=forecast_data.index[-1] + pd.DateOffset(months=1), 
                                                         periods=forecast_periods, freq='MS'))
bottom_up_total_forecast = bottom_up_forecast_df.sum(axis=1)
print (bottom_up_forecast_df)
print (bottom_up_total_forecast)


# Top-Down Forecast
# Calculate historical contribution of each Item-Color
item_color_contributions = forecast_data.sum() / forecast_data.sum().sum()

# Distribute total target sales across Item-Colors proportionally
top_down_monthly_total = total_target_sales / forecast_periods
top_down_forecast_df = pd.DataFrame({item_color: round(top_down_monthly_total * proportion,0)
                                     for item_color, proportion in item_color_contributions.items()}, 
                                    index=pd.date_range(start=forecast_data.index[-1] + pd.DateOffset(months=1), 
                                                        periods=forecast_periods, freq='MS'))


top_down_forecast_df


""" 3. In case we have to evaluate in Dec-2024 effectiveness of the forecast, how would you do it and why? 
Use the forecast created in (subsection 2) and any actuals for December to show the evaluation. """


# Example actuals of december 2024 as actuals for December 2025 
sales_trends = data.groupby(['Dates', 'Item-Color'])['Qty Sold'].sum().reset_index()

actuals_dec = sales_trends[
    (sales_trends['Dates'] == '2024-12-01')
][['Item-Color', 'Qty Sold']]

# Set index and convert to dictionary for easy lookup
actuals_dec = actuals_dec.set_index('Item-Color')['Qty Sold'].to_dict()

# Extract forecasted values for December 2025
forecast_dec = bottom_up_forecast_df.loc[bottom_up_forecast_df.index[-1]]

# Align forecast with actuals: Only include items with actuals
forecast_dec_aligned = forecast_dec[forecast_dec.index.isin(actuals_dec.keys())]
actuals_aligned = np.array([actuals_dec[item] for item in forecast_dec_aligned.index])

# Calculate error metrics
forecasts = forecast_dec_aligned.values
mae = mean_absolute_error(actuals_aligned, forecasts)
mape = np.mean(np.abs((actuals_aligned - forecasts) / actuals_aligned)) * 100
rmse = np.sqrt(mean_squared_error(actuals_aligned, forecasts))

# Print results
print(f"MAE: {mae}")
print(f"MAPE: {mape}%")
print(f"RMSE: {rmse}")


""" 4. If the PLC of items were 12 months and on 01st July, 2024, all the Item-Color combinations have 
inventory of 10 units remaining. Based on the forecast created in (subsection 2), what would be the planned order recommendation? """


# Constants
current_inventory = 10
lead_time_days = 14  # 2 weeks
dos_days = 28
days_in_month = 30  # Approximate average

# Filtering of forecasts for the remaining PLC period
bottom_up_remaining2 = bottom_up_forecast_df.loc['2025-07-01':'2025-11-30']
top_down_remaining2 = top_down_forecast_df.loc['2025-07-01':'2025-11-30']

# Calculation of remaining demand for each Item-Color
bottom_up_demand = bottom_up_remaining2.sum(axis=0)
top_down_demand = top_down_remaining2.sum(axis=0)

# Calculation of daily demand for each Item-Color (using the first month's forecast as an approximation)
daily_demand_bottom_up = bottom_up_remaining2.iloc[0] / days_in_month
daily_demand_top_down = top_down_remaining2.iloc[0] / days_in_month

# Safety stock and lead time adjustments
safety_stock_bottom_up = daily_demand_bottom_up * dos_days
lead_time_stock_bottom_up = daily_demand_bottom_up * lead_time_days

safety_stock_top_down = daily_demand_top_down * dos_days
lead_time_stock_top_down = daily_demand_top_down * lead_time_days

# Planned orders
bottom_up_orders = round(np.maximum(bottom_up_demand + safety_stock_bottom_up + lead_time_stock_bottom_up - current_inventory, 0),0)
top_down_orders = round(np.maximum(top_down_demand + safety_stock_top_down + lead_time_stock_top_down - current_inventory, 0),0)

# Combine results into a DataFrame
planned_orders_df = pd.DataFrame({
    'Item-Color': bottom_up_demand.index,
    'Planned Orders (Bottom-Up)': bottom_up_orders,
    'Planned Orders (Top-Down)': top_down_orders,
    'Planned Orders per month (Bottom-Up)': round(bottom_up_orders/5,0),
    'Planned Orders per month (Top-Down)': round(top_down_orders/5,0)
}).reset_index(drop=True)
print(planned_orders_df)



""" 5. We have an inventory of 100 units on an item, we have 3 customers requesting for the demand of this. 
Consider that there was no forecast on this item and the inventory was available due to a cancellation. 
How would you allocate the inventory. 

a. Demand 1: Wholesale demand from Norway, biggest market of ABC company of 80 units.

b. Demand 2: DTC demand of 60 units.

c. Demand 3: Wholesale demand of strategic account of 50 units."""


print(""" Given the inventory of 100 units and the demands from three customers, the allocation should consider business priorities 
      and demand fairnesszes.
1.Business Priorities. The allocation should align with business objectives.
      Priority 1: Wholesale Demand from Strategic Accounts (Demand 3): Strategic accounts are vital for long-term growth, so ensuring their demands are met is critical.
      Priority 2: Wholesale Demand from Norway (Demand 1): Norway is the biggest market for ABC, and fulfilling its demand helps maintain market dominance.
      Priority 3: DTC Demand (Demand 2): Direct-to-Customer (DTC) is important but secondary in this scenario, as wholesale clients drive larger volumes.
2. Allocation Rules. The allocation should:
Prioritize Strategic Importance: Allocate to the Strategic Account (Demand 3) first, up to their requested 50 units.
Fairly Distribute Remaining Inventory: After satisfying the strategic account, allocate the remaining inventory proportionally 
between Norway (Demand 1) and DTC (Demand 2) based on their request sizes.""")

