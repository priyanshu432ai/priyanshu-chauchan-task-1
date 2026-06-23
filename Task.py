import sqlite3

# Connect to database
conn = sqlite3.connect("inventory.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL
)
""")
conn.commit()


# Add Product
def add_product():
    name = input("Enter Product Name: ")
    quantity = int(input("Enter Quantity: "))
    price = float(input("Enter Price: "))

    cursor.execute(
        "INSERT INTO products (name, quantity, price) VALUES (?, ?, ?)",
        (name, quantity, price)
    )
    conn.commit()
    print("Product Added Successfully!\n")


# View Products
def view_products():
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    if not products:
        print("No Products Found.\n")
        return

    print("\n----- Inventory -----")
    print("ID\tName\tQuantity\tPrice")
    print("-" * 40)

    for product in products:
        print(f"{product[0]}\t{product[1]}\t{product[2]}\t\t₹{product[3]}")

    print()


# Search Product
def search_product():
    product_id = int(input("Enter Product ID: "))

    cursor.execute("SELECT * FROM products WHERE id=?", (product_id,))
    product = cursor.fetchone()

    if product:
        print("\nProduct Found")
        print(f"ID: {product[0]}")
        print(f"Name: {product[1]}")
        print(f"Quantity: {product[2]}")
        print(f"Price: ₹{product[3]}\n")
    else:
        print("Product Not Found!\n")


# Update Product
def update_product():
    product_id = int(input("Enter Product ID to Update: "))

    cursor.execute("SELECT * FROM products WHERE id=?", (product_id,))
    product = cursor.fetchone()

    if product:
        name = input("Enter New Product Name: ")
        quantity = int(input("Enter New Quantity: "))
        price = float(input("Enter New Price: "))

        cursor.execute("""
        UPDATE products
        SET name=?, quantity=?, price=?
        WHERE id=?
        """, (name, quantity, price, product_id))

        conn.commit()
        print("Product Updated Successfully!\n")
    else:
        print("Product Not Found!\n")


# Delete Product
def delete_product():
    product_id = int(input("Enter Product ID to Delete: "))

    cursor.execute("SELECT * FROM products WHERE id=?", (product_id,))
    product = cursor.fetchone()

    if product:
        cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
        conn.commit()
        print("Product Deleted Successfully!\n")
    else:
        print("Product Not Found!\n")


# Main Menu
while True:
    print("========== Inventory Management System ==========")
    print("1. Add Product")
    print("2. View Products")
    print("3. Search Product")
    print("4. Update Product")
    print("5. Delete Product")
    print("6. Exit")

    choice = input("Enter Choice: ")

    if choice == "1":
        add_product()
    elif choice == "2":
        view_products()
    elif choice == "3":
        search_product()
    elif choice == "4":
        update_product()
    elif choice == "5":
        delete_product()
    elif choice == "6":
        print("Exiting Inventory Management System...")
        conn.close()
        break
    else:
        print("Invalid Choice! Please Try Again.\n")
