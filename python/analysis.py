import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. LOAD DATA
# ==========================================

customers = pd.read_csv("Customers.csv")
orders = pd.read_csv("Orders.csv")
products = pd.read_csv("Products.csv")
payments = pd.read_csv("Payments.csv")

# ==========================================
# 2. CLEAN COLUMN NAMES
# ==========================================

customers.columns = customers.columns.str.strip()
orders.columns = orders.columns.str.strip()
products.columns = products.columns.str.strip()
payments.columns = payments.columns.str.strip()

# ==========================================
# 3. REMOVE EMPTY PAYMENT COLUMNS
# ==========================================

payments = payments.drop(
    columns=['Unnamed: 8', 'Unnamed: 9', 'Unnamed: 10',
             'Unnamed: 11', 'Unnamed: 12'],
    errors='ignore'
)

# ==========================================
# 4. MERGE ORDERS + CUSTOMERS
# ==========================================

data = orders.merge(
    customers,
    on="Customer_ID",
    how="left"
)

# ==========================================
# 5. MERGE WITH PRODUCTS
# ==========================================

data = data.merge(
    products,
    on=["Product_ID", "Product_Name"],
    how="left",
    suffixes=("", "_Product")
)

# ==========================================
# 6. MERGE WITH PAYMENTS
# ==========================================

data = data.merge(
    payments,
    on="Order_ID",
    how="left",
    suffixes=("", "_Payment")
)

# ==========================================
# 7. CHECK FINAL DATA
# ==========================================

print("\n================================")
print("DATA MERGED SUCCESSFULLY")
print("================================")

print("Rows:", data.shape[0])
print("Columns:", data.shape[1])

print("\nFinal Columns:")
print(data.columns.tolist())

print("\nFirst 5 Rows:")
print(data.head())

# ==========================================
 # MAIN BUSINESS KPIs
# ==========================================



print("\n========================================")
print("       E-COMMERCE BUSINESS KPIs")
print("========================================")

# Total Revenue
total_revenue = data["Total_Amount"].sum()

# Total Orders
total_orders = data["Order_ID"].nunique()

# Total Customers
total_customers = data["Customer_ID"].nunique()

# Total Quantity Sold
total_quantity = data["Quantity (nos.)"].sum()

# # Average Order Value
average_order_value  = total_revenue / total_orders

# Total Discount
total_discount = data["Discount_Amount"].sum()

# Total tax
total_tax = data["Tax_Amount"].sum()

# # Total Shipping Charges
total_shipping = data["Shipping_Charge"].sum()

# Total Profit
total_profit = (
    (data["Selling_Price"] - data["Cost_Price"])
    * data["Quantity (nos.)"]
).sum()

# Print results

print(f"Total Revenue       : ₹{total_revenue:,.2f}")
print(f"Total Orders        : {total_orders:,}")
print(f"Total Customers     : {total_customers:,}")
print(f"Total Quantity Sold : {total_quantity:,.0f}")
print(f"Average Order Value : ₹{average_order_value:,.2f}")
print(f"Total Discount : ₹{float(total_discount):,.2f}")
print(f"Total Tax      : ₹{float(total_tax):,.2f}")
print(f"Total Shipping : ₹{float(total_shipping):,.2f}")

print("========================================")

# ==========================================
# STEP 4: MONTHLY SALES ANALYSIS
# =========================================

# Convert Order_Date into proper date format
data["Order_Date"] = pd.to_datetime(
    data["Order_Date"],
    unit="D",
    origin="1899-12-30"
)
# Create Month column
data["Month"] = data["Order_Date"].dt.to_period("M")

# Calculate Month Sales
monthly_sales = data.groupby("Month")["Total_Amount"].sum()

# # Calculate monthly orders
monthly_orders = data.groupby("Month")["Order_ID"].nunique()

# Calculate monthly quantity
monthly_quantity = data.groupby("Month")["Quantity (nos.)"].sum()

# ==========================================
# DISPLAY MONTHLY RESULTS
# ==========================================

print("\n========================================")
print("          MONTHLY SALES ANALYSIS")
print("=======================================")

print("\nMonthly Sales:")
print(monthly_sales)

print("\nMonthly Orders:")
print(monthly_orders)

print("\nMonthly Quantity Sold:")
print(monthly_quantity)

# ==========================================
# MONTHLY SALES CHART
# ==========================================

plt.figure(figsize=(12, 5))

monthly_sales.plot(kind="line", marker="o")

plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales (₹)")
plt.xticks(rotation=45)
plt.grid(True)

plt.tight_layout()
plt.show()

# ==========================================
# STEP 5: CATEGORY ANALYSIS
# ==========================================

# Sales by Category

category_sales = data.groupby("Category")["Total_Amount"].sum()

# Quantity sold by category
category_quantity = data.groupby("Category")["Quantity (nos.)"].sum()

# Number of orders by Category
category_orders = data.groupby("Category")["Order_ID"].nunique()

# ==========================================
# DISPLAY CATEGORY RESULTS
# ==========================================


print("\n========================================")
print("           CATEGORY ANALYSIS")
print("========================================")

