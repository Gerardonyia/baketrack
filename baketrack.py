import sqlite3
from datetime import datetime

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("bakery.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON;")
        self.create_tables()
        self.seed_roles()

    def create_tables(self):
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS roles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL UNIQUE
            )
        """)
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                role_id INTEGER,
                FOREIGN KEY (role_id) REFERENCES roles(id)
            )
        """)
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL
            )
        """)
       
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER,
                employee_id INTEGER,
                quantity INTEGER NOT NULL,
                total_price REAL NOT NULL,
                sale_date TEXT NOT NULL,
                FOREIGN KEY (product_id) REFERENCES products(id),
                FOREIGN KEY (employee_id) REFERENCES employees(id)
            )
        """)
        self.conn.commit()

    def seed_roles(self):
       
        roles = ["Manager", "Baker", "Cashier"]
        for role in roles:
            self.cursor.execute("INSERT OR IGNORE INTO roles (title) VALUES (?)", (role,))
        self.conn.commit()

    def get_roles(self):
        self.cursor.execute("SELECT * FROM roles")
        return self.cursor.fetchall()

    def add_employee(self, name, role_id):
        self.cursor.execute("INSERT INTO employees (name, role_id) VALUES (?, ?)", (name, role_id))
        self.conn.commit()

    def add_product(self, name, price):
        self.cursor.execute("INSERT INTO products (name, price) VALUES (?, ?)", (name, price))
        self.conn.commit()

    def add_sale(self, product_id, employee_id, quantity, total_price):
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute("""
            INSERT INTO sales (product_id, employee_id, quantity, total_price, sale_date)
            VALUES (?, ?, ?, ?, ?)
        """, (product_id, employee_id, quantity, total_price, date_str))
        self.conn.commit()

    def get_employees_with_roles(self):
        self.cursor.execute("""
            SELECT employees.id, employees.name, roles.title 
            FROM employees 
            LEFT JOIN roles ON employees.role_id = roles.id
        """)
        return self.cursor.fetchall()

    def get_products(self):
        self.cursor.execute("SELECT * FROM products")
        return self.cursor.fetchall()

    def get_product_by_id(self, product_id):
        self.cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        return self.cursor.fetchone()

    def get_sales_history(self):
        self.cursor.execute("""
            SELECT sales.id, products.name, employees.name, sales.quantity, sales.total_price, sales.sale_date
            FROM sales
            JOIN products ON sales.product_id = products.id
            JOIN employees ON sales.employee_id = employees.id
        """)
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

    def validate_integer(self, val_str):
        try:
            val = int(val_str)
            if val <= 0:
                return None
            return val
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
            print(" [1] Add New Employee (With Role)")
            print(" [2] Add New Product")
            print(" [3] Record a Sale Transaction")
            print(" [4] View All Employees & Roles")
            print(" [5] View All Products")
            print(" [6] View Sales History")
            print(" [7] Exit System")
            print("-" * 40)
            
            choice = input("Select an option (1-7): ").strip()
            print("-" * 40)

            if choice == "1":
                name = input("Enter employee name: ")
                valid_name = self.validator.validate_name(name)
                if not valid_name:
                    print("\nError: Invalid name. Must be at least 3 letters.")
                    continue
                
                print("\nAvailable Roles:")
                roles = self.db.get_roles()
                for r in roles:
                    print(f" [{r[0]}] {r[1]}")
                
                role_choice = input("Select role ID: ").strip()
                valid_role_id = self.validator.validate_integer(role_choice)
                
                if valid_role_id and valid_role_id in [r[0] for r in roles]:
                    self.db.add_employee(valid_name, valid_role_id)
                    print("\nSuccess: Employee added with role!")
                else:
                    print("\nError: Invalid Role Selection.")

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
                    print("\nError: Invalid price.")

            elif choice == "3":
                # Record a Sale
                products = self.db.get_products()
                employees = self.db.get_employees_with_roles()
                
                if not products or not employees:
                    print("\nError: Need at least one employee and one product to make a sale.")
                    continue
                
                print("Select Product ID:")
                for p in products:
                    print(f" [{p[0]}] {p[1]} (₦{p[2]:,})")
                p_id = input("Product ID: ").strip()
                
                print("\nSelect Employee ID processing this sale:")
                for e in employees:
                    print(f" [{e[0]}] {e[1]} ({e[2]})")
                e_id = input("Employee ID: ").strip()
                
                qty_str = input("\nEnter Quantity Sold: ").strip()
                
                v_pid = self.validator.validate_integer(p_id)
                v_eid = self.validator.validate_integer(e_id)
                v_qty = self.validator.validate_integer(qty_str)
                
                product = self.db.get_product_by_id(v_pid) if v_pid else None
                
                if product and v_eid in [emp[0] for emp in employees] and v_qty:
                    total = product[2] * v_qty
                    self.db.add_sale(v_pid, v_eid, v_qty, total)
                    print(f"\nSuccess: Sale logged! Total amount: ₦{total:,}")
                else:
                    print("\nError: Invalid selections or entry parameters.")

            elif choice == "4":
                employees = self.db.get_employees_with_roles()
                if not employees:
                    print("Notice: No employees found.")
                else:
                    print(f"{'ID':<6} | {'EMPLOYEE NAME':<20} | {'ROLE':<15}")
                    print("-" * 40)
                    for emp in employees:
                        print(f"{emp[0]:<6} | {emp[1]:<20} | {emp[2]:<15}")

            elif choice == "5":
                products = self.db.get_products()
                if not products:
                    print("Notice: No products found.")
                else:
                    print(f"{'ID':<6} | {'PRODUCT NAME':<20} | {'PRICE':<10}")
                    print("-" * 40)
                    for prod in products:
                        print(f"{prod[0]:<6} | {prod[1]:<20} | ₦{prod[2]:<10,}")

            elif choice == "6":
                sales = self.db.get_sales_history()
                if not sales:
                    print("Notice: No sales recorded yet.")
                else:
                    print(f"{'ID':<4} | {'PRODUCT':<12} | {'CASHIER':<10} | {'QTY':<4} | {'TOTAL':<10} | {'DATE':<12}")
                    print("-" * 65)
                    for s in sales:
                        print(f"{s[0]:<4} | {s[1]:<12} | {s[2]:<10} | {s[3]:<4} | ₦{s[4]:<9,} | {s[5]}")

            elif choice == "7":
                print("Shutting down BakeTrack. Goodbye!")
                print("=" * 40 + "\n")
                break
            
            else:
                print("\nError: Invalid selection.")

if __name__ == "__main__":
    app = BakeryApp()
    app.run()