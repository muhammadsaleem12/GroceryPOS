import customtkinter as ctk
from tkinter import messagebox
from database import create_tables, get_products, add_product, delete_product

create_tables()

app = ctk.CTk()

app.title("GroceryPOS - Management System")
app.geometry("900x600")


#-----SIDEBAR-----
sidebar = ctk.CTkFrame(app, width=200)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)



#-----MAIN_CONTENT------
main_content = ctk.CTkFrame(app)
main_content.pack(side="right", fill="both", expand=True)

#------PAGES------

dashboard_page = ctk.CTkFrame(main_content)
pos_page = ctk.CTkFrame(main_content)
inventory_page = ctk.CTkFrame(main_content)


#------DASHBOARD------(Starts here)

dashboard_heading = ctk.CTkLabel(
    dashboard_page, 
    text="Dashboard Overview", 
    font=ctk.CTkFont(size=26, weight="bold")
)
dashboard_heading.pack(pady=30)



#----CARDS_CONTAINER----(FOR BETTER CONTROL)
cards_container = ctk.CTkFrame(
    dashboard_page,
    fg_color="transparent"
)
cards_container.pack(fill="x", padx=20, pady=20)



#------SALES_CARD------
sales_card = ctk.CTkFrame(
    cards_container, 
    width=250, 
    height=130, 
    fg_color="#FFFFFF", 
    corner_radius=12, 
    border_width=1
)
sales_card.pack(side="left", pady=20, padx=20, anchor="n")
sales_card.pack_propagate(False)

first_s = ctk.CTkLabel(
    sales_card, 
    text="Today's Sales",
    font=ctk.CTkFont(size=12, weight="bold")
)
first_s.pack(pady=(12, 4))

second_s = ctk.CTkLabel(
    sales_card, 
    text="$0.00",
    font=ctk.CTkFont(size=24, weight="bold")
)
second_s.pack(pady=4)

third_s = ctk.CTkLabel(
    sales_card, 
    text="Today's total revenue", 
    wraplength=180, 
    justify="center", 
    font=ctk.CTkFont(size=12, weight="bold")
)
third_s.pack(pady=4)



#------TRANSACTIONS_CARD------
transactions_card = ctk.CTkFrame(
    cards_container, 
    width=250, 
    height=130, 
    fg_color="#FFFFFF", 
    corner_radius=12, 
    border_width=1
)
transactions_card.pack(side="left", pady=20, padx=20, anchor="n")
transactions_card.pack_propagate(False)

first_t = ctk.CTkLabel(
    transactions_card, 
    text="Total Transactions", 
    font=ctk.CTkFont(size=12, weight="bold")
)
first_t.pack(pady=(12, 4))

second_t = ctk.CTkLabel(
    transactions_card, 
    text="0", 
    font=ctk.CTkFont(size=24, weight="bold")
)
second_t.pack(pady=(4))

third_t = ctk.CTkLabel(
    transactions_card, 
    text="Today's transactions", 
    wraplength=180, 
    justify="center", 
    font=ctk.CTkFont(size=12, weight="bold")
)
third_t.pack(pady=(4))



#------RECENT_SALES_HISTORY-------
recent_sales_frame = ctk.CTkFrame(
    dashboard_page, 
    width=500, 
    height=250, 
    fg_color="#FFFFFF",
    corner_radius=12, 
    border_width=1
)
recent_sales_frame.pack(side="top", fill="x", padx=20, pady=20)
recent_sales_frame.pack_propagate(False)



#------RECENT_SALES_HEADING-------
recent_sales_heading = ctk.CTkLabel(
    recent_sales_frame, 
    text="Recent Sales", 
    font=ctk.CTkFont(size=20, weight="bold")
)
recent_sales_heading.pack(pady=(4))



