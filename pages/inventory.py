import customtkinter as ctk
from tkinter import messagebox

from database import get_products, add_product, delete_product, update_product  

class InventoryPage(ctk.CTkFrame):

    def __init__(self, master, on_products_changed=None):
        super().__init__(master)

        self.on_products_changed = on_products_changed

        # Inventory heading
        inventory_title = ctk.CTkLabel(
            self,
            text="Inventory Management",
            font=ctk.CTkFont(size=26, weight="bold")
        )
        inventory_title.pack(pady=30)

        # Main two-column layout
        inventory_content = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        inventory_content.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        self.inventory_left = ctk.CTkFrame(
            inventory_content,
            width=280
        )
        self.inventory_left.pack(side="left", fill="y", padx=10, pady=10)

        self.inventory_right = ctk.CTkFrame(
            inventory_content
        )
        self.inventory_right.pack(side="right", fill="both", expand=True, padx=10, pady=10)


        # Products Heading Section
        products_heading = ctk.CTkLabel(
            self.inventory_right,
            text="Products",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        products_heading.pack(anchor="w", padx=15, pady=15)

        # Scrollable products list
        self.products_list_frame = ctk.CTkScrollableFrame(
            self.inventory_right,
            fg_color="transparent"
        )
        self.products_list_frame.pack(
            fill="both", expand=True, padx=10, pady=10)


        # Inventory summary card
        inventory_summary = ctk.CTkFrame(
            self.inventory_left,
            width=250,
            height=100,
            corner_radius=12
        )
        inventory_summary.pack(anchor="w", padx=30, pady=10)
        inventory_summary.pack_propagate(False)

        total_products_label = ctk.CTkLabel(
            inventory_summary,
            text="Total Products",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        total_products_label.pack(pady=(15, 5))

        self.total_products_value = ctk.CTkLabel(
            inventory_summary,
            text="0",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.total_products_value.pack()


        # Product name input
        self.product_name_entry = ctk.CTkEntry(
            self.inventory_left,
            placeholder_text="Product Name",
            width=250
        )
        self.product_name_entry.pack(pady=10)

        # Product price input
        self.product_price_entry = ctk.CTkEntry(
            self.inventory_left,
            placeholder_text="Product Price",
            width=250
        )
        self.product_price_entry.pack(pady=10)

        # Product stock input
        self.product_stock_entry = ctk.CTkEntry(
            self.inventory_left,
            placeholder_text="Product Stock",
            width=250
        )
        self.product_stock_entry.pack(pady=10)

        # Add product button
        add_product_btn = ctk.CTkButton(
            self.inventory_left,
            text="Add Product",
            width=200,
            height=40,
            command=self.save_product
        )
        add_product_btn.pack(pady=20)

        self.load_inventory()





    
    def save_product(self):
        name = self.product_name_entry.get().strip()
        price = self.product_price_entry.get()
        stock = self.product_stock_entry.get()

        if not name or not price or not stock:
            messagebox.showerror("Error", "Please fill in all fields!")
            return

        try:
            price = float(price)
            stock = int(stock)

            if price <= 0 or stock < 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Enter a valid price and stock quantity!"
            )
            return

        add_product(name, price, stock)

        if self.on_products_changed:
            self.on_products_changed()

        self.load_inventory()

        messagebox.showinfo(
            "Product Added",
            f"{name} added successfully!"
        )

        self.product_name_entry.delete(0, "end")
        self.product_price_entry.delete(0, "end")
        self.product_stock_entry.delete(0, "end")




    
    def load_inventory(self):

        # Clear the previous product list
        for widget in self.products_list_frame.winfo_children():
            widget.destroy()

        # Retrieve products from database
        products = get_products()

        # Update total product count
        self.total_products_value.configure(
            text=str(len(products))
        )

        # Create a card for each product
        for product_id, name, price, stock in products:

            product_row = ctk.CTkFrame(
                self.products_list_frame,
                corner_radius=10
            )
            product_row.pack(fill="x", padx=8, pady=6)

            product_name = ctk.CTkLabel(
                product_row,
                text=name,
                font=ctk.CTkFont(size=16, weight="bold")
            )
            product_name.pack(anchor="w", padx=15, pady=(10, 2))

            details_frame = ctk.CTkFrame(
                product_row,
                fg_color="transparent"
            )
            details_frame.pack(fill="x", padx=15, pady=(2, 10))

            price_label = ctk.CTkLabel(
                details_frame,
                text=f"${price:.2f}",
                font=ctk.CTkFont(size=13)
            )
            price_label.pack(side="left")

            stock_label = ctk.CTkLabel(
                details_frame,
                text=f"Stock: {stock}",
                font=ctk.CTkFont(size=13)
            )

            edit_btn = ctk.CTkButton(
                details_frame,
                text="Edit",
                width=50,
                height=28,
                command=lambda pid=product_id, pname=name, pprice=price, pstock=stock:
                    self.edit_product(pid, pname, pprice, pstock)
            )
            edit_btn.pack(side="right", padx=5)

            restock_btn = ctk.CTkButton(
                details_frame,
                text="Restock",
                width=50,
                height=28,
                command=lambda pid=product_id, pname=name:
                    self.restock_product(pid, pname)
            )
            restock_btn.pack(side="right", padx=5)



            delete_btn = ctk.CTkButton(
                details_frame,
                text="Delete",
                width=50,
                height=28,
                fg_color="#D9534F",
                hover_color="#B52B27",
                command=lambda pid=product_id, pname=name: self.delete_inventory_product(pid, pname)
            )
            delete_btn.pack(side="right", padx=5)
            stock_label.pack(side="right")


    def edit_product(self, product_id, name, price, stock):
        edit_window  = ctk.CTkToplevel(self)
        edit_window.title("Edit Product")
        edit_window.geometry("350x350")
        
        edit_window.transient(self.winfo_toplevel())
        edit_window.grab_set()

        name_entry = ctk.CTkEntry(edit_window, placeholder_text="Product Name")
        name_entry.pack(pady=10, padx=20, fill="x")
        name_entry.insert(0, name)

        price_entry = ctk.CTkEntry(edit_window, placeholder_text="Product Price")
        price_entry.pack(pady=10, padx=20, fill="x")
        price_entry.insert(0, str(price))

        stock_entry = ctk.CTkEntry(edit_window, placeholder_text="Product Stock")
        stock_entry.pack(pady=10, padx=20, fill="x")
        stock_entry.insert(0, str(stock))

        save_btn = ctk.CTkButton(
            edit_window,
            text="Save Changes",
            command=lambda: self.save_edited_product(
                product_id,
                name_entry.get(),
                price_entry.get(),
                stock_entry.get(),
                edit_window
            )
        )
        save_btn.pack(pady=20)

    def restock_product(self, product_id, name):
        restock_window = ctk.CTkToplevel(self)
        restock_window.title("Restock Product")
        restock_window.geometry("350x220")

        restock_window.transient(self.winfo_toplevel())
        restock_window.grab_set()

        product_label = ctk.CTkLabel(
            restock_window,
            text=f"Restocking: {name}",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        product_label.pack(pady=15)

        quantity_entry = ctk.CTkEntry(
            restock_window,
            placeholder_text="Quantity to add",
            width=250
        )
        quantity_entry.pack(pady=10)

        restock_btn = ctk.CTkButton(
            restock_window,
            text="Add Stock",
            command=lambda: self.save_restock(
                product_id, 
                quantity_entry.get(),
                restock_window
            )
        )
        restock_btn.pack(pady=15)

    def save_restock(self, product_id, quantity, restock_window):
        
        try:
            quantity = int(quantity)
        except ValueError:
            messagebox.showerror(
                "Invalid Quantity",
                "Please enter a valid whole number!"
            )
            return
            
        if quantity <= 0:
            messagebox.showerror(
                "Invalid Quantity",
                "Quantity must be greater than zero!"
            )
            return

        for pid, name, price, stock in get_products():
            if pid == product_id:
                new_stock = stock + quantity
                update_product(product_id, name, price, new_stock)

                if self.on_products_changed:
                    self.on_products_changed()

                self.load_inventory()
                restock_window.destroy()

                messagebox.showinfo(
                    "Restock Successful",
                    f"Added {quantity} units to {name}!"
                )
                break



    def save_edited_product(self, product_id, name, price, stock, edit_window):
        name = name.strip()

        if not name:
            messagebox.showerror("Invalid Name", "Product name cannot be empty!")
            return

        try:
            price = float(price)
            stock = int(stock)

            if price <= 0 or stock < 0:
                raise ValueError

        except ValueError:
            messagebox.showerror("Invalid Input", "Enter a valid price and stock quantity!")
            return

        update_product(product_id, name, price, stock)


        if self.on_products_changed:
            self.on_products_changed()

        self.load_inventory()
        edit_window.destroy()

        messagebox.showinfo("Success", "Product updated successfully!")


        






    def delete_inventory_product(self, product_id, name):

        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete {name}?"
        )

        if not confirm:
            return

        delete_product(product_id)

        if self.on_products_changed:
            self.on_products_changed()

        self.load_inventory()








    