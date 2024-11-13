# ----------------- Product Class -----------------
class Product:
    def _init_(self, product_id, name, category, price, stock_quantity):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.stock_quantity = stock_quantity

    def update_stock(self, quantity):
        """Update stock quantity (positive for restocking, negative for sales)."""
        if self.stock_quantity + quantity < 0:
            raise ValueError("Not enough stock to complete the sale.")
        self.stock_quantity += quantity

    def _str_(self):
        return f"ID: {self.product_id}, Name: {self.name}, Category: {self.category}, Price: ${self.price}, Stock: {self.stock_quantity}"


# ----------------- Inventory Management Class -----------------
class Inventory:
    def _init_(self):
        self.products = {}

    def add_product(self, product):
        """Add a new product to the inventory."""
        if product.product_id in self.products:
            raise ValueError(f"Product ID {product.product_id} already exists.")
        self.products[product.product_id] = product

    def update_product(self, product_id, name=None, category=None, price=None, stock_quantity=None):
        """Update an existing product."""
        if product_id not in self.products:
            raise ValueError(f"Product ID {product_id} not found.")
        product = self.products[product_id]
        if name:
            product.name = name
        if category:
            product.category = category
        if price is not None:
            product.price = price
        if stock_quantity is not None:
            product.stock_quantity = stock_quantity

    def delete_product(self, product_id):
        """Delete a product from the inventory."""
        if product_id not in self.products:
            raise ValueError(f"Product ID {product_id} not found.")
        del self.products[product_id]

    def view_all_products(self):
        """View all products in the inventory."""
        if not self.products:
            print("No products available in inventory.")
        for product in self.products.values():
            print(product)

    def search_product(self, query):
        """Search products by name or category."""
        found = False
        for product in self.products.values():
            if query.lower() in product.name.lower() or query.lower() in product.category.lower():
                print(product)
                found = True
        if not found:
            print(f"No products found for query: {query}")

    def check_stock_levels(self):
        """Check stock levels and prompt restocking if necessary."""
        for product in self.products.values():
            if product.stock_quantity <= 5:
                print(f"Warning: {product.name} (ID: {product.product_id}) is low on stock!")


# ----------------- User and Admin Authentication -----------------
class User:
    def _init_(self, username, password):
        self.username = username
        self.password = password


class Admin(User):
    def _init_(self, username, password):
        super()._init_(username, password)


class CafeIMS:
    def _init_(self):
        self.inventory = Inventory()
        self.users = {
            'admin': Admin('admin', 'admin123'),
            'user1': User('user1', 'user123')
        }
        self.logged_in_user = None

    def login(self, username, password):
        """Authenticate user."""
        if username in self.users and self.users[username].password == password:
            self.logged_in_user = self.users[username]
            print(f"Welcome, {username}!")
            return True
        else:
            print("Invalid username or password.")
            return False

    def logout(self):
        """Log out the user."""
        self.logged_in_user = None
        print("Logged out successfully.")

    def show_menu(self):
        """Show menu based on user role."""
        if isinstance(self.logged_in_user, Admin):
            return """
1. Add Product
2. Update Product
3. Delete Product
4. View All Products
5. Search Products
6. Check Stock Levels
7. Logout
            """
        elif isinstance(self.logged_in_user, User):
            return """
1. View All Products
2. Search Products
3. Check Stock Levels
4. Logout
            """
        return ""

    def execute_option(self, choice):
        """Execute the menu option."""
        try:
            if isinstance(self.logged_in_user, Admin):
                if choice == 1:
                    self.add_product()
                elif choice == 2:
                    self.update_product()
                elif choice == 3:
                    self.delete_product()
                elif choice == 4:
                    self.inventory.view_all_products()
                elif choice == 5:
                    self.search_product()
                elif choice == 6:
                    self.inventory.check_stock_levels()
                elif choice == 7:
                    self.logout()
                else:
                    print("Invalid option!")
            elif isinstance(self.logged_in_user, User):
                if choice == 1:
                    self.inventory.view_all_products()
                elif choice == 2:
                    self.search_product()
                elif choice == 3:
                    self.inventory.check_stock_levels()
                elif choice == 4:
                    self.logout()
                else:
                    print("Invalid option!")
        except ValueError as e:
            print(f"Error: {e}")

    def add_product(self):
        """Add a new product to the inventory."""
        try:
            product_id = input("Enter product ID: ")
            name = input("Enter product name: ")
            category = input("Enter product category: ")
            price = float(input("Enter product price: "))
            stock_quantity = int(input("Enter product stock quantity: "))
            new_product = Product(product_id, name, category, price, stock_quantity)
            self.inventory.add_product(new_product)
            print(f"Product {name} added successfully.")
        except ValueError as e:
            print(f"Error: {e}")

    def update_product(self):
        """Update a product's details."""
        try:
            product_id = input("Enter product ID to update: ")
            name = input("Enter new name (leave blank to keep current): ")
            category = input("Enter new category (leave blank to keep current): ")
            price = input("Enter new price (leave blank to keep current): ")
            stock_quantity = input("Enter new stock quantity (leave blank to keep current): ")

            price = float(price) if price else None
            stock_quantity = int(stock_quantity) if stock_quantity else None

            self.inventory.update_product(product_id, name, category, price, stock_quantity)
            print(f"Product {product_id} updated successfully.")
        except ValueError as e:
            print(f"Error: {e}")

    def delete_product(self):
        """Delete a product from the inventory."""
        try:
            product_id = input("Enter product ID to delete: ")
            self.inventory.delete_product(product_id)
            print(f"Product {product_id} deleted successfully.")
        except ValueError as e:
            print(f"Error: {e}")

    def search_product(self):
        """Search products by name or category."""
        query = input("Enter product name or category to search: ")
        self.inventory.search_product(query)


# ----------------- Main Program -----------------
def main():
    ims = CafeIMS()

    while True:
        if ims.logged_in_user is None:
            print("1. Login")
            print("2. Exit")
            try:
                option = int(input("Choose an option: "))
                if option == 1:
                    username = input("Enter username: ")
                    password = input("Enter password: ")
                    if ims.login(username, password):
                        continue
                elif option == 2:
                    print("Exiting the system.")
                    break
                else:
                    print("Invalid option.")
            except ValueError:
                print("Invalid input, please enter a valid number.")
        else:
            print(ims.show_menu())
            try:
                choice = int(input("Choose an option: "))
                ims.execute_option(choice)
            except ValueError:
                print("Invalid input, please enter a valid number.")

if _name_ == "_main_":
    main()