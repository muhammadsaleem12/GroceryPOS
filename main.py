import customtkinter as ctk

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

product_frame = ctk.CTkFrame(pos_page)
product_frame.pack(
    side="left", 
    fill="both", 
    expand=True, 
    padx=20, 
    pady=10
)
product_frame.pack_propagate(False)

cart_frame = ctk.CTkFrame(pos_page, width=280)
cart_frame.pack(
    side="right", 
    fill="both", 
    expand=True,
    padx=20,
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

cart_total = ctk.CTkLabel(
    cart_frame, 
    text="Total: $0.00", 
    font=ctk.CTkFont(size=20, weight="bold")
)
cart_total.pack(pady=20)

checkout_btn = ctk.CTkButton(
    cart_frame, 
    text="Checkout", 
    height=40, 
    font=ctk.CTkFont(size=15, weight="bold")
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

cart_items_frame = ctk.CTkFrame(cart_frame)
cart_items_frame.pack(
    fill="both", 
    expand=True, 
    padx=10, 
    pady=10
)

#-----CART_FUNCTION------
cart = {}
discount_percentage = 0
product_prices = {
    "Milk": 3.00,
    "Bread": 2.50,
    "Eggs": 4.00
}

def add_to_cart(product):
    if product in cart:
        cart[product] += 1
    else:
        cart[product] = 1

    update_cart()

def calculate_total():
    total = 0 
    for product, quantity in cart.items():
        amount = quantity * product_prices[product]
        total += amount
        try:
            discount_percentage = float(discount_entry.get() or 0)
        except ValueError:
            discount_percentage = 0
        if discount_percentage < 0 or discount_percentage > 100:
            discount_percentage = 0
        discount = total * (discount_percentage / 100)
        total -= discount
    return total

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
    cart_total.configure(text=f"Total: ${calculate_total():.2f}")


#-----Products-----(starts here) 
milk_btn = ctk.CTkButton(
    product_frame, 
    text="Milk - $3.00", 
    width=150, 
    height=50, 
    command=lambda: add_to_cart("Milk")
)
milk_btn.pack(pady=5)

bread_btn = ctk.CTkButton(
    product_frame, 
    text="Bread - $2.50", 
    width=150, 
    height=50, 
    command=lambda: add_to_cart("Bread")
)
bread_btn.pack(pady=5)

eggs_btn = ctk.CTkButton(
    product_frame, 
    text="Eggs - $4.00",
    width=150,
    height=50, 
    command=lambda: add_to_cart("Eggs")
)
eggs_btn.pack(pady=5)


#------Products------(Ends here)

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
    text="Inventory"
)
inventory.pack(pady=15)

sales = ctk.CTkButton(
    sidebar, 
    text="Sales"
)
sales.pack(pady=15)




# FUNCTION TO HIDE ALL EXISTING WIDGETS AND DISPLAY THE SELECTED ONE.
def show_page(page):
    for widget in main_content.winfo_children():
        widget.pack_forget()

    page.pack(fill="both", expand=True)










app.mainloop()