#------RECENT_SALES_TRANSACTIONS------
recent_sales_t1 = ctk.CTkLabel(
    recent_sales_frame, 
    text="Receipt #001 | Walk-in | Rs. 1,500", 
    font=ctk.CTkFont(size=12, weight="bold")
)
recent_sales_t1.pack(pady=(4))

recent_sales_t2 = ctk.CTkLabel(
    recent_sales_frame, 
    text="Receipt #002 | Walk-in | Rs. 850", 
    font=ctk.CTkFont(size=12, weight="bold")
)
recent_sales_t2.pack(pady=(4))

recent_sales_t3 = ctk.CTkLabel(
    recent_sales_frame, 
    text="Receipt #003 | Walk-in | Rs. 2,200", 
    font=ctk.CTkFont(size=12, weight="bold")
)
recent_sales_t3.pack(pady=(4))

#------DASHBOARD------(Ends here)


#-----POS----(Starts here)
pos_heading = ctk.CTkLabel(
    pos_page, 
    text="Point Of Sale", 
    font=ctk.CTkFont(size=26, weight="bold")
)
pos_heading.pack(pady=30)

product_search = ctk.CTkEntry(
    pos_page, 
    placeholder_text="Search Products..."
)
product_search.pack(padx=20, pady=20, fill="x")

product_frame = ctk.CTkScrollableFrame(pos_page)
product_frame.pack(
    side="left", 
    fill="both", 
    expand=True, 
    padx=10, 
    pady=10
)

cart_frame = ctk.CTkFrame(pos_page, width=280)
cart_frame.pack(
    side="right",
    fill="both",
    expand=False,
    padx=10,
    pady=10
)
cart_frame.pack_propagate(False)

cart_heading = ctk.CTkLabel(
    cart_frame, 
    text="Shopping Cart", 
    font=ctk.CTkFont(size=20, weight="bold")
)
cart_heading.pack(side="top", pady=15)

discount_entry = ctk.CTkEntry(
    cart_frame,
    placeholder_text="Discount (%)", 
    width=120
)
discount_entry.pack(pady=5)

apply_discount_btn = ctk.CTkButton(
    cart_frame,
    text="Apply Discount",
    command=lambda: update_cart()
)
apply_discount_btn.pack(pady=5)

subtotal_label = ctk.CTkLabel(
    cart_frame,
    text="Subtotal: $0.00"
)
subtotal_label.pack(pady=2)

discount_label = ctk.CTkLabel(
    cart_frame,
    text="Discount: $0.00"
)
discount_label.pack(pady=2)



cart_total = ctk.CTkLabel(
    cart_frame, 
    text="Total: $0.00", 
    font=ctk.CTkFont(size=20, weight="bold")
)
cart_total.pack(pady=20)


def checkout():
    if not cart:
        print("Cart is empty!")
        return

    total = calculate_total()

    if total <= 0:
        print("Invalid checkout total!")
        return

    messagebox.showinfo(
        "Checkout Successful", 
        f"Total Amount: ${total:.2f}\n\nThankyou for your purchase!"
    )


checkout_btn = ctk.CTkButton(
    cart_frame, 
    text="Checkout", 
    height=40, 
    font=ctk.CTkFont(size=15, weight="bold"),
    command=checkout
)
checkout_btn.pack(fill="x", padx=15, pady=20)

def clear_cart():
    cart.clear()
    update_cart()

def remove_from_cart(product):
    if product in cart:
        if cart[product] > 1:
            cart[product] -= 1
        else:
            cart.pop(product)

    update_cart()
    


clear_cart_btn = ctk.CTkButton(
    cart_frame, 
    text="Clear Cart", 
    fg_color="#D9534F", 
    hover_color="#B52B27", 
    command=clear_cart
)
clear_cart_btn.pack(fill="x", padx=15, pady=10)

cart_items_frame = ctk.CTkScrollableFrame(
    cart_frame,
    width=300,
    height=250
)
cart_items_frame.pack(fill="both", expand=True, padx=5, pady=5)

