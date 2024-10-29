class Product:
    def __init__(self, product_id, name, price, quantity):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity
        
    def __str__(self):
        return f"{self.product_id}: {self.name} - ₹{self.price} (Stock: {self.quantity})"
   
    
class Inventory:
    def __init__(self):
        self.products = {}
    
    def add_products(self, product):
        self.products[product.product_id] = product
    
    def get_product(self, product_id):
        return self.products.get(product_id)
    
    def update_stock(self, product_id, quantity):
        if product_id in self.products and self.products[product_id].quantity >= quantity:
            self.products[product_id].quantity -= quantity
            return True
        return False
    
    def display_products(self):
        print("Available Products: ")
        for product in self.products.values():
            print(product)


class Cart:
    def __init__(self):
        self.items = {}
    
    def add_to_cart(self, product, quantity):
        if product.product_id in self.items:
            self.items[product.product_id]['quantity'] += quantity
        else:
            self.items[product.product_id] = {'product': product, 'quantity': quantity}
    
    def remove_from_cart(self, product_id):
        if product_id in self.items:
            del self.items[product_id]
            print("Item removed from cart.")
        else:
            print("Item not in cart.")
        
    def display_cart(self):
        if not self.items:
            print("Your cart is empty.")
            return
        print("Items in Cart: ")
        for item in self.items.values():
            product = item['product']
            quantity = item['quantity']
            print(f"{product.name} - ₹{product.price} x {quantity} (Total: ₹{product.price * quantity})")
    
    def calculate_total(self):
        return sum(item['product'].price * item['quantity'] for item in self.items.values())
    
    def checkout(self, inventory):
        for item in self.items.values():
            product = item['product']
            quantity = item['quantity']
            if inventory.update_stock(product.product_id, quantity):
                continue
            else:
                print(f"Sorry, not enough stock for {product.name}.")
                return False
        total = self.calculate_total()
        self.items.clear()
        print(f"Checkout successful! Total: ₹{total}")
        return True
    

class ECommerceSystem:
    def __init__(self):
        self.inventory = Inventory()
        self.cart = Cart()
        self.setup_inventory()
        
    def setup_inventory(self):
        self.inventory.add_products(Product(1, "Laptop", 999.99, 5))
        self.inventory.add_products(Product(2, "Smartphone", 499.99, 10))
        self.inventory.add_products(Product(3, "Headphones", 149.99, 15))
        self.inventory.add_products(Product(4, "Keyboard", 89.99, 20))

    def display_menu(self):
        print("\nE-Commerce System")
        print("1. View Products")
        print("2. Add to Cart")
        print("3. View Cart")
        print("4. Remove from Cart")
        print("5. Checkout")
        print("6. Exit")

    def run(self):
        while True:
            self.display_menu()
            choice = input("Choose an option: ")
            if choice == "1":
                self.inventory.display_products()
            elif choice == "2":
                product_id = int(input("Enter the product ID to add: "))
                quantity = int(input("Enter the quantity: "))
                product = self.inventory.get_product(product_id)
                if product and product.quantity >= quantity:
                    self.cart.add_to_cart(product, quantity)
                    print(f"Added {quantity} of {product.name} to cart.")
                else:
                    print("Product not available or insufficient stock.")
            elif choice == "3":
                self.cart.display_cart()
            elif choice == "4":
                product_id = int(input("Enter the product ID to remove: "))
                self.cart.remove_from_cart(product_id)
            elif choice == "5":
                if self.cart.checkout(self.inventory):
                    print("Thank you for your purchase!")
                else:
                    print("Checkout failed due to stock issues.")
            elif choice == "6":
                print("Exiting system. Thank you!")
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    ecommerce_system = ECommerceSystem()
    ecommerce_system.run()