import customtkinter as ctk
import mysql.connector
from tkinter import messagebox
from settings import *


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
        # Zoomed state
        self.after(1, lambda: self.state("zoomed"))

        self.mainloop()

    def aspect_ratio(self):
        self.MAIN_BIG_FONT = (MAIN_BIG_FONT_ESH[0], round(
            self.winfo_screenwidth() * MAIN_BIG_FONT_ESH[1] / 1980))
        
        self.MAIN_SMALL_FONT = (MAIN_SMALL_FONT_ESH[0], round(
            self.winfo_screenwidth() * MAIN_SMALL_FONT_ESH[1] / 1980))

    def create_main_frame_items(self):
        frame = self.main_frame.tab("Cashier")

        self.entry_text = ctk.StringVar(value="")

        entry = ctk.CTkEntry(
            frame,
            textvariable=self.entry_text,
            font=self.MAIN_BIG_FONT)

        entry.place(relx=0.005, rely=0.01, relwidth=0.3, anchor="nw")

        button = ctk.CTkButton(
            frame,
            command=self.retrieve_items,
            text="Search",
            font=self.MAIN_SMALL_FONT)

        button.place(relx=0.007, rely=0.07, relheight=0.04)

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

    def retrieve_items(self):
        cursor = self.db.cursor()
        command = f"""
        SELECT name, price 
        FROM items
        WHERE barcode_id = {self.entry_text.get()};"""

        cursor.execute(command)
        result = cursor.fetchone()

        if result is not None:
            self.item_name.set(result[0])  # Name
            self.item_price.set(result[1])  # Price

            self.qty_text.set(1)
        else:
            messagebox.showerror(
                "Item not found",
                "Item is not registered",
                icon=messagebox.ERROR)

        cursor.close()

    def update_total_price(self, *_):
        if self.item_price.get() != "" and self.qty_text.get() != "":
            if self.qty_text.get().isdigit():
                result = int(self.item_price.get()) * int(self.qty_text.get())
                self.total_price.set(str(result))
            else:
                pass



App()
