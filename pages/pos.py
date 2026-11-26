import customtkinter as ctk
from tkinter import messagebox

from database import get_products, create_sale


class POSPage(ctk.CTkFrame):

    def __init__(self, master, on_sale_completed=None):
        super().__init__(master)
        self.on_sale_completed = on_sale_completed
        self.cart = {}
        self.products = {}
        self.product_buttons = []

        # POS heading
        self.pos_heading = ctk.CTkLabel(
            self,
            text="Point Of Sale",
            font=ctk.CTkFont(size=26, weight="bold")
        )
        self.pos_heading.pack(pady=30)

        # Product search
        self.product_search = ctk.CTkEntry(
            self,
            placeholder_text="Search Products..."
        )
        self.product_search.pack(padx=20, pady=20, fill="x")


        # Main POS layout

        # Product list
        self.product_frame = ctk.CTkScrollableFrame(self)
        self.product_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.product_frame.bind(
            "<Configure>",
            self.arrange_product_buttons,
            add="+"
        )

        # Shopping cart
        self.cart_frame = ctk.CTkFrame(
            self,
            width=280
        )
        self.cart_frame.pack(
            side="right",
            fill="both",
            expand=False,
            padx=10,
            pady=10
        )
        self.cart_frame.pack_propagate(False)

        # Shopping cart heading
        self.cart_heading = ctk.CTkLabel(
            self.cart_frame,
            text="Shopping Cart",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.cart_heading.pack(side="top", pady=10)

        # Cart items list
        self.cart_items_frame = ctk.CTkScrollableFrame(
            self.cart_frame,
            height=180
        )
        self.cart_items_frame.pack(
            side="top",
            fill="both",
            expand=False,
            padx=8,
            pady=5
        )

        # Cart controls
        self.cart_controls_frame = ctk.CTkFrame(self.cart_frame)
        self.cart_controls_frame.pack(
            side="bottom",
            fill="x",
            padx=8,
            pady=4
        )

        self.cart_controls_frame.grid_columnconfigure(
            0, weight=1, uniform="cart"
        )
        self.cart_controls_frame.grid_columnconfigure(
            1, weight=1, uniform="cart"
        )


        # Discount controls
        self.discount_entry = ctk.CTkEntry(
            self.cart_controls_frame,
            placeholder_text="Discount (%)",
            height=30
        )
        self.discount_entry.grid(
            row=0, column=0, padx=3, pady=2, sticky="ew"
        )

        self.apply_discount_btn = ctk.CTkButton(
            self.cart_controls_frame,
            text="Apply Discount",
            height=30,
            command=self.update_cart
        )
        self.apply_discount_btn.grid(
            row=0, column=1, padx=3, pady=2, sticky="ew"
        )


        # Subtotal
        self.subtotal_label = ctk.CTkLabel(
            self.cart_controls_frame,
            text="Subtotal: $0.00"
        )
        self.subtotal_label.grid(
            row=1, column=0, padx=3, pady=2
        )

        # Discount amount
        self.discount_label = ctk.CTkLabel(
            self.cart_controls_frame,
            text="Discount: $0.00"
        )
        self.discount_label.grid(
            row=1, column=1, padx=3, pady=2
        )

        # Final total
        self.cart_total = ctk.CTkLabel(
            self.cart_controls_frame,
            text="Total: $0.00",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.cart_total.grid(
            row=2,
            column=0,
            columnspan=2,
            pady=3
        )


        # Checkout button
        self.checkout_btn = ctk.CTkButton(
            self.cart_controls_frame,
            text="Checkout",
            height=34,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.checkout
        )
        self.checkout_btn.grid(
            row=3, column=0, padx=3, pady=2, sticky="ew"
        )

        # Clear cart button
        self.clear_cart_btn = ctk.CTkButton(
            self.cart_controls_frame,
            text="Clear Cart",
            height=34,
            fg_color="#D9534F",
            hover_color="#B52B27",
            command=self.clear_cart
        )
        self.clear_cart_btn.grid(
            row=3, column=1, padx=3, pady=2, sticky="ew"
        )

        # Load products and initialize cart
        self.load_products()
        self.update_cart()


    def arrange_product_buttons(self, event=None):

        available_width = self.product_frame._parent_canvas.winfo_width()

        if not self.product_buttons:
            return

        button_width = self.product_buttons[0].winfo_reqwidth()

        # Calculate how many buttons actually fit
        columns = max(
            1,
            min(4, (available_width - 20) // (button_width + 20))
        )

        for index, button in enumerate(self.product_buttons):

            row = index // columns
            column = index % columns

            button.grid(
                row=row,
                column=column,
                padx=10,
                pady=10
            )



    def load_products(self):

        # Remove old product buttons
        for widget in self.product_frame.winfo_children():
            widget.destroy()

        # Load complete product information from database
        self.products.clear()

        for product_id, name, price, stock in get_products():

            self.products[product_id] = {
                "name": name,
                "price": price,
                "stock": stock
            }

            self.cart = {
                product_id: quantity
                for product_id, quantity in self.cart.items()
                if product_id in self.products
            }

        # Create product buttons
        self.product_buttons.clear()

        for product_id, product in self.products.items():

            product_btn = ctk.CTkButton(
                self.product_frame,
                text=f"{product['name']} - ${product['price']:.2f}",
                width=180,
                height=65,
                command=lambda pid=product_id: self.add_to_cart(pid)
            )

            self.product_buttons.append(product_btn)

        self.arrange_product_buttons()
        self.update_cart()




    def add_to_cart(self, product_id):

        current_quantity = self.cart.get(product_id, 0)
        available_stock = self.products[product_id]["stock"]

        if current_quantity >= available_stock:
            messagebox.showwarning(
                "Insufficient Stock",
                "Not enough stock available!"   
            )
            return

        self.cart[product_id] = current_quantity + 1

        self.update_cart()



    def update_cart(self):

        # Clear existing cart items
        for widget in self.cart_items_frame.winfo_children():
            widget.destroy()

        # Display current cart items
        for product_id, quantity in self.cart.items():

            product_name = self.products[product_id]["name"]

            item_frame = ctk.CTkFrame(self.cart_items_frame)
            item_frame.pack(fill="x", padx=5, pady=5)

            item_frame.grid_columnconfigure(0, weight=1)
            item_frame.grid_columnconfigure(1, weight=0)
            item_frame.grid_columnconfigure(2, weight=0)

            item = ctk.CTkLabel(
                item_frame,
                text=f"{product_name}  x{quantity}",
                anchor="w",
                justify="left",
                wraplength=130
            )
            item.grid(row=0, column=0, sticky="ew", padx=8, pady=5)

            remove_btn = ctk.CTkButton(
                item_frame,
                text="-",
                width=30,
                command=lambda pid=product_id: self.remove_from_cart(pid)
            )
            remove_btn.grid(row=0, column=1, padx=3, pady=5)

            add_btn = ctk.CTkButton(
                item_frame,
                text="+",
                width=30,
                command=lambda pid=product_id: self.add_to_cart(pid)
            )
            add_btn.grid(row=0, column=2, padx=3, pady=5)

        # Refresh price labels
        self.subtotal_label.configure(
            text=f"Subtotal: ${self.calculate_subtotal():.2f}"
        )

        self.discount_label.configure(
            text=f"Discount: -${self.calculate_discount():.2f}"
        )

        self.cart_total.configure(
            text=f"Total: ${self.calculate_total():.2f}"
        )




    def calculate_subtotal(self):

        total = 0

        for product_id, quantity in self.cart.items():

            price = self.products[product_id]["price"]

            total += quantity * price

        return total


    def calculate_discount(self):

        try:
            percentage = float(self.discount_entry.get() or 0)
        except ValueError:
            percentage = 0

        percentage = max(0, min(percentage, 100))

        return self.calculate_subtotal() * (percentage / 100)


    def calculate_total(self):

        return self.calculate_subtotal() - self.calculate_discount()


    def remove_from_cart(self, product):

        if product in self.cart:
            if self.cart[product] > 1:
                self.cart[product] -= 1
            else:
                self.cart.pop(product)

        self.update_cart()


    def clear_cart(self):

        self.cart.clear()
        self.update_cart()



    def checkout(self):

        if not self.cart:
            print("Cart is empty!")
            return

        total = self.calculate_total()

        if total <= 0:
            print("Invalid checkout total!")
            return

        discount = self.calculate_discount()

        try:
            sale_id = create_sale(
                self.cart,
                self.products,
                total,
                discount
            )

        except Exception as e:
            messagebox.showerror("Checkout Failed", str(e))
            return

        messagebox.showinfo(
            "Checkout Successful",
            f"Sale ID: {sale_id}\n"
            f"Total Amount: ${total:.2f}\n\n"
            "Thank you for your purchase!"
        )

        self.cart.clear()
        self.load_products()

        if self.on_sale_completed:
            self.on_sale_completed()
