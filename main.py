import customtkinter as ctk
import mysql.connector
from tkinter import messagebox
from settings import *
from tkinter.ttk import Treeview, Style
from tkinter import W


class Cart(Treeview):
    def __init__(self, master, small_font, big_font):
        super().__init__(
            master,
            style="Cart.Treeview",
            show="headings",
            columns=("Name", "Price", "Qty", "Total price"),
            selectmode="browse")

        self.scrollbar = ctk.CTkScrollbar(
            master, orientation="vertical", command=self.yview)

        self.small_font = small_font
        self.big_font = big_font

        self.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.place(relx=0.981, rely=0.02, relheight=0.7)

        self.bind('<<TreeviewSelect>>', self.item_selected)

        self.create_style()
        
        self.create_widgets(master)

        self.heading("Name", text="Name", anchor=W)
        self.heading("Price", text="Price", anchor=W)
        self.heading("Qty", text="Qty", anchor=W)
        self.heading("Total price", text="Total price", anchor=W)
        self.place(relx=0.48, rely=0.02, relwidth=0.5, relheight=0.7)
        self.column_width()

    def create_widgets(self, master):
        # Qty label
        self.qty_label = ctk.CTkLabel(
            master,
            font=self.big_font,
            text="Qty:")

        self.qty_label.place(relx=0.48, rely=0.73)

        self.qty_text = ctk.StringVar(value="")

        self.qty_text.trace_add("write", self.update_total_price)

        self.qty_entry = ctk.CTkEntry(
            master,
            textvariable=self.qty_text,
            font=self.small_font,
            state="readonly")
        
        self.qty_entry.place(relx=0.48, rely=0.78, relwidth=0.06)
        
        # Total price label
        total_price_label = ctk.CTkLabel(
            master,
            font=self.big_font,
            text="Total Price:")

        total_price_label.place(relx=0.55, rely=0.73)

        # Total price entry
        self.total_price = ctk.StringVar(value="")

        self.total_price_entry = ctk.CTkEntry(
            master,
            font=self.small_font,
            state="readonly",
            textvariable=self.total_price)

        self.total_price_entry.place(relx=0.553, rely=0.78)

        self.update_btn = ctk.CTkButton(
            master,
            text="Update Qty",
            command=self.update_btn_command)

        self.update_btn.place(relx=0.48, rely=0.83)

    def column_width(self):
        width = round(self.winfo_screenwidth() / 2)
        width = round(width / 10)

        self.column("Name", width=width*5)
        self.column("Price", width=width*2)
        self.column("Qty", width=width*1)
        self.column("Total price", width=width*2)

    def create_style(self):
        style = Style()
        style.theme_use("default")

        style.configure(
            "Cart.Treeview",
            background="#45474a",
            foreground="#dce4ee",
            fieldbackground="#45474a",
            borderwidth=0,
            rowheight=25,
            font=("Arial", 14))
        ctk.CTkLabel
        style.map("Cart.Treeview", background=[("selected", "#3e4b6b")])
        style.configure(
            'Cart.Treeview.Heading',
            foreground='#dce4ee',
            background="#8c9096",
            font=('Arial', 17),
            relief="flat",
            padding=5)

    def update_qty(self, item_name, qty, add):
        values = self.item(item_name)["values"]

        old_qty = values[2]
        if add:
            new_qty = int(old_qty) + int(qty)
        else:
            new_qty = int(qty)

        new_total_price = str(round(float(values[1]), 2) * new_qty)

        self.item(item_name,
                  values=(item_name, values[1], new_qty, new_total_price))

    def add(self, item_name, item_price, qty, total_price):

        if self.exists(item_name):
            self.update_qty(item_name, qty, True)

        else:
            self.insert(
                parent="",
                index="end",
                iid=item_name,
                values=(
                    item_name,
                    item_price,
                    qty,
                    total_price))

    def update_btn_command(self):
        qty_text = self.qty_text.get()
        item = self.selection()
        if len(item) != 0:
            if qty_text.isdigit() and int(qty_text) != 0:
                self.update_qty(item[0], qty_text, False)

                self.qty_text.set("")
                self.qty_entry.configure(state="readonly")
                self.total_price.set("")

    def item_selected(self, *_):
        item = self.selection()[0]

        self.qty_text.set(str(self.item(item)["values"][2]))
        self.qty_entry.configure(state="normal")

    def update_total_price(self, *_):
        qty_text = self.qty_text.get()
        if qty_text.isdigit():
            item = self.selection()[0]
            item_price = self.item(item)["values"][1]

            total_price = str(round(int(qty_text) * round(float(item_price), 2), 2))

            self.total_price.set(total_price)



            


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self._set_appearance_mode("dark")

        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Hi1234.",
            database="supermarket")

        self.main_frame = ctk.CTkTabview(self, segmented_button_fg_color=GREY)
        self.main_frame.add("Cashier")
        self.main_frame.add("Admin")
        self.main_frame.place(x=0, rely=0.01, relwidth=1, relheight=0.99)
        self.aspect_ratio()
        self.create_main_frame_items()

        self.enter = False

        # Zoomed state
        self.after(1, lambda: self.state("zoomed"))

        self.mainloop()

    def aspect_ratio(self):
        self.MAIN_BIG_FONT = (MAIN_BIG_FONT_ESH[0], round(
            self.winfo_screenwidth() * MAIN_BIG_FONT_ESH[1] / 1920))

        self.MAIN_SMALL_FONT = (MAIN_SMALL_FONT_ESH[0], round(
            self.winfo_screenwidth() * MAIN_SMALL_FONT_ESH[1] / 1920))

    def create_main_frame_items(self):
        frame = self.main_frame.tab("Cashier")
        self.cart = Cart(frame, self.MAIN_SMALL_FONT, self.MAIN_BIG_FONT)

        self.entry_text = ctk.StringVar(value="")

        entry = ctk.CTkEntry(
            frame,
            textvariable=self.entry_text,
            font=self.MAIN_BIG_FONT)

        entry.place(relx=0.005, rely=0.01, relwidth=0.3, anchor="nw")

        entry.bind("<Return>", self.enter)

        self.auto_add = ctk.IntVar(value=1)
        auto_add = ctk.CTkSwitch(
            frame,
            variable=self.auto_add,
            text="Auto add",
            font=self.MAIN_SMALL_FONT,
            switch_width=48,
            switch_height=24)
        
        auto_add.place(relx=0.01, rely=0.12)

        button = ctk.CTkButton(
            frame,
            command=self.retrieve_items,
            text="Search",
            font=self.MAIN_SMALL_FONT)

        button.place(relx=0.007, rely=0.07, relheight=0.04)

        button_two = ctk.CTkButton(
            frame,
            command=self.search_and_add,
            text="Search and add",
            font=self.MAIN_SMALL_FONT)

        button_two.place(relx=0.1, rely=0.07, relheight=0.04)

        # First label
        first_label = ctk.CTkLabel(
            frame,
            font=self.MAIN_BIG_FONT,
            text="Item name:")

        first_label.place(relx=0.005, rely=0.2)

        # Second label
        second_label = ctk.CTkLabel(
            frame,
            font=self.MAIN_BIG_FONT,
            text="Item Price:")

        second_label.place(relx=0.205, rely=0.2)

        # Item name
        self.item_name = ctk.StringVar(value="")
        self.item_name_label = ctk.CTkEntry(
            frame,
            font=self.MAIN_SMALL_FONT,
            state="readonly",
            textvariable=self.item_name)

        self.item_name_label.place(relx=0.0054, rely=0.3, relwidth=0.15)

        # Item price
        self.item_price = ctk.StringVar(value="")
        self.item_price_label = ctk.CTkEntry(
            frame,
            font=self.MAIN_SMALL_FONT,
            state="readonly",
            textvariable=self.item_price)

        self.item_price_label.place(relx=0.2054, rely=0.3)

        # Qty var
        self.qty_text = ctk.StringVar(value="1")
        self.qty_text.trace_add("write", self.update_total_price)

        # Qty label
        self.qty_label = ctk.CTkLabel(
            frame,
            font=self.MAIN_BIG_FONT,
            text="Qty:")

        self.qty_label.place(relx=0.0054, rely=0.361)

        # Qty entry
        self.qty_entry = ctk.CTkEntry(
            frame,
            textvariable=self.qty_text,
            font=self.MAIN_SMALL_FONT)
        
        self.qty_entry.place(relx=0.006, rely=0.423, relwidth=0.023)

        # Total price label
        total_price_label = ctk.CTkLabel(
            frame,
            font=self.MAIN_BIG_FONT,
            text="Total Price:")

        total_price_label.place(relx=0.07, rely=0.361)

        # Total price entry
        self.total_price = ctk.StringVar(value="")

        self.total_price_entry = ctk.CTkEntry(
            frame,
            font=self.MAIN_SMALL_FONT,
            state="readonly",
            textvariable=self.total_price)

        self.total_price_entry.place(relx=0.075, rely=0.423)

        # Add to cart button
        self.add_btn = ctk.CTkButton(
            self, text="Add to cart", command=self.add_to_cart)

        self.add_btn.place(relx=0.01, rely=0.53, relwidth=0.08)

    def retrieve_items(self):
        barcode = self.entry_text.get()
        if barcode.isdigit():
            cursor = self.db.cursor()
            command = f"""
            SELECT name, price 
            FROM items
            WHERE barcode_id = {barcode};"""
        else:
            return

        cursor.execute(command)
        result = cursor.fetchone()

        if result is not None:
            self.item_name.set(result[0])  # Name
            self.item_price.set(str(result[1]))  # Price

            self.qty_text.set("1")
        else:
            messagebox.showerror(
                "Item not found",
                "Item is not registered",
                icon=messagebox.ERROR)

        cursor.close()

    def update_total_price(self, *_):
        item_price = self.item_price_label.get()
        qty_text = self.qty_text.get()
        if item_price != "" and qty_text != "":
            if qty_text.isdigit():
                result = round(round(float(item_price), 2) * int(qty_text), 2)
                self.total_price.set(str(result))
                self.last_qty_text = qty_text
            else:
                self.qty_text.set(self.last_qty_text)

    def add_to_cart(self):
        if self.item_name.get() != "":

            item_name = self.item_name.get()
            item_price = self.item_price.get()
            qty_text = self.last_qty_text
            total_price = self.total_price.get()

            self.cart.add(
                item_name=item_name,
                item_price=item_price,
                qty=qty_text,
                total_price=total_price)

            self.entry_text.set("")
            self.item_name.set("")
            self.item_price.set("")
            self.qty_text.set("")
            self.total_price.set("")

    def search_and_add(self):
        self.retrieve_items()
        self.add_to_cart()

    def enter(self, event):
        if event.state == 0 and self.entry_text.get() != "" and self.auto_add.get():
            self.search_and_add()

        
App()