print("\nSales by Category:")
print(category_sales.sort_values(ascending=False))

print("\nQuantity Sold by Category:")
print(category_quantity.sort_values(ascending=False))

print("\nOrder by Category:")
print(category_orders.sort_values(ascending=False))

# ==========================================
# CATEGORY SALES CHART
# ==========================================

plt.figure(figsize=(10,6))

category_sales.sort_values(ascending=False).plot(
    kind="bar"
)

plt.title("Sales by Product Category")
plt.xlabel("Category")
plt.ylabel("Sales (₹)")
plt.xticks(rotation=45)
plt.grid(axis="y")

plt.tight_layout()
plt.show()



# ==========================================
# STEP 6: TOP 10 PRODUCTS ANALYSIS
# ==========================================

# Calculate total sales for each product
product_sales = data.groupby("Product_Name")["Total_Amount"].sum()

# Calculate total quantity sold for each product
product_quantity = data.groupby("Product_Name")["Quantity (nos.)"].sum()

# Get Top 10 products by revenue
top_10_products = product_sales.sort_values(
    ascending=False
    ).head(10)

# Get Top 10 products by quantity sold
top_10_quantity = product_quantity.sort_values(
    ascending=False
    ).head(10)


# ==========================================
# DISPLAY RESULTS
# ==========================================

print("\n========================================")
print("          TOP 10 PRODUCTS")
print("========================================")

print("\nTop 10 Products by Revenue:")
print(top_10_products)

print("\nTop Products by Quantity Sold:")
print(top_10_quantity)

# ==========================================
# TOP 10 PRODUCTS CHART
# ==========================================

plt.figure(figsize=(12, 6))

top_10_products.plot(kind="bar")

plt.title("Top 10 Products by Revenue")
plt.xlabel("Product")
plt.ylabel("Revenue (₹)")
plt.xticks(rotation=45)
plt.grid(axis="y")

plt.tight_layout()
plt.show()

# ==========================================
# STEP 7: CUSTOMER BEHAVIOUR ANALYSIS
# ==========================================

# Total spending by each customer
customer_spending = data.groupby(
    "Customer_ID"
)["Total_Amount"].sum()

# Number of orders by each customer
customer_orders = data.groupby(
    "Customer_ID"
)["Order_ID"].nunique()

# Quantity purchased by each customer
customer_quantity = data.groupby(
    "Customer_ID"
)["Quantity (nos.)"].sum()


# ==========================================
# TOP 10 CUSTOMERS BY SPENDING
# ==========================================

top_10_customers = customer_spending.sort_values(
    ascending=False
).head(10)


# ==========================================
# DISPLAY CUSTOMER RESULTS
# ==========================================

print("\n========================================")
print("       CUSTOMER BEHAVIOUR ANALYSIS")
print("========================================")

print("\nTop 10 Customers by Spending:")
print(top_10_customers)


# ==========================================
# ORDERS PER CUSTOMER
# ==========================================

print("\nOrders per Customer:")
print(customer_orders.describe())


# ==========================================
# QUANTITY PURCHASED PER CUSTOMER
# ==========================================

print("\nQuantity Purchased per Customer:")
print(customer_quantity.describe())

print("\nNumber of customer quantity records:")
print(len(customer_quantity))

print("\nSample Customer Quantity:")
print(customer_quantity.head(10))


# ==========================================
# MEMBERSHIP ANALYSIS
# ==========================================

membership_sales = data.groupby(
    "Membership_label"
)["Total_Amount"].sum()

print("\nSales by Membership:")
print(membership_sales)


# ==========================================
# TOP 10 CUSTOMERS CHART
# ==========================================

plt.figure(figsize=(12, 6))

top_10_customers.plot(kind="bar")

plt.title("Top 10 Customers by Spending")
plt.xlabel("Customer ID")
plt.ylabel("Total Spending (₹)")
plt.xticks(rotation=45)
plt.grid(axis="y")

plt.tight_layout()
plt.show()


# ==========================================
# STEP 8: PAYMENT & ORDER ANALYSIS
# ==========================================

# Orders by payment method
payment_methods = data.groupby("Payment_Mode")["Order_ID"].nunique()

# Orders by Payment Status
payment_status = data.groupby("Payment_Status")["Order_ID"].nunique()

# Orders by Order status
order_status = data.groupby("Order_Status")["Order_ID"].nunique()

# Total Revenue Amount
total_refund = (
    data["Refund_Amount"]
    .astype(str)
    .str.replace("₹", "", regex=False)
    .str.replace(",", "", regex=False)
    .str.replace("-", "0", regex=False)
    .str.strip()
    .astype(float)
    .sum()
)

# ==========================================
# DISPLAY RESULTS
# ==========================================

print("\n========================================")
print("       PAYMENT & ORDER ANALYSIS")
print("========================================")

print("\nOrders by Payment Method:")
print(payment_methods)

print("\nOrders by Payment Status:")
print(payment_status)

print("\nOrders by Order Status:")
print(order_status)

print(f"\nTotal Refund Amount: ₹{total_refund:,.2f}")

print("\nRefund Amount Sample:")
print(data["Refund_Amount"].head(20))

