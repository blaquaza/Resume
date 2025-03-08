# cafe.py

# Step 1: Create a list called menu

menu = ["coffee", "tea", "sandwich", "cake"]

# Step 2: Create a dictionary called stock

stock = {
    "coffee": 20,
    "tea": 25,
    "sandwich": 10,
    "cake": 5
}

# Step 3: Create a dictionary called price
price = {
    "coffee": 2.5,
    "tea": 1.5,
    "sandwich": 4.0,
    "cake": 3.0
}

# Step 4: Calculate the total worth of the stock

total_stock = 0
for item in menu:
    item_value = stock[item] * price[item]  # Calculate the value of each item in stock
    total_stock += item_value  # Add the item value to the total stock value

# Step 5: Print the result of the calculation
print(f"The total worth of the stock in the café is: ${total_stock:.2f}")