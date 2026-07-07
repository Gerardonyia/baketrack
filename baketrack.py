import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("bakery.db")
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL
            )
        """)
        self.conn.commit()

    def add_employee(self, name):
        self.cursor.execute("INSERT INTO employees (name) VALUES (?)", (name,))
        self.conn.commit()

    def add_product(self, name, price):
        self.cursor.execute("INSERT INTO products (name, price) VALUES (?, ?)", (name, price))
        self.conn.commit()

    def get_employees(self):
        self.cursor.execute("SELECT * FROM employees")
        return self.cursor.fetchall()

    def get_products(self):
        self.cursor.execute("SELECT * FROM products")
        return self.cursor.fetchall()

    def __del__(self):
        self.conn.close()

class Validator:
    def validate_name(self, name):
        clean_name = name.strip()
        if len(clean_name) < 3 or not clean_name.isalpha():
            return None
        return clean_name

    def validate_price(self, price_str):
        try:
            price = float(price_str)
            if price <= 0:
                return None
            return price
        except ValueError:
            return None

class BakeryApp:
    def __init__(self):
        self.db = Database()
        self.validator = Validator()

    def run(self):
        while True:
            print("\n--- BakeTrack Menu ---")
            print("1. Add Employee\n2. Add Product\n3. View Employees\n4. View Products\n5. Exit")
            choice = input("Select an option: ").strip()

            if choice == "1":
                name = input("Enter employee name: ")
                valid_name = self.validator.validate_name(name)
                if valid_name:
                    self.db.add_employee(valid_name)
                    print("Employee added.")
                else:
                    print("Invalid name. Must be at least 3 letters.")

            elif choice == "2":
                name = input("Enter product name: ")
                valid_name = self.validator.validate_name(name)
                if not valid_name:
                    print("Invalid name. Must be at least 3 letters.")
                    continue
                
                price_str = input("Enter product price: ")
                valid_price = self.validator.validate_price(price_str)
                if valid_price:
                    self.db.add_product(valid_name, valid_price)
                    print("Product added.")
                else:
                    print("Invalid price. Must be a positive number.")

            elif choice == "3":
                employees = self.db.get_employees()
                for emp in employees:
                    print(f"ID: {emp[0]} | Name: {emp[1]}")

            elif choice == "4":
                products = self.db.get_products()
                for prod in products:
                    print(f"ID: {prod[0]} | Name: {prod[1]} | Price: ₦{prod[2]}")

            elif choice == "5":
                break