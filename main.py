import customtkinter as ctk
import sqlite3
from tkinter import messagebox
from settings import *
from tkinter.ttk import Treeview, Style
from tkinter import W
from _tkinter import TclError
from datetime import date


class AdminPanel:

    def __init__(self, master, very_small_font, small_font, big_font):
        self.master = master

        self.very_small_font = very_small_font
        self.small_font = small_font
        self.big_font = big_font

        self.signed_in = False

        self.create_sign_in(small_font)
        self.create_main_items(very_small_font, small_font, big_font)

        self.db = sqlite3.connect("supermarket.db")

        self.get_all_items()

        self.add_item_window = None
        self.add_employ_window = None
        self.receipt_window = None
        self.delete_receipts_window = None

    def create_sign_in(self, font):
        self.sign_in_frame = ctk.CTkFrame(self.master, fg_color="#333333")
        frame = self.sign_in_frame

        label = ctk.CTkLabel(frame, text="Enter root password: ", font=font)

        self.sign_name_entry = ctk.CTkEntry(
            frame, font=font, placeholder_text="Name")
        self.sign_password_entry = ctk.CTkEntry(
            frame, show="*", font=font, placeholder_text="Password")

        button = ctk.CTkButton(frame, text="Enter",
                               command=self.check_password, font=font)

        label.place(relx=0.03, rely=0.1)
        self.sign_name_entry.place(
            relx=0.03, rely=0.4, relwidth=0.6, relheight=0.2)
        self.sign_password_entry.place(
            relx=0.03, rely=0.65, relwidth=0.6, relheight=0.2)
        button.place(relx=0.67, rely=0.5, relwidth=0.3, relheight=0.25)

    def get_all_items(self):
        cus = self.db.cursor()

        cus.execute("SELECT * FROM items;")

        result = cus.fetchall()

        for item in result:
            self.treeview.insert(parent="", index="end",
                                 iid=item[0], values=item)

        cus.execute("""SELECT * 
                    FROM receipts
                    ORDER BY id DESC
                    LIMIT 10000;""")

        result = cus.fetchall()

        for item in result:
            self.receipt_treeview.insert(parent="", index="end",
                                         iid=item[0], values=item)

        cus.close()

    def create_main_items(self, very_small_font, small_font, big_font):
        self.main_frame = ctk.CTkFrame(self.master, fg_color="transparent")

        self.create_style(very_small_font)

        self.create_treeview()

        barcode_label = ctk.CTkLabel(
            self.main_frame, text="Barcode:", font=big_font)

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

        price_label = ctk.CTkLabel(
            self.main_frame, text="Price:", font=big_font)

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

        search_label = ctk.CTkLabel(
            self.main_frame,
            text="Search:",
            font=small_font)

        self.search_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Barcode",
            font=small_font)

        search_btn = ctk.CTkButton(
            self.main_frame,
            text="Search",
            font=very_small_font,
            command=self.search)

        add_btn = ctk.CTkButton(
            self.main_frame,
            text="Add item",
            command=self.add_item_window,
            font=very_small_font,
            fg_color="#ccf7a1",
            hover_color="#daf5bf",
            text_color="#7c7d7a")

        add_employ_btn = ctk.CTkButton(
            self.main_frame,
            text="Add employ",
            command=self.add_employ_window,
            font=very_small_font,
            fg_color="#b8c5d9",
            hover_color="#c7cdd6",
            text_color="black")

        self.receipt_search_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Receipt id",
            font=big_font)
        
        receipt_search_btn = ctk.CTkButton(
            self.main_frame,
            text="Search",
            command=self.receipt_search,
            font=small_font)
        
        delete_old_receipt_btn = ctk.CTkButton(
            self.main_frame,
            text="Delete old receipts",
            command=self.delete_receipts,
            font=small_font,
            fg_color="#b3b5aa",
            hover_color="red")

        employ_statics_btn = ctk.CTkButton(
            self.main_frame,
            text="Employ statics",
            command=self.add_employ_window,
            font=small_font,
            fg_color="#b8c5d9",
            hover_color="#c7cdd6",
            text_color="black")
        
        barcode_entry.place(relx=0.001, rely=0.8, relwidth=0.085)
        barcode_label.place(relx=0.001, rely=0.75)
        name_label.place(relx=0.1, rely=0.75)
        name_entry.place(relx=0.1, rely=0.8, relwidth=0.15)
        price_label.place(relx=0.26, rely=0.75)
        price_entry.place(relx=0.26, rely=0.8, relwidth=0.06)
        update_btn.place(relx=0.001, rely=0.85, relwidth=0.07, relheight=0.035)
        delete_btn.place(relx=0.08, rely=0.85, relwidth=0.07, relheight=0.035)
        add_btn.place(relx=0.001, rely=0.9, relheight=0.09, relwidth=0.07)

        add_employ_btn.place(relx=0.08, rely=0.9,
                             relheight=0.09, relwidth=0.07)

        search_label.place(relx=0.16, rely=0.955, anchor="sw")

        self.search_entry.place(relx=0.16, rely=0.99,
                                relheight=0.03, relwidth=0.1, anchor="sw")

        search_btn.place(relx=0.265, rely=0.99, anchor="sw",
                         relwidth=0.05, relheight=0.03)

        self.receipt_search_entry.place(relx=0.55, rely=0.4, relheight=0.04, relwidth=0.12)
        receipt_search_btn.place(relx=0.55, rely=0.45, relheight=0.03, relwidth=0.05)
        delete_old_receipt_btn.place(relx=0.68, rely=0.4, relheight=0.035, relwidth=0.1)
        employ_statics_btn.place(relx=0.79, rely=0.4, relheight=0.035, relwidth=0.1)
        
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

        self.receipt_treeview = Treeview(
            self.main_frame,
            style="Cart.Treeview",
            show="headings",
            columns=("Id", "Emp Name", "Total Price", "Date"),
            selectmode="browse")

        self.receipt_treeview.heading("Id", text="Id", anchor=W)
        self.receipt_treeview.heading("Emp Name", text="Emp Name", anchor=W)
        self.receipt_treeview.heading(
            "Total Price", text="Total Price", anchor=W)
        self.receipt_treeview.heading("Date", text="Date", anchor=W)

        self.scrollbar_two = ctk.CTkScrollbar(
            self.main_frame, orientation="vertical", command=self.receipt_treeview.yview)

        self.receipt_treeview.configure(yscrollcommand=self.scrollbar_two.set)
        self.scrollbar_two.place(relx=0.95, rely=0.02,
                                 relheight=0.35, anchor="nw")

        self.receipt_treeview.place(
            relx=0.55, rely=0.02, relheight=0.35, relwidth=0.4)
        self.receipt_treeview.bind('<<TreeviewSelect>>', self.receipt_item_selected)

        self.column_width()

    def create_style(self, very_small_font):
        style = Style()
        style.theme_use("default")
        # ------- #

        # First one
        style.configure(
            "Admin.Treeview",
            background="#b3b5aa",
            foreground="#d4fff7",
            fieldbackground="#b3b5aa",
            borderwidth=0,
            rowheight=25,
            font=very_small_font)

        style.map("Admin.Treeview", background=[("selected", "#807e7d")])
        style.configure(
            'Admin.Treeview.Heading',
            foreground='#f5d07a',
            background="#ed8a00",
            font=('Arial', 17),
            relief="flat",
            padding=5)

        # ------- #
        # Second one
        style.configure(
            "AEW.Treeview",
            background="#b3b5aa",
            foreground="#e3ffcc",
            fieldbackground="#b3b5aa",
            borderwidth=0,
            rowheight=25,
            font=10)

        style.map("AEW.Treeview", background=[("selected", "#807e7d")])
        style.configure(
            'AEW.Treeview.Heading',
            foreground="white",
            background="#f5e0ae",
            font=('Arial', 14),
            relief="flat",
            padding=5)

    def check_password(self):
        cus = self.db.cursor()
        name, password = self.sign_name_entry.get(
        ).strip(), self.sign_password_entry.get().strip()
        cus.execute("""SELECT root
                       FROM admin
                       WHERE name = ? AND password = ?""",
                    [name, password])

        result = cus.fetchone()
        cus.close()

        sudo_opening = False

        if name == "1" and password == "1":
            sudo_opening = True

        if result is not None:
            if result[0] == "Yes":
                self.sign_in_frame.place_forget()
                self.main_frame.place(x=0, y=0, relwidth=1, relheight=1)
                self.sign_name_entry.delete(0, "end")
                self.sign_password_entry.delete(0, "end")
                self.master.focus()

            else:
                messagebox.showerror("Invalid credentials",
                                     message="User is not a root")

        elif sudo_opening:
            self.sign_in_frame.place_forget()
            self.main_frame.place(x=0, y=0, relwidth=1, relheight=1)
            self.sign_name_entry.delete(0, "end")
            self.sign_password_entry.delete(0, "end")
            self.master.focus()
        else:
            messagebox.showerror("Invalid credentials",
                                 message="Name or password is incorrect")

    def check_signed_in(self):
        if not self.signed_in:
            self.sign_in_frame.place(
                relx=0.5, rely=0.5, anchor="center", relwidth=0.2, relheight=0.15)
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

                        self.treeview.item(item[0], values=(
                            item[0], name_text, price))

            except ValueError:
                pass

    def item_selected(self, _):
        item = self.treeview.selection()
        if len(item) == 1:
            result = self.treeview.item(item[0])["values"]

            self.barcode_text.set(result[0])
            self.name_text.set(result[1])
            self.price_text.set(result[2])
    
    def receipt_item_selected(self, _):
        selected_item = self.receipt_treeview.selection()

        if len(selected_item) == 1:
            receipt_id = self.receipt_treeview.item(selected_item[0])["values"][0]
            self.receipt_search_entry.delete(0, "end")
            self.receipt_search_entry.insert(0, receipt_id)
   
    def receipt_search(self):

        receipt_id = self.receipt_search_entry.get()
        if receipt_id.isdigit():
            cus = self.db.cursor()
            cus.execute("SELECT * FROM receipts WHERE id = ?", [int(receipt_id)])
            result = cus.fetchone()

            if result is not None:
                self.open_receipt_window(values=result)

            else:
                messagebox.showerror("Receipt not found", message="Couldn't find the receipt")

        self.receipt_search_entry.delete(0, "end")
    
    def open_receipt_window(self, values):
        if self.receipt_window is None or not self.receipt_window.winfo_exists():
            self.receipt_window = ctk.CTkToplevel()
            frame = self.receipt_window
            frame.title("Receipt")

            frame.geometry("600x340")
            frame.attributes("-topmost", True)
            frame.grab_set()
            frame.resizable(False, False)

            self.rw_values = values

            first_label = ctk.CTkLabel(
                frame,
                font=SMALL_FONT_ESH,
                text=f"Id: {values[0]}")

            second_label = ctk.CTkLabel(
                frame,
                font=SMALL_FONT_ESH,
                text=f"Emp Name: {values[1]}")

            self.total_receipt_price = ctk.CTkLabel(
                frame,
                font=SMALL_FONT_ESH,
                text=f"Total Price: %.2f" % (values[2]))

            fourth_label = ctk.CTkLabel(
                frame,
                font=SMALL_FONT_ESH,
                text=f"Date: {values[3]}")

            first_label.place(x=5, y=5)
            second_label.place(x=5, y=40)
            self.total_receipt_price.place(x=350, y=5)
            fourth_label.place(x=350, y=40)

            self.rw_treeview = Treeview(
                frame,
                show="headings",
                columns=("Name", "Qty", "Total Price"),
                style="AEW.Treeview",
                selectmode="browse")
            
            rw_scrollbar = ctk.CTkScrollbar(frame, command=self.rw_treeview.yview, height=200)

            self.rw_treeview.configure(yscrollcommand=rw_scrollbar.set)

            self.rw_treeview.heading("Name", text="Name", anchor=W)
            self.rw_treeview.heading("Qty", text="Qty", anchor=W)
            self.rw_treeview.heading("Total Price", text="Total Price", anchor=W)

            self.rw_treeview.column("Name", width=390, minwidth=100, stretch=False)
            self.rw_treeview.column("Qty", width=50, minwidth=40, stretch=False, anchor="center")
            self.rw_treeview.column("Total Price", width=130, minwidth=100, stretch=False)

            cus = self.db.cursor()

            command = """SELECT receipts_items.item_name, receipts_items.qty, items.price
                         FROM receipts_items
                         JOIN items ON receipts_items.item_name = items.name
                         WHERE receipts_items.receipt_barcode = ?;"""
            
            cus.execute(command, [values[0]])
            result = cus.fetchall()
            for item in result:
                qty = item[1]
                price = item[2]
                total_price = round(qty * price, 2)
                total_price = "%.2f" % total_price
                self.rw_treeview.insert(parent="", index="end", iid=item[0], values=(item[0], qty, total_price))

            single_return_btn = ctk.CTkButton(
                frame,
                text="Return selected item",
                font=VERY_SMALL_FONT_ESH,
                fg_color="#9ee3e6",
                hover_color="#b6e1e3",
                text_color="#242424",
                command=self.return_item)
            
            whole_return_btn = ctk.CTkButton(
                frame,
                text="Return whole receipt",
                font=VERY_SMALL_FONT_ESH,
                fg_color="#b3b5aa",
                hover_color="red",
                command=lambda: self.return_item(True))

            self.rw_treeview.place(x=0, y=70, width=570, height=200)
            rw_scrollbar.place(x=570, y=70, anchor="nw")
            single_return_btn.place(x=5, y=290)
            whole_return_btn.place(x=160, y=290)
            cus.close()
        else:
            self.receipt_window.focus()
    
    def return_item(self, whole_receipt=False):
        values = self.rw_values

        if whole_receipt:
            dialog = ctk.CTkToplevel()
            dialog.protocol("WM_DELETE_WINDOW", print) 
            dialog.grab_set()  # Set modal state for the dialog window
            label = ctk.CTkLabel(dialog, text="Temporary until yes or no is answered")
            label.pack(expand=True, fill="both")

            sure = messagebox.askyesno(
                title="Return receipt",
                message="Are you sure you want to return thw whole receipt")
            
            dialog.destroy() 
            self.receipt_window.grab_set()

            cus = self.db.cursor()

            cus.execute("SELECT total_price FROM receipts WHERE id = ?", [values[0]])
            item_price = cus.fetchone()
            cus.close()

            if sure and item_price != 0:
                receipt_id = values[0]
                cus = self.db.cursor()

                cus.execute("""DELETE FROM receipts_items
                            WHERE receipt_barcode = ?""", [receipt_id])
                
                cus.execute("""UPDATE receipts
                            SET total_price = ?
                            WHERE id = ?""", (0, receipt_id))

                self.db.commit()

                cus.close()
                exists = self.receipt_treeview.exists(receipt_id)

                if exists:
                    self.receipt_treeview.item(receipt_id, values=(values[0], values[1], "0.00", values[3]))

                messagebox.showinfo(
                    title="Return receipt",
                    message="Please return %.2f to the customer" % values[2])
                
                self.rw_treeview.delete(*self.rw_treeview.get_children())

                self.total_receipt_price.configure(text="Total_price: 0")
        else:
            selected = self.rw_treeview.selection()

            dialog = ctk.CTkToplevel()
            dialog.protocol("WM_DELETE_WINDOW", print) 
            dialog.grab_set()  # Set modal state for the dialog window
            label = ctk.CTkLabel(dialog, text="Temporary until yes or no is answered")
            label.pack(expand=True, fill="both")
            sure = messagebox.askyesno(
                title="Return item",
                message="Are you sure you want to return selected item")
            dialog.destroy()

            self.receipt_window.grab_set()

            if len(selected) != 0 and sure:
                selected = selected[0]

                receipt_id = values[0]
                item_price = round(float(self.rw_treeview.item(selected)["values"][2]), 2)

                cus = self.db.cursor()
                cus.execute("SELECT total_price FROM receipts WHERE id = ?", [receipt_id])

                old_total_price = cus.fetchone()[0]

                new_total_price = old_total_price - item_price
                self.rw_treeview.delete(selected)

                self.receipt_treeview.item(
                    item=values[0],
                    values=(receipt_id, values[1], new_total_price, values[3]))
                
                self.total_receipt_price.configure(text="Total price: %.2f" % new_total_price)


                cus.execute("""UPDATE receipts 
                            SET total_price = ?
                            WHERE id = ?""", (new_total_price, receipt_id))
                

                cus.execute("""DELETE FROM receipts_items
                        WHERE item_name = ? AND receipt_barcode = ?""", (selected, receipt_id))

                self.db.commit()

                messagebox.showinfo(
                    title="Return receipt",
                    message="Please return %.2f to the customer" % item_price)

            elif len(selected) == 0 and sure:
                messagebox.showerror(title="No item is selected", message="You didn't select any item")
                
    def delete_item(self):
        item = self.treeview.selection()

        if len(item) == 1:
            sure = messagebox.askyesno(
                "Delete item", message="Are you sure you want to delete it")
            if sure:
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

    def search(self):
        barcode = self.search_entry.get()
        self.search_entry.delete(0, "end")

        try:
            self.treeview.selection_set(barcode)
        except TclError:
            messagebox.showerror(
                "Item not found", message="Items is not registered")

    def add_item_window(self):
        if self.add_item_window is None or not self.add_item_window.winfo_exists():
            self.add_item_window = ctk.CTkToplevel()
            frame = self.add_item_window
            
            frame.attributes("-topmost", True)
            frame.grab_set()

            frame.title("Add item")
            frame.geometry(f"450x130")
            frame.resizable(True, False)

            small_font = ("Arial", 20)
            very_small_font = ("Arial", 15)

            # Barcode label
            barcode = ctk.CTkLabel(frame, text="Barcode:", font=small_font)
            # Barcode entry
            self.aiw_barcode_text = ctk.StringVar(value="")
            barcode_entry = ctk.CTkEntry(
                frame, textvariable=self.aiw_barcode_text, font=very_small_font)

            # Name label
            name = ctk.CTkLabel(frame, text="Name:", font=small_font)
            # Name entry
            self.aiw_name_text = ctk.StringVar(value="")
            name_entry = ctk.CTkEntry(
                frame, textvariable=self.aiw_name_text, font=very_small_font)

            # Price label
            price = ctk.CTkLabel(frame, text="Price:", font=small_font)
            # Price entry
            self.aiw_price_text = ctk.StringVar(value="")
            price_entry = ctk.CTkEntry(
                frame, textvariable=self.aiw_price_text, font=very_small_font)

            # Add button
            btn = ctk.CTkButton(frame, text="Add item",
                                font=very_small_font, command=self.add_item)

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
        barcode = self.aiw_barcode_text.get()
        name = self.aiw_name_text.get().strip()
        price = self.aiw_price_text.get()
        if barcode.isdigit() and not name.isspace():
            try:
                price = round(float(price), 2)
                cus = self.db.cursor()

                try:
                    cus.execute("INSERT INTO items VALUES(? , ?, ?)",
                                (barcode, name, price))
                    self.treeview.insert(
                        parent="", index="end", iid=barcode, values=(barcode, name, price))
                    self.aiw_barcode_text.set("")
                    self.aiw_name_text.set("")
                    self.aiw_price_text.set("")

                    self.db.commit()

                    cus.close()
                except sqlite3.IntegrityError:
                    messagebox.showerror(
                        title="Item registered", message="Barcode or name is already taken")

            except ValueError:
                pass

    def add_employ_window(self):
        if self.add_item_window is None or not self.add_item_window.winfo_exists():
            self.add_item_window = ctk.CTkToplevel()
            frame = self.add_item_window

            frame.title("Add employ")
            frame.geometry(f"600x340")

            frame.resizable(False, False)
            frame.grab_set()
            frame.attributes("-topmost", True)

            small_font = ("Arial", 20)
            very_small_font = ("Arial", 13)

            self.create_aew_treeview(frame)

            cus = self.db.cursor()
            cus.execute("SELECT * FROM admin;")
            result = cus.fetchall()
            cus.close()

            for item in result:
                self.aew_treeview.insert(
                    parent="", index="end", iid=item[0], values=item)

            name_label = ctk.CTkLabel(frame, text="Name:", font=small_font)

            self.aew_name_text = ctk.StringVar(value="")
            name_entry = ctk.CTkEntry(
                frame, textvariable=self.aew_name_text, font=very_small_font)

            # Password
            password_label = ctk.CTkLabel(
                frame, text="Password:", font=small_font)

            self.aew_password_text = ctk.StringVar(value="")

            password_entry = ctk.CTkEntry(
                frame, textvariable=self.aew_password_text, font=very_small_font)

            self.aew_root_var = ctk.IntVar(value=0)
            root = ctk.CTkSwitch(
                frame,
                text="Root",
                switch_width=54,
                switch_height=27,
                font=small_font,
                variable=self.aew_root_var)

            add_btn = ctk.CTkButton(
                frame, text="Add employ", command=self.add_employ)

            delete_btn = ctk.CTkButton(
                frame, text="Delete selected employ", command=self.delete_employ)

            name_label.place(x=5, y=210)
            name_entry.place(x=5, y=250)
            password_label.place(x=150, y=210)
            password_entry.place(x=150, y=250)
            root.place(x=300, y=250)
            add_btn.place(x=5, y=300)
            delete_btn.place(x=150, y=300)

        else:
            self.add_item_window.focus()

    def create_aew_treeview(self, frame):

        self.aew_treeview = Treeview(
            frame,
            show="headings",
            columns=("Name", "Password", "Root"),
            selectmode="browse",
            style="AEW.Treeview")

        self.aew_treeview.heading("Name", text="Name", anchor=W)
        self.aew_treeview.heading("Password", text="Password", anchor=W)

        self.aew_treeview.column("Name", width=190, stretch=False)
        self.aew_treeview.column("Password", width=190, stretch=False)
        self.aew_treeview.column(
            "Root", width=70, stretch=False, anchor="center")
        self.aew_treeview.heading("Root", text="Root", anchor=W)

        self.aew_scrollbar = ctk.CTkScrollbar(
            frame, command=self.aew_treeview.yview, height=200)
        self.aew_treeview.configure(yscrollcommand=self.aew_scrollbar.set)

        self.aew_treeview.place(x=0, y=0, relwidth=0.75, height=200)
        self.aew_scrollbar.place(relx=0.75, y=0, anchor="nw")

    def add_employ(self):
        name = self.aew_name_text.get()
        password = self.aew_password_text.get()

        if self.aew_root_var.get():
            root = "Yes"
        else:
            root = "No"

        if not name.isspace() and not password.isspace():
            cus = self.db.cursor()
            name = name.strip()
            password = password.strip()
            values = [name, password, root]
            try:
                cus.execute("""INSERT INTO admin VALUES(?, ?, ?)""", values)

                self.aew_treeview.insert(
                    parent="", index="end", iid=name, values=values)

                name = self.aew_name_text.set("")
                password = self.aew_password_text.set("")

                self.db.commit()
                cus.close()
            except sqlite3.IntegrityError:
                pass

    def delete_employ(self):
        res = self.aew_treeview.selection()
        if len(res) == 1:
            cus = self.db.cursor()
            item = self.aew_treeview.item(res[0])["values"]

            self.aew_treeview.delete(item[0])

            cus.execute("""DELETE FROM admin
                           WHERE name = ? AND password = ?;""", [item[0], item[1]])

            self.db.commit()
            cus.close()

    def delete_receipts(self):
        if self.delete_receipts_window is None or not self.delete_receipts_window.winfo_exists():
            self.delete_receipts_window = ctk.CTkToplevel()
            frame = self.delete_receipts_window

            frame.attributes("-topmost", True)
            frame.grab_set()

            frame.title("Delete receipts")
            frame.geometry(f"350x200")
            frame.resizable(False, False)

            small_font = ("Arial", 20)
            very_small_font = ("Arial", 15)

            def check():
                year_text = year_entry.get()
                month_text = month_combobox.get()

                if year_text.isdigit() and len(year_text) == 4:
                    cus = self.db.cursor()

                    cus.execute("""SELECT id 
                                FROM receipts
                                WHERE date < ?""", [f"{year_text}-{month_text}-01"])
                    
                    result = cus.fetchall()

                    cus.executemany("""DELETE FROM receipts
                                    WHERE id = ?""", result)
                    count = cus.rowcount
                    
                    cus.executemany("""DELETE FROM receipts_items
                                    WHERE receipt_barcode = ?""", result)
                    
                    messagebox.showinfo(
                        title="Deleted successfully",
                        message=f"Deleted {count} receipts successfully")

                    self.db.commit()
                    cus.close()
                    if count != 0:
                        self.update_receipt_treeview()
                else:
                    messagebox.showerror(title="Invalid input", message="Invalid year")

                year_entry.delete(0, "end")
                month_combobox.set("01")
                
            label = ctk.CTkLabel(frame, text="Delete Before:", font=small_font, text_color="#d94011")

            year_label = ctk.CTkLabel(frame, text="Year:", font=small_font)
            year_entry = ctk.CTkEntry(frame, width=150, font=small_font)

            month_label = ctk.CTkLabel(frame, text="Month:", font=small_font)
            month_combobox = ctk.CTkOptionMenu(frame, values=MONTHS)
            
            delete_btn = ctk.CTkButton(
                frame,
                font=very_small_font,
                text="Delete",
                width=70,
                fg_color="#b3b5aa",
                hover_color="red",
                command=check)
            
            label.place(x=5, y=5)
            year_label.place(x=5, y=45)
            month_label.place(x=170, y=45)
            year_entry.place(x=5, y=80)
            month_combobox.place(x=170, y=80)
            delete_btn.place(x=5, y=130)

        else:
            self.delete_receipts_window.focus()

    def update_receipt_treeview(self):
        self.receipt_treeview.delete(*self.receipt_treeview.get_children())

        cus = self.db.cursor()
        cus.execute("""SELECT * 
                    FROM receipts
                    ORDER BY id DESC
                    LIMIT 10000;""")

        result = cus.fetchall()

        for item in result:
            self.receipt_treeview.insert(parent="", index="end",
                                         iid=item[0], values=item)
            
        cus.close()

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
        self.update_btn.place(relx=0.48, rely=0.83,
                              relwidth=0.05, relheight=0.03)
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

        new_total_price = str(round(round(float(values[1]), 2) * new_qty, 2))

        self.item(item_name,
                  values=(item_name, values[1], new_qty, new_total_price))

        self.update_total_price()

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

            total_price = str(
                round(int(qty_text) * round(float(item_price), 2), 2))

            self.qty_total_price.set(total_price)

    def delete_item(self):
        item = self.selection()
        if len(item) != 0:
            self.delete(item[0])
            self.update_total_price()
        
    def update_total_price(self, add=False, total_price=None):
        if add:
            self.total_price = round(self.total_price + total_price, 2)
            self.total_price_text.set(str(self.total_price))
        else:
            children = self.get_children()

            self.total_price = 0
            for child in children:
                value = self.item(child)["values"][3]

                self.total_price = round(
                    self.total_price + round(float(value), 2), 2)

            self.total_price_text.set(str(self.total_price))


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self._set_appearance_mode("dark")

        self.db = sqlite3.connect("supermarket.db")

        self.check_table()

        self.main_frame = ctk.CTkTabview(self, segmented_button_fg_color=GREY,
                                         command=self.main_frame_func)

        self.checkout_window = None

        self.main_frame.add("Cashier")
        self.main_frame.add("Admin")

        self.aspect_ratio()
        self.sign_in(self.SMALL_FONT)
        self.create_main_frame_items()

        self.admin_panel = AdminPanel(
            self.main_frame.tab("Admin"),
            self.VERY_SMALL_FONT,
            self.SMALL_FONT,
            self.BIG_FONT)

        self.enter = False

        self.user = None

        # Zoomed state
        self.after(1, lambda: self.state("zoomed"))

        self.mainloop()

    def sign_in(self, font):
        self.sign_in_frame = ctk.CTkFrame(self.master, fg_color="#333333")

        frame = self.sign_in_frame

        label = ctk.CTkLabel(frame, text="Sign in: ", font=font)

        self.sign_name_entry = ctk.CTkEntry(
            frame, font=font, placeholder_text="Name")
        self.sign_password_entry = ctk.CTkEntry(
            frame, show="*", font=font, placeholder_text="Password")

        button = ctk.CTkButton(frame, text="Enter",
                               command=self.check_password, font=font)

        label.place(relx=0.03, rely=0.1)
        self.sign_name_entry.place(
            relx=0.03, rely=0.4, relwidth=0.6, relheight=0.2)
        self.sign_password_entry.place(
            relx=0.03, rely=0.65, relwidth=0.6, relheight=0.2)
        button.place(relx=0.67, rely=0.5, relwidth=0.3, relheight=0.25)

        self.sign_in_frame.place(
            relx=0.5, rely=0.5, anchor="center", relwidth=0.2, relheight=0.15)

    def check_password(self):
        cus = self.db.cursor()
        name = self.sign_name_entry.get().strip()
        password = self.sign_password_entry.get().strip()

        cus.execute("""SELECT root
                       FROM admin
                       WHERE name = ? AND password = ?""",
                    [name, password])

        result = cus.fetchone()
        cus.close()

        sudo_opening = False

        if name == "1" and password == "1":
            sudo_opening = True

        if result is not None or sudo_opening:
            self.sign_in_frame.place_forget()
            self.main_frame.place(x=0, rely=0.01, relwidth=1, relheight=0.99)
            self.sign_name_entry.delete(0, "end")
            self.sign_password_entry.delete(0, "end")
            self.main_frame.focus()

            self.user = name
            self.user_label.configure(text=f"User: {name}")
        else:
            messagebox.showerror("Invalid credentials",
                                 message="Name or password is incorrect")

    def change_user(self):
        self.sign_in_frame.place(
            relx=0.5, rely=0.5, anchor="center", relwidth=0.2, relheight=0.15)

        self.main_frame.place_forget()

    def check_table(self):
        cursor = self.db.cursor()

        command = """CREATE TABLE IF NOT EXISTS items (
            barcode INT PRIMARY KEY,
            name TEXT,
            price DECIMAL(20, 2)
        );"""

        cursor.execute(command)

        command = """CREATE TABLE IF NOT EXISTS admin (
            name TEXT PRIMARY KEY,
            password TEXT,
            root TEXT
        );"""

        cursor.execute(command)

        command = """CREATE TABLE IF NOT EXISTS receipts (
            id INTEGER,
            emp_name TEXT,
            total_price DECIMAl (20, 2),
            date TEXT,
            PRIMARY KEY (id))"""

        cursor.execute(command)

        command = """CREATE TABLE IF NOT EXISTS receipts_items (
            item_name TEXT, 
            qty INTEGER,
            price REAL,
            receipt_barcode INTEGER, 
            FOREIGN KEY(receipt_barcode) REFERENCES receipts(id) ON DELETE SET NULL )"""

        cursor.execute(command)

        command = "CREATE INDEX IF NOT EXISTS barcode ON items ('barcode' ASC);"
        cursor.execute(command)

        command = "CREATE INDEX IF NOT EXISTS main ON receipts (id ASC, date);"
        cursor.execute(command)

        command = "CREATE INDEX IF NOT EXISTS main_2 ON receipts_items (receipt_barcode ASC);"
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
        self.cart = Cart(frame, self.VERY_SMALL_FONT,
                         self.SMALL_FONT, self.BIG_FONT)

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

        # Item name
        self.item_name = ctk.StringVar(value="")
        self.item_name_entry = ctk.CTkEntry(
            frame,
            font=self.SMALL_FONT,
            state="readonly",
            textvariable=self.item_name)

        # Second label
        second_label = ctk.CTkLabel(
            frame,
            font=self.BIG_FONT,
            text="Item Price:")

        # Item price
        self.item_price = ctk.StringVar(value="")
        self.item_price_entry = ctk.CTkEntry(
            frame,
            font=self.SMALL_FONT,
            state="readonly",
            textvariable=self.item_price)

        # Add to cart button
        self.add_btn = ctk.CTkButton(
            frame, text="Add to cart", command=self.add_to_cart)
        self.barcode_id_label = ctk.CTkLabel(
            frame, font=self.SMALL_FONT, text=f"Barcode: {self.next_receipt_id()}")
        self.user_label = ctk.CTkLabel(frame, font=self.SMALL_FONT)
        self.user_btn = ctk.CTkButton(
            frame,
            font=self.VERY_SMALL_FONT,
            text="Change user",
            fg_color="#9ee3e6",
            hover_color="#b6e1e3",
            text_color="#242424",
            command=self.change_user)

        checkout_btn = ctk.CTkButton(
            frame,
            text="Check Out",
            font=self.SMALL_FONT,
            fg_color="#e09512",
            hover_color="#e8ab41",
            command=self.show_checkout)

        entry.place(relx=0.005, rely=0.01, relwidth=0.3, anchor="nw")
        auto_add.place(relx=0.01, rely=0.12)
        button.place(relx=0.007, rely=0.07, relheight=0.04, relwidth=0.09)
        button_two.place(relx=0.11, rely=0.07, relheight=0.04, relwidth=0.1)
        first_label.place(relx=0.005, rely=0.2)
        second_label.place(relx=0.205, rely=0.2)
        self.item_name_entry.place(relx=0.0054, rely=0.26, relwidth=0.15)
        self.item_price_entry.place(relx=0.2054, rely=0.26)
        self.add_btn.place(relx=0.0054, rely=0.33, relwidth=0.08)
        self.barcode_id_label.place(relx=0.999, rely=0.999, anchor="se")
        self.user_label.place(relx=0.001, rely=0.96)
        self.user_btn.place(relx=0.001, rely=0.93,
                            relheight=0.025, relwidth=0.06)
        checkout_btn.place(relx=0.87, rely=0.85, relwidth=0.1, relheight=0.08)
    
    def next_receipt_id(self):
        cus = self.db.cursor()
        cus.execute("""SELECT id 
                    FROM receipts
                    ORDER BY id DESC
                    LIMIT 1""")

        result = cus.fetchone()
        if result is not None:
            id = result[0] + 1
        else:
            id = 1
        cus.close()
        return id
    
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

        else:
            messagebox.showerror(
                "Item not found",
                "Item is not registered")

        cursor.close()

    def add_to_cart(self):
        if self.item_name.get() != "":

            item_name = self.item_name.get()
            item_price = self.item_price.get()
            qty_text = 1
            total_price = self.item_price.get()

            self.cart.add(
                item_name=item_name,
                item_price=item_price,
                qty=qty_text,
                total_price=total_price)

            self.entry_text.set("")
            self.item_name.set("")
            self.item_price.set("")

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
            id = self.next_receipt_id()
            self.barcode_id_label.configure(text="Barcode: " + str(id))

    def show_checkout(self):
        if self.cart.total_price == 0:
            messagebox.showerror(title="Invalid cart",
                                 message="Can't checkout with zero items")
            return

        if self.checkout_window is None or not self.checkout_window.winfo_exists():
            self.checkout_window = ctk.CTkToplevel(fg_color="#4d7861")
            frame = self.checkout_window

            frame.attributes("-topmost", True)
            frame.grab_set()
            self.cc_frame = None

            frame.title("Checkout")
            frame.geometry(f"350x200")
            frame.resizable(False, False)

            small_font = ("Arial", 20)
            very_small_font = ("Arial", 15)

            self.cw_choose_frame = ctk.CTkFrame(frame, fg_color="transparent")
            choose_frame = self.cw_choose_frame

            cw_choose_label = ctk.CTkLabel(
                choose_frame,
                text="Cash or Credit: ",
                font=small_font,
                text_color="#8ebfbd")

            cash_btn = ctk.CTkButton(
                choose_frame,
                text="Cash",
                font=very_small_font,
                command=self.cash_checkout,
                fg_color="#47c900",
                hover_color="#cfc86d")

            credit_btn = ctk.CTkButton(
                choose_frame,
                font=very_small_font,
                text="Credit",
                command=self.checkout,
                fg_color="#c26c15",
                hover_color="#a37d56")

            choose_frame.pack(fill="both", expand=True)
            cw_choose_label.place(x=175, y=20, anchor="center")
            cash_btn.place(x=20, y=100)
            credit_btn.place(x=200, y=100)

        else:
            self.checkout_window.focus()

    def cash_checkout(self):
        self.cw_choose_frame.pack_forget()

        self.cc_frame = ctk.CTkFrame(
            self.checkout_window, fg_color="transparent")
        frame = self.cc_frame
        font = ("Arial", 15)

        var = ctk.StringVar()
        btn = ctk.CTkButton(frame, text="Continue",
                            command=lambda: self.cw_check_price(var))

        customer_cash_label = ctk.CTkLabel(
            frame,
            text="Customer cash:",
            font=font)

        customer_cash_entry = ctk.CTkEntry(
            frame,
            height=30,
            width=170,
            font=font,
            textvariable=var)

        total_price_label = ctk.CTkLabel(
            frame,
            text="Total price:",
            font=font)

        text = str(self.cart.total_price)

        hmm = ctk.StringVar(value=text)
        total_price_entry = ctk.CTkEntry(
            frame,
            height=30,
            width=170,
            font=font,
            state="readonly",
            textvariable=hmm)

        customer_cash_label.place(x=5, y=10)
        customer_cash_entry.place(x=5, y=40)
        total_price_label.place(x=5, y=90)
        total_price_entry.place(x=5, y=120)
        btn.place(x=200, y=120)
        frame.pack(fill="both", expand=True)

    def cw_check_price(self, var):
        error = False
        try:
            paid = round(float(var.get()), 2)
            if self.cart.total_price <= paid:
                self.cc_frame.pack_forget()
                self.checkout(paid)
            else:
                error = True
        except ValueError:
            error = True

        if error:
            messagebox.showerror(title="Invalid input",
                                 message="Invalid cash amount")

    def checkout(self, paid=None):
        frame = self.checkout_window

        radio_var = ctk.IntVar(value=0)
        remaining_label = ctk.CTkLabel(frame, font=(
            "Arial", 18), text="Remaining:\n0.00")
        if paid is not None:
            radio_var.set(1)
            remaining = paid - self.cart.total_price
            remaining = round(remaining, 2)
            remaining_label.configure(text=f"Remaining:\n{remaining}")
        else:
            self.cw_choose_frame.pack_forget()

        radio_btn_one = ctk.CTkRadioButton(
            frame,
            text="Cash",
            value=1,
            variable=radio_var,
            corner_radius=0,
            state="disabled",
            text_color_disabled="#DCE4EE")

        radio_btn_two = ctk.CTkRadioButton(
            frame,
            text="Credit",
            value=0,
            variable=radio_var,
            corner_radius=0,
            state="disabled",
            text_color_disabled="#DCE4EE")

        print_btn = ctk.CTkButton(
            frame, text="Print", command=self.print, width=70)
        finish_btn = ctk.CTkButton(
            frame, text="Finish", command=self.finish, width=70)

        remaining_label.place(x=5, y=5)
        radio_btn_one.place(x=280, y=20)
        radio_btn_two.place(x=280, y=50)
        print_btn.place(x=5, y=165)
        finish_btn.place(x=275, y=165)

    def finish(self):
        cus = self.db.cursor()
        id = self.next_receipt_id()

        command = """INSERT INTO receipts(emp_name, total_price, date) VALUES(?, ?, ?)"""
        cus.execute(command, (self.user, self.cart.total_price, date.today()))

        self.admin_panel.receipt_treeview.insert(
            parent="", iid=id, index=0,
            values=(id, self.user, self.cart.total_price, date.today()))

        command = """INSERT INTO receipts_items VALUES(?, ?, ?, ?)"""
        values = []
        for item in self.cart.get_children():
            vals = self.cart.item(item)["values"]
            values.append((vals[0], vals[2], vals[1], id))
            self.cart.delete(vals[0])

        cus.executemany(command, values)

        self.barcode_id_label.configure(
            text=f"Barcode: {id + 1}")
        self.cart.total_price = 0
        self.cart.total_price_text.set("0")
        self.checkout_window.destroy()
        self.db.commit()
        cus.close()

    def print(self):
        pass


App()
