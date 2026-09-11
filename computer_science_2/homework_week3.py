# We're assuming that these are all ordered and correspond with eachother
# i.e. that books[i] is written by authors[i] and checked out by borrower_names[i]
library_books = []
authors = []
book_statuses = [] # True for available, False for checked out
borrower_names = []

def add_book(title, author):
	library_books.append(title)
	authors.append(author)
	book_statuses.append(True)
	borrower_names.append(None)
	print(f"Added: {title} by {author}")

def _search_for_book(title):
	index = -1
	for idx, name in enumerate(library_books):
		if name == title:
			index = idx
	return index

def checkout_book(title, borrower):
	index = _search_for_book(title)
	if index == -1:
		print(f'{title} is not in this library system')
		return
	if book_statuses[index]:
		book_statuses[index] = False
		borrower_names[index] = borrower
		print(f'{title} was successfully checked out by {borrower}')
	else:
		print(f'{title} is already checked out by {borrower_names[index]}')


def return_book(title):
	index = _search_for_book(title)
	if index == -1:
		print(f'{title} is not in this library system')
		return
	if not book_statuses[index]:
		borrower = borrower_names[index]
		book_statuses[index] = True
		borrower_names[index] = None
		print(f'Book {title} returned by {borrower}')
	else:
		print(f'Book {title} was not checked out')



def display_library():
	print("\n")
	print("--- Library Inventory ---")
	for i in range(len(library_books)):
		status = "Available" if book_statuses[i] else f"Checked out by {borrower_names[i]}"
		print(f"{i}: {library_books[i]} by {authors[i]} - {status}")
	print("\n")



if __name__ == '__main__':
	
	add_book("1984", "George Orwell")
	add_book("One Hundred Years of Solitude", "Gabriel García Márquez")
	add_book("Of Mice and Men", "John Steinbeck")
	add_book("Giovanni's Room", "James Baldwin")
	add_book("The Labyrinth of Solitude", "Octavio Paz")
	add_book("The Catcher in the Rye", "J.D. Salinger")
	add_book("To Kill a Mockingbird", "Harper Lee")
	add_book("The Hobbit", "J.R.R. Tolkien")
	add_book("The Price of Salt", "Patricia Highsmith")
	add_book("Moby-Dick", "Herman Melville")
	add_book("Pedro Páramo", "Juan Rulfo")
	add_book("Frankenstein", "Mary Shelley")
	add_book("The Picture of Dorian Gray", "Oscar Wilde")
	add_book("Like Water for Chocolate", "Laura Esquivel")
	add_book("Beloved", "Toni Morrison")
	add_book("The Color Purple", "Alice Walker")

	display_library()
	checkout_book("The Price of Salt", "Jorge")
	checkout_book("Moby-Dick", "Jessica")
	checkout_book("Beloved", "Ramu")

	display_library()
	return_book("Beloved")
	return_book("1984")

	display_library()