#---WORKAORUND_FOR_TOUCHPAD_SCROLLING-->--(Mouse wheel works but not a touchpad scrolling)
def decode_touchpad_delta(raw_delta):
    raw = raw_delta & 0xFFFFFFFF

    delta_y = raw & 0xFFFF

    if delta_y >= 0x8000:
        delta_y -= 0x10000

    return delta_y


def trackpad_scroll(event):
    delta_y = decode_touchpad_delta(event.delta)

    if delta_y:
        cart_items_frame._parent_canvas.yview_scroll(
            -delta_y,
            "units"
        )

    return "break"

app.bind_all(
    "<TouchpadScroll>",
    trackpad_scroll,
    add="+"
)

#-----CART_FUNCTION------
cart = {}
discount_percentage = 0
product_prices = {
    name: price for product_id, name, price, stock in get_products()
}

def add_to_cart(product):
    if product in cart:
        cart[product] += 1
    else:
        cart[product] = 1

    update_cart()

def calculate_subtotal():
    total = 0

    for product, quantity in cart.items():
        total += quantity * product_prices[product]

    return total

def calculate_discount():
    try:
        percentage = float(discount_entry.get() or 0)
    except ValueError:
        percentage = 0

    percentage = max(0, min(percentage, 100))

    return calculate_subtotal() * (percentage/100)

def calculate_total():
    return calculate_subtotal() - calculate_discount()

def update_cart():
    for widget in cart_items_frame.winfo_children():
        widget.destroy()

    for product, quantity in cart.items():

        item_frame = ctk.CTkFrame(cart_items_frame)
        item_frame.pack(fill="x", padx=5, pady=5)

        item = ctk.CTkLabel(
            item_frame,
            text=f"{product}  x{quantity}"
        )
        item.pack(side="left", padx=10, pady=5)

        remove_btn = ctk.CTkButton(
            item_frame,
            text="-",
            width=30,
            command=lambda p=product: remove_from_cart(p)
        )
        remove_btn.pack(side="right", padx=5, pady=5)

        add_btn = ctk.CTkButton(
            item_frame,
            text="+",
            width=30,
            command=lambda p=product: add_to_cart(p)
        )
        add_btn.pack(side="right", padx=5, pady=5)

    subtotal_label.configure(
        text=f"Subtotal: ${calculate_subtotal():.2f}"
    )
    discount_label.configure(
    text=f"Discount: -${calculate_discount():.2f}"
    )
    cart_total.configure(
        text=f"Total: ${calculate_total():.2f}"
    )

#-----Load-Products-----
def load_products():

    # Remove the old product buttons
    for widget in product_frame.winfo_children():
        widget.destroy()

    # Reload products from database
    product_prices.clear()
    product_prices.update({
        name: price for product_id, name, price, stock in get_products()
    }) 

    # Create product buttons
    for product, price in product_prices.items():

        product_btn = ctk.CTkButton(
            product_frame,
            text=f"{product} - ${price:.2f}",
            width=150,
            height=50,
            command=lambda p=product: add_to_cart(p)
        )
        product_btn.pack(pady=5)

    total_products_value.configure(
        text=str(len(product_prices))
    )


#------POS----(Ends here)




#------SIDEBAR_HEADIING------
heading = ctk.CTkLabel(
    sidebar, 
    text="GroceryPOS", 
    font=ctk.CTkFont(size=20, weight="bold")
)
heading.pack(pady=30)



#------NEVIGATION------
dashboard = ctk.CTkButton(
    sidebar, 
    text="Dashboard", 
    command=lambda: show_page(dashboard_page)
)
dashboard.pack(pady=15)

pos = ctk.CTkButton(
    sidebar, 
    text="Point Of Sale", 
    command=lambda: show_page(pos_page)
)
pos.pack(pady=15)

inventory = ctk.CTkButton(
    sidebar, 
    text="Inventory",
    command=lambda: show_page(inventory_page)
)
inventory.pack(pady=15)

