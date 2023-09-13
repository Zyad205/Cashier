import customtkinter as ctk
import sqlite3
from tkinter import messagebox
from settings import *
from tkinter.ttk import Treeview, Style
from tkinter import W


class AdminPanel:
    
    def __init__(self, master, very_small_font, small_font, big_font):
        self.master = master
        self.signed_in = False
        self.create_sign_in(small_font)
        self.create_main_items(very_small_font, small_font, big_font)
        
        self.very_small_font = very_small_font
        self.small_font = small_font
        self.big_font = big_font

        self.db = sqlite3.connect("supermarket.db")

        self.get_all_items()

        self.add_item_window = None
        
    def create_sign_in(self, font):
        self.sign_in_frame = ctk.CTkFrame(self.master)
        frame = self.sign_in_frame
        
        label = ctk.CTkLabel(frame, text="Enter root password: ", font=font)

        self.entry_text = ctk.StringVar(value="")

        entry = ctk.CTkEntry(frame, textvariable=self.entry_text, show="*", font=font)

        button = ctk.CTkButton(frame, text="Enter", command=self.check_password, font=font)

        label.place(relx=0.03, rely=0.1)
        entry.place(relx=0.03, rely=0.5, relwidth=0.6, relheight=0.35)
        button.place(relx=0.67, rely=0.5, relwidth=0.3, relheight=0.35)

    def get_all_items(self):
        cus = self.db.cursor()

        cus.execute("SELECT * FROM items;")

        result = cus.fetchall()

        for item in result:
            self.treeview.insert(parent="", index="end", iid=item[0], values=item)

        cus.close()

    def create_main_items(self, very_small_font, small_font, big_font):
        self.main_frame = ctk.CTkFrame(self.master, fg_color="transparent")

        self.create_style(very_small_font)

        self.create_treeview()

        barcode_label = ctk.CTkLabel(self.main_frame, text="Barcode:", font=big_font)

        self.barcode_text = ctk.StringVar(value="")

        barcode_entry = ctk.CTkEntry(
            self.main_frame,
            textvariable=self.barcode_text,
            font=very_small_font,
            state="readonly")
    
        name_label = ctk.CTkLabel(self.main_frame, text="Name:", font=big_font)

        self.name_text = ctk.StringVar(value="")

        name_entry = ctk.CTkEntry(
            self.main_frame,
            textvariable=self.name_text,
            font=very_small_font)

        price_label = ctk.CTkLabel(self.main_frame, text="Price:", font=big_font)

        self.price_text = ctk.StringVar(value="")

        price_entry = ctk.CTkEntry(
            self.main_frame,
            textvariable=self.price_text,
            font=very_small_font)
        
        update_btn = ctk.CTkButton(
            self.main_frame,
            text="Update item",
            command=self.update_item,
            font=very_small_font)
        
        delete_btn = ctk.CTkButton(
            self.main_frame,
            text="Delete item",
            command=self.delete_item,
            font=very_small_font,
            fg_color="#b3b5aa",
            hover_color="red")
        
        add_btn = ctk.CTkButton(
            self.main_frame,
            text="Add item",
            command=self.add_item_window,
            font=very_small_font,
            fg_color="#ccf7a1",
            hover_color="#daf5bf",
            text_color="#7c7d7a")
        
        barcode_entry.place(relx=0.001, rely=0.8, relwidth=0.085)
        barcode_label.place(relx=0.001, rely=0.75)
        name_label.place(relx=0.1, rely=0.75)
        name_entry.place(relx=0.1, rely=0.8, relwidth=0.15)
        price_label.place(relx=0.26, rely=0.75)
        price_entry.place(relx=0.26, rely=0.8, relwidth=0.06)
        update_btn.place(relx=0.001, rely=0.85, relwidth=0.07, relheight=0.035)
        delete_btn.place(relx=0.08, rely=0.85, relwidth=0.07, relheight=0.035)
        add_btn.place(relx=0.001, rely=0.9, relheight=0.09, relwidth=0.07)

    def create_treeview(self):

        self.treeview = Treeview(
            self.main_frame,
            style="Admin.Treeview",
            show="headings",
            columns=("Barcode", "Name", "Price"),
            selectmode="browse")

        self.scrollbar = ctk.CTkScrollbar(
            self.main_frame, orientation="vertical", command=self.treeview.yview)

        self.treeview.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.place(relx=0.501, rely=0.02, relheight=0.7)

        self.treeview.bind('<<TreeviewSelect>>', self.item_selected)

        self.treeview.heading("Barcode", text="Barcode", anchor=W)
        self.treeview.heading("Name", text="Name", anchor=W)
        self.treeview.heading("Price", text="Price", anchor=W)

        self.treeview.place(relx=0.001, rely=0.02, relwidth=0.5, relheight=0.7)
        self.column_width()

    def create_style(self, very_small_font):
        style = Style()
        style.theme_use("default")

        style.configure(
            "Admin.Treeview",
            background="#b3b5aa",
            foreground="#d4fff7",
            fieldbackground="#b3b5aa",
            borderwidth=0,
            rowheight=25,
            font=very_small_font)
        ctk.CTkLabel
        style.map("Admin.Treeview", background=[("selected", "#807e7d")])
        style.configure(
            'Admin.Treeview.Heading',
            foreground='#f5d07a',
            background="#ed8a00",
            font=('Arial', 17),
            relief="flat",
            padding=5)
    
    def check_password(self):
        if self.entry_text.get() == "1":
            self.sign_in_frame.place_forget()
            self.main_frame.place(x=0, y=0, relwidth=1, relheight=1)
            self.entry_text.set("")

    def check_signed_in(self):
        if not self.signed_in:
            self.sign_in_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.2, relheight=0.1)
            self.main_frame.place_forget()
        else:
            self.main_frame.place(x=0, y=0, relwidth=1, relheight=1)

    def column_width(self):
        width = round(self.master.winfo_screenwidth() / 2)
        width = round(width / 10)

        self.treeview.column("Barcode", width=width*4)
        self.treeview.column("Name", width=width*4)
        self.treeview.column("Price", width=width*2)
    
    def update_item(self):
        name_text = self.name_text.get()
        if not name_text.isspace():
            try:
                price = round(float(self.price_text.get()), 2)
                if price > 0:
                    item = self.treeview.selection()
                    if len(item) == 1:

                        cus = self.db.cursor()
                        barcode = self.treeview.item(item[0])["values"][0]
    
                        cus.execute("""UPDATE items
                                    SET name = ?, price = ?
                                    WHERE barcode = ?""", [name_text, price, barcode])
                        self.db.commit()
                        cus.close()
    
                        self.treeview.item(item[0], values=(item[0], name_text, price))
    
            except ValueError:
                pass    
                
    def item_selected(self, _):
        item = self.treeview.selection()
        if len(item) == 1:
            result = self.treeview.item(item[0])["values"]
            
            self.barcode_text.set(result[0])
            self.name_text.set(result[1])
            self.price_text.set(result[2])

    def delete_item(self):
        item = self.treeview.selection()
        if len(item) == 1:
            cus = self.db.cursor()

            barcode = self.treeview.item(item[0])["values"][0]

            cus.execute("""DELETE FROM items
                        WHERE barcode = ?""", [barcode])

            self.db.commit()
            cus.close()

            self.treeview.delete(item[0])

            self.barcode_text.set("")
            self.name_text.set("")
            self.price_text.set("")
    
    def add_item_window(self):
        if self.add_item_window is None or not self.add_item_window.winfo_exists():
            self.add_item_window = ctk.CTkToplevel()
            frame = self.add_item_window

            frame.title("Add item")
            frame.geometry(f"450x130")
            frame.resizable(True, False)

            small_font = ("Arial", 20)
            very_small_font = ("Arial", 15)

            # Barcode label
            barcode = ctk.CTkLabel(frame, text="Barcode:", font=small_font)
            # Barcode entry
            self.aiw_barcode_text = ctk.StringVar(value="")
            barcode_entry = ctk.CTkEntry(frame, textvariable=self.aiw_barcode_text, font=very_small_font)

            # Name label
            name = ctk.CTkLabel(frame, text="Name:", font=small_font)
            # Name entry
            self.aiw_name_text = ctk.StringVar(value="")
            name_entry = ctk.CTkEntry(frame, textvariable=self.aiw_name_text, font=very_small_font)

            # Price label
            price = ctk.CTkLabel(frame, text="Price:", font=small_font)
            # Price entry
            self.aiw_price_text = ctk.StringVar(value="")
            price_entry = ctk.CTkEntry(frame, textvariable=self.aiw_price_text, font=very_small_font)

            # Add button
            btn = ctk.CTkButton(frame, text="Add item", font=very_small_font, command=self.add_item)

            # Placing
            barcode.place(relx=0.005, rely=0.001)
            barcode_entry.place(relx=0.01, rely=0.3, relwidth=0.22)
            name.place(relx=0.25, rely=0.001)
            name_entry.place(relx=0.25, rely=0.3, relwidth=0.3)
            price.place(relx=0.57, rely=0.001)
            price_entry.place(relx=0.57, rely=0.3, relwidth=0.15)
            btn.place(relx=0.75, rely=0.3, relwidth=0.2)
        else:
            self.add_item_window.focus()
        
    def add_item(self):
        barcode = self.aiw_barcodd_text.get()
        name = self.aiw_name_text.get()
        price = self.aiw_price_text.get()
        if barcode.isdigit() and not name.isspace():
            try:
                price = round(float(price), 2)    
                cus = self.db.cursor()

                self.treeview.insert(parnet="", index="end", iid=barcode, values=(barcode, name, price))

   
    
              
            except ValueError:
                pass



 


