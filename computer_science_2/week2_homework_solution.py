class ProductInfo:
	def __init__(self, stock=0, price=0.00):
		self.stock = stock
		self.price = price

	def __repr__(self):
		# Must return a string
		return f"stock: {self.stock}, price: ${self.price:.2f}"


def check_out_item(item, stock):
	# removes 1 from stock and returns price
	item_info = stock.get(item, None)
	if item_info:
		if item_info.stock > 0:
			item_info.stock -= 1
			return item_info.price
	else:
		print(f"{item} is out of stock")
		return 0




grocery_stock = {	"apple": ProductInfo(30, 0.50),
					"banana": ProductInfo(10, 0.20),
					"cheese": ProductInfo(8, 4.99)}

print("Tina's Grocery Stock")
print(grocery_stock)

grocery_list = ["apple", "apple", "cheese", "banana", "banana", "banana", "orange"]

print("My grocery list")
for i in range(len(grocery_list)):
	print(grocery_list[i])

# Let's add up the cost and check out
print("Checking out")

total_cost = 0.0
for i in grocery_list:
	total_cost += check_out_item(i, grocery_stock)

print(f'Total cost of my list is ${total_cost:.2f}')

print("Tina's Grocery Stock")
print(grocery_stock)