sales = ctk.CTkButton(
    sidebar, 
    text="Sales"
)
sales.pack(pady=15)


#-------INVENTORY_PAGE------(Starts here)

inventory_title = ctk.CTkLabel(
    inventory_page,
    text="Inventory Management",
    font=ctk.CTkFont(size=26, weight="bold")
)
inventory_title.pack(pady=30)

inventory_content = ctk.CTkFrame(
    inventory_page,
    fg_color="transparent"
)
inventory_content.pack(fill="both", expand=True, padx=20, pady=10)

inventory_left = ctk.CTkFrame(
    inventory_content,
    width=280
)
inventory_left.pack(side="left", fill="y", padx=10, pady=10)

inventory_right = ctk.CTkFrame(
    inventory_content
)
inventory_right.pack(side="right", fill="both", expand=True, padx=10, pady=10)

#-----INVENTORY-PRODUCTS-SECTION-----

products_heading = ctk.CTkLabel(
    inventory_right,
    text="Products",
    font=ctk.CTkFont(size=22, weight="bold")
)
products_heading.pack(anchor="w", padx=15, pady=15)

products_list_frame = ctk.CTkScrollableFrame(
    inventory_right,
    fg_color="transparent",
)   
products_list_frame.pack(fill="both", expand=True, padx=10, pady=10)



inventory_summary = ctk.CTkFrame(
    inventory_left,
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

total_products_value = ctk.CTkLabel(
    inventory_summary,
    text="0",
    font=ctk.CTkFont(size=24, weight="bold")
)
total_products_value.pack()



product_name_entry = ctk.CTkEntry(
    inventory_left,
    placeholder_text="Product Name",
    width=250
)
product_name_entry.pack(pady=10)

product_price_entry = ctk.CTkEntry(
    inventory_left,
    placeholder_text="Product Price",
    width=250
)
product_price_entry.pack(pady=10)

product_stock_entry = ctk.CTkEntry(
    inventory_left,
    placeholder_text="Product Stock",
    width=250
)
product_stock_entry.pack(pady=10)

def save_product():
    name = product_name_entry.get().strip()
    price = product_price_entry.get()
    stock = product_stock_entry.get()

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
    
    load_products()
    load_inventory()

    messagebox.showinfo(
    "Product Added",
    f"{name} added successfully!"
    )

    product_name_entry.delete(0, "end")
    product_price_entry.delete(0, "end")
    product_stock_entry.delete(0, "end")

add_product_btn = ctk.CTkButton(
    inventory_left,
    text="Add Product", 
    width=200,
    height=40,
    command=save_product
)
add_product_btn.pack(pady=20)



#-------INVENTORY_PAGE------(Endss here)

# FUNCTION TO HIDE ALL EXISTING WIDGETS AND DISPLAY THE SELECTED ONE.
def show_page(page):
    for widget in main_content.winfo_children():
        widget.pack_forget()

    page.pack(fill="both", expand=True)







load_products()

def load_inventory():
    for widget in products_list_frame.winfo_children():
        widget.destroy()


    products = get_products()

    for product_id, name, price, stock in products:

        product_row = ctk.CTkFrame(
            products_list_frame,
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
        delete_btn = ctk.CTkButton(
            details_frame,
            text="Delete",
            width=70,
            height=28,
            fg_color="#D9534F",
            hover_color="#B52B27",
            command=lambda pid=product_id, pname=name: delete_inventory_product(pid, pname)
        )
        delete_btn.pack(side="right", padx=5)
        stock_label.pack(side="right")

load_inventory()


def delete_inventory_product(product_id, name):

    confirm = messagebox.askyesno(
        "Confirm Deletion",
        f"Are you sure you want to delete {name}?"
    )

    if not confirm:
        return

    delete_product(product_id)

    cart.pop(name, None)

    load_products()
    load_inventory()
    update_cart()




app.mainloop()