class Cart(Treeview):

    def __init__(self, master, very_small_font, small_font, big_font):
        super().__init__(
            master,
            style="Cart.Treeview",
            show="headings",
            columns=("Name", "Price", "Qty", "Total price"),
            selectmode="browse")
        
        self.total_price = 0

        self.scrollbar = ctk.CTkScrollbar(
            master, orientation="vertical", command=self.yview)

        self.very_small_font = very_small_font
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

        self.qty_text = ctk.StringVar(value="")
        self.qty_text.trace_add("write", self.update_qty_total_price)

        self.qty_entry = ctk.CTkEntry(
            master,
            textvariable=self.qty_text,
            font=self.small_font,
            state="readonly")
        
        # Total price label
        qty_total_price_label = ctk.CTkLabel(
            master,
            font=self.big_font,
            text=" Total Price:")

        # Total price entry
        self.qty_total_price = ctk.StringVar(value="")

        self.qty_total_price_entry = ctk.CTkEntry(
            master,
            font=self.small_font,
            state="readonly",
            textvariable=self.qty_total_price)

        self.update_btn = ctk.CTkButton(
            master,
            text="Update Qty",
            command=self.update_btn_command,
            font=self.very_small_font)

        delete_btn = ctk.CTkButton(
            master,
            text="Delete selected item",
            command=self.delete_item,
            font=self.very_small_font)

        total_price_label = ctk.CTkLabel(
            master,
            font=self.big_font,
            text=" Total Price:")

        # Total price entry
        self.total_price_text = ctk.StringVar(value="")

        self.total_price_entry = ctk.CTkEntry(
            master,
            font=self.small_font,
            state="readonly",
            textvariable=self.total_price_text)
        
        self.qty_label.place(relx=0.48, rely=0.73)
        self.qty_entry.place(relx=0.48, rely=0.78, relwidth=0.06)
        qty_total_price_label.place(relx=0.545, rely=0.73)
        self.qty_total_price_entry.place(relx=0.553, rely=0.78)
        self.update_btn.place(relx=0.48, rely=0.83, relwidth=0.05, relheight=0.03)
        delete_btn.place(relx=0.54, rely=0.83, relwidth=0.09, relheight=0.03)
        total_price_label.place(relx=0.86, rely=0.73)
        self.total_price_entry.place(relx=0.87, rely=0.78, relwidth=0.1)

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
            font=self.very_small_font)
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

        self.update_total_price(False)

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
            
            self.update_total_price(True, round(float(total_price), 2))

    def update_btn_command(self):
        qty_text = self.qty_text.get()
        item = self.selection()
        if len(item) != 0:
            if qty_text.isdigit() and int(qty_text) != 0:
                self.update_qty(item[0], qty_text, False)

                self.qty_text.set("")
                self.qty_entry.configure(state="readonly")
                self.qty_total_price.set("")

    def item_selected(self, *_):
        item = self.selection()
        if len(item) != 0:
            item = item[0]
            self.qty_text.set(str(self.item(item)["values"][2]))
            self.qty_entry.configure(state="normal")

    def update_qty_total_price(self, *_):
        qty_text = self.qty_text.get()
        if qty_text.isdigit():
            item = self.selection()[0]
            item_price = self.item(item)["values"][1]

            total_price = str(round(int(qty_text) * round(float(item_price), 2), 2))

            self.qty_total_price.set(total_price)

    def delete_item(self):
        item = self.selection()
        if len(item) != 0:
            self.delete(item[0])

    def update_total_price(self, add, total_price=None):
        if add:
            self.total_price = round(self.total_price + total_price, 2)
            self.total_price_text.set(str(self.total_price))
        else:
            children = self.get_children()

            self.total_price = 0
            for child in children:
                value = self.item(child)["values"][3]

                self.total_price = round(self.total_price + round(float(value), 2), 2)
                
            self.total_price_text.set(str(self.total_price))


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self._set_appearance_mode("dark")

        self.db = sqlite3.connect("supermarket.db")

        self.check_table()

        self.main_frame = ctk.CTkTabview(self, segmented_button_fg_color=GREY,
                                         command=self.main_frame_func)
        self.main_frame.add("Cashier")
        self.main_frame.add("Admin")
        self.main_frame.place(x=0, rely=0.01, relwidth=1, relheight=0.99)

        self.aspect_ratio()
        self.create_main_frame_items()

        self.admin_panel = AdminPanel(
            self.main_frame.tab("Admin"),
            self.VERY_SMALL_FONT,
            self.SMALL_FONT,
            self.BIG_FONT)

        self.enter = False

        # Zoomed state
        self.after(1, lambda: self.state("zoomed"))
        
        self.mainloop()

    def check_table(self):
        cursor = self.db.cursor()

        command = """CREATE TABLE IF NOT EXISTS items (
            barcode INT PRIMARY KEY,
            name TEXT,
            price DECIMAL(20, 2)
        );"""

        cursor.execute(command)
        self.db.commit()
        cursor.close()

    def aspect_ratio(self):
        self.BIG_FONT = (BIG_FONT_ESH[0], round(
            self.winfo_screenwidth() * BIG_FONT_ESH[1] / 1920))

        self.SMALL_FONT = (SMALL_FONT_ESH[0], round(
            self.winfo_screenwidth() * SMALL_FONT_ESH[1] / 1920))

        self.VERY_SMALL_FONT = (VERY_SMALL_FONT_ESH[0], round(
            self.winfo_screenwidth() * VERY_SMALL_FONT_ESH[1] / 1920))
        
    def create_main_frame_items(self):
        frame = self.main_frame.tab("Cashier")
        self.cart = Cart(frame, self.VERY_SMALL_FONT, self.SMALL_FONT, self.BIG_FONT)

        self.entry_text = ctk.StringVar(value="")

        entry = ctk.CTkEntry(
            frame,
            textvariable=self.entry_text,
            font=self.BIG_FONT)
        entry.bind("<Return>", self.enter)

        self.auto_add = ctk.IntVar(value=1)
        auto_add = ctk.CTkSwitch(
            frame,
            variable=self.auto_add,
            text="Auto add",
            font=self.SMALL_FONT,
            switch_width=48,
            switch_height=24)
        

        button = ctk.CTkButton(
            frame,
            command=self.retrieve_items,
            text="Search",
            font=self.SMALL_FONT)

        button_two = ctk.CTkButton(
            frame,
            command=self.search_and_add,
            text="Search and add",
            font=self.SMALL_FONT)

        # First label
        first_label = ctk.CTkLabel(
            frame,
            font=self.BIG_FONT,
            text="Item name:")

        # Second label
        second_label = ctk.CTkLabel(
            frame,
            font=self.BIG_FONT,
            text="Item Price:")

        # Item name
        self.item_name = ctk.StringVar(value="")
        self.item_name_label = ctk.CTkEntry(
            frame,
            font=self.SMALL_FONT,
            state="readonly",
            textvariable=self.item_name)

        # Item price
        self.item_price = ctk.StringVar(value="")
        self.item_price_label = ctk.CTkEntry(
            frame,
            font=self.SMALL_FONT,
            state="readonly",
            textvariable=self.item_price)

        # Qty var
        self.qty_text = ctk.StringVar(value="1")
        self.qty_text.trace_add("write", self.update_total_price)

        # Qty label
        self.qty_label = ctk.CTkLabel(
            frame,
            font=self.BIG_FONT,
            text="Qty:")

        # Qty entry
        self.qty_entry = ctk.CTkEntry(
            frame,
            textvariable=self.qty_text,
            font=self.SMALL_FONT)

        # Total price label
        total_price_label = ctk.CTkLabel(
            frame,
            font=self.BIG_FONT,
            text="Total Price:")

        # Total price entry
        self.total_price = ctk.StringVar(value="")

        self.total_price_entry = ctk.CTkEntry(
            frame,
            font=self.SMALL_FONT,
            state="readonly",
            textvariable=self.total_price)

        # Add to cart button
        self.add_btn = ctk.CTkButton(
            frame, text="Add to cart", command=self.add_to_cart)


        entry.place(relx=0.005, rely=0.01, relwidth=0.3, anchor="nw")
        auto_add.place(relx=0.01, rely=0.12)
        button.place(relx=0.007, rely=0.07, relheight=0.04, relwidth=0.09)
        button_two.place(relx=0.11, rely=0.07, relheight=0.04, relwidth=0.1)
        first_label.place(relx=0.005, rely=0.2)
        second_label.place(relx=0.205, rely=0.2)
        self.item_name_label.place(relx=0.0054, rely=0.3, relwidth=0.15)
        self.item_price_label.place(relx=0.2054, rely=0.3)
        self.qty_label.place(relx=0.0054, rely=0.361)
        self.qty_entry.place(relx=0.006, rely=0.423, relwidth=0.023)
        total_price_label.place(relx=0.07, rely=0.361)
        self.total_price_entry.place(relx=0.075, rely=0.423)
        self.add_btn.place(relx=0.01, rely=0.5, relwidth=0.08)

    def retrieve_items(self):
        barcode = self.entry_text.get()
        if barcode.isdigit():
            cursor = self.db.cursor()
            command = """
            SELECT name, price 
            FROM items
            WHERE barcode = ?;"""
        else:
            return

        cursor.execute(command, [barcode])
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

    def main_frame_func(self):

        if self.main_frame.get() == "Admin":
            self.admin_panel.check_signed_in()
        else:
            self.admin_panel.signed_in = False
        

App()
 
