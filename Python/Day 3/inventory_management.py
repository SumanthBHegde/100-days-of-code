#An Inventory Management System

class Item:
    #starting ID for items
    item_counter = 1000
    
    def __init__(self, name, price, quantity):
        Item.item_counter += 1
        self.item_id = Item.item_counter
        self.name = name
        self.price = price
        self.quantity = quantity
        
    def update_price(self, new_price):
        if new_price > 0:
            self.price = new_price
            print(f"Price updated to : {self.price}")
        else:
            print("Invalid price. Price must to be greater than 0")
    
    def update_quantity(self, new_quantity):
        if new_quantity >= 0:
            self.price = new_quantity
            print(f"Quantity updated to : {self.quantity}")
        else:
            print("Invalid quantity. Quantity must to be a positive number")
        
    def __str__(self):
        return f"ID: {self.item_id}, Name: {self.name}, Price: {self.price}, Quantity: {self.quantity}"

class Inventory:
    def __init__(self):
        self.items = {}
    
    def add_item(self, name, price, quantity):
        if price <= 0 or quantity < 0:
            print("Invalid Price or Quantity. Price must to be greater than 0 and quantity must to be a positive number")
            return
        item = Item(name, price, quantity)
        self.items[item.item_id] = item
        print(f"Item added successfully with Item ID : {item.item_id}")
        
    def update_item_price(self, item_id, new_price):
        item = self.get_item_by_id(item_id)
        if item:
            item.update_price(new_price)
        else:
            print("Item not found")
            
    def update_item_quantity(self, item_id, new_quantity):
        item = self.get_item_by_id(item_id)
        if item:
            item.update_quantity(new_quantity)
        else:
            print("Item not found")
    
    def view_item(self, item_id):
        item = self.get_item_by_id(item_id)
        if item:
            print(item)
        else:
            print("Item not found")
    def delete_item(self, item_id):
        if item_id in self.items:
            del self.items[item_id]
            print(f"Item with ID {item_id} deleted.")
        else:
            print("Item not found")
            
    def view_all_items(self, sort_by=None):
        items_list = list(self.items.values())
        if sort_by == 'price':
            items_list.sort(key=lambda x: x.price)
        elif sort_by == 'quantity':
            items_list.sort(key=lambda x: x.quantity)
            
        if items_list:
            for item in items_list:
                print(item)
        else:
            print("No items in inventory.")
        
    def calculate_inventory_value(self):
        total_value = sum(item.price * item.quantity for item in self.items.values())
        print(f"Total inventory value: ₹{total_value}")
    
    def search_item_by_name(self, name):
        results = [item for item in self.items.values() if name.lower() in item.name.lower()]
        if results:
            for item in results:
                print(item)
        else:
            print("No items found with that name.")
    
    def search_item_by_id(self, item_id):
        item = self.get_item_by_id(item_id)
        if item:
            print(item)
        else:
            print("Item not found.")
    
    def get_item_by_id(self, item_id):
        return self.items.get(item_id)

def main():
    inventory = Inventory()

    while True:
        print("\n1. Add New Item\n2. Update Item\n   a. Update Price\n   b. Update Quantity")
        print("3. View Item\n4. Delete Item\n5. View All Items\n   a. Sort by Price\n   b. Sort by Quantity")
        print("6. Calculate Total Inventory Value\n7. Search for an Item\n   a. Search by Name\n   b. Search by Item ID\n8. Exit")

        choice = input("Choose an option: ").strip()

        if choice == '1':
            name = input("Enter item name: ")
            price = float(input("Enter item price: "))
            quantity = int(input("Enter item quantity: "))
            inventory.add_item(name, price, quantity)

        elif choice == '2':
            sub_choice = input("Choose option (a for price, b for quantity): ").strip().lower()
            item_id = int(input("Enter item ID: "))

            if sub_choice == 'a':
                new_price = float(input("Enter new price: "))
                inventory.update_item_price(item_id, new_price)
            elif sub_choice == 'b':
                new_quantity = int(input("Enter new quantity: "))
                inventory.update_item_quantity(item_id, new_quantity)

        elif choice == '3':
            item_id = int(input("Enter item ID: "))
            inventory.view_item(item_id)

        elif choice == '4':
            item_id = int(input("Enter item ID: "))
            inventory.delete_item(item_id)

        elif choice == '5':
            sub_choice = input("Sort by (a for price, b for quantity, or press Enter for no sorting): ").strip().lower()
            sort_by = None
            if sub_choice == 'a':
                sort_by = "price"
            elif sub_choice == 'b':
                sort_by = "quantity"
            inventory.view_all_items(sort_by)

        elif choice == '6':
            inventory.calculate_inventory_value()

        elif choice == '7':
            sub_choice = input("Search by (a for name, b for item ID): ").strip().lower()
            if sub_choice == 'a':
                name = input("Enter name to search: ")
                inventory.search_item_by_name(name)
            elif sub_choice == 'b':
                item_id = int(input("Enter item ID to search: "))
                inventory.search_item_by_id(item_id)

        elif choice == '8':
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()