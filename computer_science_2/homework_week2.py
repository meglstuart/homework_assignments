class ProductInfo:
	stock = 0
	price = 0.0
	
	def __repr__(self):
		# Must return a string
		return f"stock: {self.stock}, price: ${self.price:.2f}"


new_product_info = ProductInfo()

grocery_stock = {	"apple": new_product_info,
					"banana": new_product_info,
					"cheese": new_product_info}

grocery_stock["apple"].stock = 30
grocery_stock["apple"].price = 0.50

grocery_stock["banana"].stock = 10
grocery_stock["banana"].price = 0.20

grocery_stock["cheese"].stock = 8
grocery_stock["cheese"].price = 4.99

print("Tina's Grocery Stock")
print(grocery_stock)

grocery_list = ["apple", "apple", "cheese", "banana", "banana", "banana", "orange"]

print("My grocery list")
for i in range(10):
	print(grocery_list[i])

# Let's add up the cost
total_cost = 0.0

info = grocery_stock[grocery_list[0]]
if info.stock == 0:
	print (f"{grocery_list[0]} is out of stock")
else: total_cost += info.price

info = grocery_stock[grocery_list[1]]
if info.stock == 0:
	print (f"{grocery_list[1]} is out of stock")
else: total_cost += info.price

info = grocery_stock[grocery_list[2]]
if info.stock == 0:
	print (f"{grocery_list[2]} is out of stock")
else: total_cost += info.price

info = grocery_stock[grocery_list[3]]
if info.stock == 0:
	print (f"{grocery_list[3]} is out of stock")
else: total_cost += info.price

info = grocery_stock[grocery_list[4]]
if info.stock == 0:
	print (f"{grocery_list[4]} is out of stock")
else: total_cost += info.price

info = grocery_stock[grocery_list[5]]
if info.stock == 0:
	print (f"{grocery_list[5]} is out of stock")
else: total_cost += info.price

info = grocery_stock[grocery_list[6]]
if info.stock == 0:
	print (f"{grocery_list[6]} is out of stock")
else: total_cost += info.price

print(f'Total cost of my list is {total_cost:.2f}')

#now let's check out

grocery_stock[grocery_list[0]].stock -= 1
grocery_stock[grocery_list[1]].stock -= 1
grocery_stock[grocery_list[2]].stock -= 1
grocery_stock[grocery_list[3]].stock -= 1
grocery_stock[grocery_list[4]].stock -= 1
grocery_stock[grocery_list[5]].stock -= 1
grocery_stock[grocery_list[6]].stock -= 1

print("Tina's Grocery Stock")
print(grocery_stock)
