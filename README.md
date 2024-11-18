# ASICS Case study


## Dependencies
Python version: 3.11.7


## Instruction
To run EACH python script
Install modules: `pip install -r requirements.txt`
Run the script: `python Question1.py` or `python Question2.py`

## Description
#### Question 1.py:
Answers for case study:
Let’s consider we are in the first week of June-2025 for a company called ABC, attached below is the time series data of a few item which we have sold in the past 6 months, keep in mind that all the items were introduced for the first time in Dec-2024, the Product life cycle of the items are 6 months. Perform an data exploration to understand the situation better and help how to deal with the below suggestions. 
All the items have a leadtime of 2 weeks and currently we have 28 DOS. 
1.	Is there an data hierarchy present in the shown data. Yes or No. Please justify your answer with reasoning. 
2.	Create a forecast based on this data for the upcoming 12months. 
a.	Create a bottoms up forecast and provide the reasoning for the same.
b.	Create a top down forecast and with a target of 10 million.
3.	In case we have to evaluate in Dec-2025 effectiveness of the forecast, how would you do it and why? Use the forecast created in (subsection 2) and any actuals for December to show the evaluation. 
4.	If the PLC of items were 12 months and on 01st July, 2025, all the Item-Color combinations have inventory of 10 units remaining. Based on the forecast created in (subsection 2), what would be the planned order recommendation?
5.	We have an inventory of 100 units on an item, we have 3 customers requesting for the demand of this. Consider that there was no forecast on this item and the inventory was available due to a cancellation. How would you allocate the inventory. 
a.	Demand 1: Wholesale demand from Norway, biggest market of ABC company of 80 units. 
b.	Demand 2: DTC demand of 60 units. 
c.	Demand 3: Wholesale demand of strategic account of 50 units.



#### Question2.py:
These two datasets represent a mock example of ASICS own purchasing data.
The sample provides a subsets of Purchase Requests, Purchase Orders and Item Masterdata.

Purchase requisition is basically a formal request to buy a material. This is represented by the field [No].
Purchase order is a legal authorised document created by the buyer for purchasing material. This is represnted by the field [Order number]

The (mock) Item Masterdata presents article name, price information and selling channel detail.

Using the coding language/technique of your choice answer the following questions:

1. Amount of Oustanding Qty per Article per Month
2. How many Purchase Orders were deleted
3. How many Purchase Orders could be for e-Com
4.Summarise the Total Ecom Order Value.

Additionall insights.




