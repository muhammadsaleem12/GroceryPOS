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

dashboard_heading = ctk.CTkLabel(main_content, text="Dashboard Overview", font=ctk.CTkFont(size=26, weight="bold"))
dashboard_heading.pack(pady=30)

#----CARDS_CONTAINER----(FOR BETTER CONTROL)
cards_container = ctk.CTkFrame(main_content, fg_color="transparent")
cards_container.pack(fill="x", padx=20, pady=20)


#------SALES_CARD------
sales_card = ctk.CTkFrame(cards_container, width=250, height=130, fg_color="#FFFFFF", corner_radius=12, border_width=1)
sales_card.pack(side="left", pady=20, padx=20, anchor="n")
sales_card.pack_propagate(False)

first_s = ctk.CTkLabel(sales_card, text="Today's Sales", font=ctk.CTkFont(size=12, weight="bold"))
first_s.pack(pady=(12, 4))
second_s = ctk.CTkLabel(sales_card, text="$0.00", font=ctk.CTkFont(size=24, weight="bold"))
second_s.pack(pady=4)
third_s = ctk.CTkLabel(sales_card, text="Today's total revenue", wraplength=180, justify="center", font=ctk.CTkFont(size=12, weight="bold"))
third_s.pack(pady=4)

#------TRANSACTIONS_CARD------

transactions_card = ctk.CTkFrame(cards_container, width=250, height=130, fg_color="#FFFFFF", corner_radius=12, border_width=1)
transactions_card.pack(side="left", pady=20, padx=20, anchor="n")
transactions_card.pack_propagate(False)

first_t = ctk.CTkLabel(transactions_card, text="Total Transactions", font=ctk.CTkFont(size=12, weight="bold"))
first_t.pack(pady=(12, 4))
second_t = ctk.CTkLabel(transactions_card, text="0", font=ctk.CTkFont(size=24, weight="bold"))
second_t.pack(pady=(4))
third_t = ctk.CTkLabel(transactions_card, text="Today's transactions", wraplength=180, justify="center", font=ctk.CTkFont(size=12, weight="bold"))
third_t.pack(pady=(4))


#------RECENT_SALES_HISTORY-------

recent_sales_frame = ctk.CTkFrame(main_content, width=500, height=250, fg_color="#FFFFFF",corner_radius=12, border_width=1)
recent_sales_frame.pack(side="top", fill="x", padx=20, pady=20)
recent_sales_frame.pack_propagate(False)

#------RECENT_SALES_HEADING-------
recent_sales_heading = ctk.CTkLabel(recent_sales_frame, text="Recent Sales", font=ctk.CTkFont(size=20, weight="bold"))
recent_sales_heading.pack(pady=(4))

#------RECENT_SALES_TRANSACTIONS------
recent_sales_t1 = ctk.CTkLabel(recent_sales_frame, text="Receipt #001 | Walk-in | Rs. 1,500", font=ctk.CTkFont(size=12, weight="bold"))
recent_sales_t1.pack(pady=(4))
recent_sales_t1 = ctk.CTkLabel(recent_sales_frame, text="Receipt #002 | Walk-in | Rs. 850", font=ctk.CTkFont(size=12, weight="bold"))
recent_sales_t1.pack(pady=(4))
recent_sales_t1 = ctk.CTkLabel(recent_sales_frame, text="Receipt #003 | Walk-in | Rs. 2,200", font=ctk.CTkFont(size=12, weight="bold"))
recent_sales_t1.pack(pady=(4))













#------SIDEBAR_HEADIING------
heading = ctk.CTkLabel(sidebar, text="GroceryPOS", font=ctk.CTkFont(size=20, weight="bold"))
heading.pack(pady=30)


#------NEVIGATION------

dashboard = ctk.CTkButton(sidebar, text="Dashboard")
dashboard.pack(pady=15)

pos = ctk.CTkButton(sidebar, text="Point Of Sale")
pos.pack(pady=15)

inventory = ctk.CTkButton(sidebar, text="Inventory")
inventory.pack(pady=15)

sales = ctk.CTkButton(sidebar, text="Sales")
sales.pack(pady=15)


app.mainloop()