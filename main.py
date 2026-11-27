import customtkinter as ctk
from pages.inventory import InventoryPage
from database import create_tables
from pages.pos import POSPage
from pages.dashboard import DashboardPage

create_tables()

app = ctk.CTk()

app.title("GroceryPOS - Management System")
app.geometry("1000x600")


#-----SIDEBAR-----
sidebar = ctk.CTkFrame(app, width=200)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)



#-----MAIN_CONTENT------
main_content = ctk.CTkFrame(app)
main_content.pack(side="right", fill="both", expand=True)

#------PAGES------

dashboard_page = DashboardPage(main_content)
pos_page = POSPage(main_content)

inventory_page = InventoryPage(
    main_content,
    on_products_changed=pos_page.load_products
)

pos_page.on_sale_completed = inventory_page.load_inventory

#---TOUCHPAD SCROLLING WORKAROUND---

def decode_touchpad_delta(raw_delta):
    raw = raw_delta & 0xFFFFFFFF

    delta_y = raw & 0xFFFF

    if delta_y >= 0x8000:
        delta_y -= 0x10000

    return delta_y


def trackpad_scroll(event):

    delta_y = decode_touchpad_delta(event.delta)

    if not delta_y:
        return

    # Get the mouse pointer position
    pointer_x = event.x_root
    pointer_y = event.y_root

    # Check whether the pointer is inside a scrollable area
    def pointer_over(canvas):

        x = canvas.winfo_rootx()
        y = canvas.winfo_rooty()

        width = canvas.winfo_width()
        height = canvas.winfo_height()

        return (
            x <= pointer_x <= x + width
            and y <= pointer_y <= y + height
        )

    # POS page
    if pos_page.winfo_ismapped():

        product_canvas = pos_page.product_frame._parent_canvas
        cart_canvas = pos_page.cart_items_frame._parent_canvas

        if pointer_over(product_canvas):
            product_canvas.yview_scroll(-delta_y, "units")
            return "break"

        if pointer_over(cart_canvas):
            cart_canvas.yview_scroll(-delta_y, "units")
            return "break"

    # Inventory page
    if inventory_page.winfo_ismapped():

        inventory_canvas = (
            inventory_page.products_list_frame._parent_canvas
        )

        if pointer_over(inventory_canvas):
            inventory_canvas.yview_scroll(-delta_y, "units")
            return "break"

app.bind_all(
    "<TouchpadScroll>",
    trackpad_scroll,
    add="+"
)



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








# FUNCTION TO HIDE ALL EXISTING WIDGETS AND DISPLAY THE SELECTED ONE.
def show_page(page):
    for widget in main_content.winfo_children():
        widget.pack_forget()

    page.pack(fill="both", expand=True)








app.mainloop()