print("\nRefund Amount Data Type:")
print(data["Refund_Amount"].dtype)

# ==========================================
# PAYMENT METHOD CHART
# ==========================================

plt.figure(figsize=(10, 6))

payment_methods.plot(kind="bar")

plt.title("Orders by Payment Method")
plt.xlabel("Payment Method")
plt.ylabel("Number of Orders")
plt.xticks(rotation=45)
plt.grid(axis="y")

plt.tight_layout()
plt.show()

# ==========================================
# STEP 9: REVENUE & PROFIT ANALYSIS
# ==========================================

# Calculate profit for each order

data["Profit"] = (
    (data["Selling_Price"] - data["Cost_Price"])
    * data["Quantity (nos.)"]
    )

# Total profit

total_profit = data["Profit"].sum()

# Profit by category
category_profit = data.groupby("Category")["Profit"].sum()

# Revenue by category
category_revenue = data.groupby("Category")["Total_Amount"].sum()

# Profit margin
profit_margin = (total_profit / total_revenue) * 100


# ==========================================
# DISPLAY RESULTS
# ==========================================

print("\n========================================")
print("        REVENUE & PROFIT ANALYSIS")
print("========================================")

print(f"\nTotal Revenue : ₹{total_revenue:,.2f}")
print(f"Total Profit : ₹{total_profit: ,.2f}")
print(f"Profit Margin :{profit_margin:2f}%")

print("\nProfit by Category:")
print(category_profit)

print("\nRevenue by Category:")
print(category_revenue)


# ==========================================
# MOST PROFITABLE CATEGORY
# ==========================================

most_profitable_category = category_profit.idxmax()

print(
      f"\nMost Profitable Category:"
      f"{most_profitable_category}"
      )

# ==========================================
# PROFIT BY CATEGORY CHART
# ==========================================

plt.figure(figsize=(10, 6))


category_profit.sort_values(ascending=False).plot(kind="bar")

plt.title("Profit by Product Category")
plt.xlabel("Category")
plt.ylabel("Profit (₹)")
plt.xticks(rotation=45)
plt.grid(axis="y")

plt.tight_layout()
plt.show()

# ==========================================
# STEP 10: FINAL VISUALIZATIONS
# ==========================================



# ==========================================
# 1. MONTHLY SALES TREND
# ==========================================

plt.figure(figsize=(12, 6))

monthly_sales.plot(
    kind="line",
    marker="o"
)

plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Revenue (₹)")
plt.xticks(rotation=45)
plt.grid(True)

plt.tight_layout()
plt.show()


# ==========================================
# 2. SALES BY CATEGORY
# ==========================================

plt.figure(figsize=(10,6))

category_sales.sort_values(ascending=False).plot(
    kind="bar"
    )

plt.title("Sales by Product Category")
plt.xlabel("Category")
plt.ylabel("Revenue (₹)")
plt.xticks(rotation=45)
plt.grid(axis="y")

plt.tight_layout()
plt.show()

# ==========================================
# 3. TOP 10 PRODUCTS
# ==========================================

plt.figure(figsize=(12, 6))

top_10_products.sort_values(ascending=True).plot(
    kind="barh"
    )

plt.title("Top 10 products by Revenue")
plt.xlabel("Revenue(₹)")
plt.ylabel("Product")

plt.tight_layout()
plt.show()



# ==========================================
# 4. TOP 10 CUSTOMERS
# ==========================================

plt.figure(figsize=(12, 6))

top_10_customers.sort_values(ascending=True).plot(
    kind="barh"
)

plt.title("Top 10 Customers by Spending")
plt.xlabel("Total Spending (₹)")
plt.ylabel("Customer ID")

plt.tight_layout()
plt.show()


# ==========================================
# 5. PAYMENT METHODS
# ==========================================

plt.figure(figsize=(10, 6))

payment_methods.plot(kind="bar")

plt.title("Orders by Payment Method")
plt.xlabel("Payment Method")
plt.ylabel("Number of Orders")
plt.xticks(rotation=45)
plt.grid(axis="y")

plt.tight_layout()
plt.show()



# ==========================================
# 6. ORDER STATUS
# ==========================================

plt.figure(figsize=(8, 6))

order_status.plot(kind="bar")


plt.title("Order Status Distribution")
plt.xlabel("Order Status")
plt.ylabel("Number of Orders")
plt.xticks(rotation=0)
plt.grid(axis="y")

plt.tight_layout()
plt.show()


# ==========================================
# 7. PROFIT BY CATEGORY
# ==========================================

plt.figure(figsize=(10, 6))

category_profit.sort_values(ascending=False).plot(
    kind="bar"
)

plt.title("Profit by Product Category")
plt.xlabel("Category")
plt.ylabel("Profit (₹)")
plt.xticks(rotation=45)
plt.grid(axis="y")

plt.tight_layout()
plt.show()


print("\n========================================")
print("       FINAL VISUALIZATIONS COMPLETE")
print("========================================")

# ==========================================
# STEP 11.1: EXPORT DATA FOR POWER BI
# ==========================================

data.to_csv("ecommerce_final_data.csv", index=False)

print("\nData exported successfully for Power BI!")
