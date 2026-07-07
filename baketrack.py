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
            print("\n" + "=" * 40)
            print("         BAKETRACK DASHBOARD         ")
            print("=" * 40)
            print(" [1] Add New Employee")
            print(" [2] Add New Product")
            print(" [3] View All Employees")
            print(" [4] View All Products")
            print(" [5] Exit System")
            print("-" * 40)
            
            choice = input("Select an option (1-5): ").strip()
            print("-" * 40)

            if choice == "1":
                name = input("Enter employee name: ")
                valid_name = self.validator.validate_name(name)
                if valid_name:
                    self.db.add_employee(valid_name)
                    print("\nSuccess: Employee added successfully!")
                else:
                    print("\nError: Invalid name. Must be at least 3 letters.")

            elif choice == "2":
                name = input("Enter product name: ")
                valid_name = self.validator.validate_name(name)
                if not valid_name:
                    print("\nError: Invalid name. Must be at least 3 letters.")
                    continue
                
                price_str = input("Enter product price: ")
                valid_price = self.validator.validate_price(price_str)
                if valid_price:
                    self.db.add_product(valid_name, valid_price)
                    print("\nSuccess: Product added successfully!")
                else:
                    print("\nError: Invalid price. Must be a positive number.")

            elif choice == "3":
                employees = self.db.get_employees()
                if not employees:
                    print("Notice: No employees found in the database.")
                else:
                    print(f"{'ID':<6} | {'EMPLOYEE NAME':<25}")
                    print("-" * 40)
                    for emp in employees:
                        print(f"{emp[0]:<6} | {emp[1]:<25}")

            elif choice == "4":
                products = self.db.get_products()
                if not products:
                    print("Notice: No products found in the database.")
                else:
                    print(f"{'ID':<6} | {'PRODUCT NAME':<20} | {'PRICE':<10}")
                    print("-" * 40)
                    for prod in products:
                        print(f"{prod[0]:<6} | {prod[1]:<20} | ₦{prod[2]:<10,}")

            elif choice == "5":
                print("Shutting down BakeTrack. Goodbye!")
                print("=" * 40 + "\n")
                break
            
            else:
                print("\nError: Invalid selection. Please choose a number between 1 and 5.")

if __name__ == "__main__":
    app = BakeryApp()
    app.run()