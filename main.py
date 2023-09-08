import customtkinter as ctk
import mysql.connector
from tkinter import messagebox


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self._set_appearance_mode("dark")

        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Saktamnbaktam12.",
            database="supermarket")
        
        self.main_frame = ctk.CTkTabview(self, segmented_button_fg_color="#242424")
        self.main_frame.add("Cashier")
        self.main_frame.add("Admin")
        self.main_frame.place(x=0, rely=0.01, relwidth=1, relheight=0.99)


        self.test()
        # Zoomed state
        self.after(1, lambda: self.state("zoomed"))

        self.mainloop()

    def test(self):
        frame = self.main_frame.tab("Cashier")
        self.entry_text = ctk.StringVar(value="")
        entry = ctk.CTkEntry(
            frame,
            textvariable=self.entry_text,
            font=("Arial", 35))
        entry.place(relx=0.005, rely=0.01, relwidth=0.3, anchor="nw")

        button = ctk.CTkButton(frame, command=self.pr, text="Search")
        button.place(relx=0.005, rely=0.07, relheight=0.04)
        
        first_label = ctk.CTkLabel(
            frame,
            font=("Arial", 35),
            text="Item name:")
        
        first_label.place(relx=0.05, rely=0.2)

        second_label = ctk.CTkLabel(
            frame,
            font=("Arial", 35),
            text="Item Price:")
        
        second_label.place(relx=0.25, rely=0.2)

        self.third_label_text = ctk.StringVar(value="")
        self.third_label = ctk.CTkEntry(
            frame,
            font=("Arial", 20),
            state="readonly",
            textvariable=self.third_label_text)
        
        self.third_label.place(relx=0.054, rely=0.3, relwidth=0.15)

        self.fourth_label_text = ctk.StringVar(value="")
        self.fourth_label = ctk.CTkEntry(
            frame,
            font=("Arial", 20),
            state="readonly",
            textvariable=self.fourth_label_text)
        
        self.fourth_label.place(relx=0.254, rely=0.3)

    def pr(self):
        cursor = self.db.cursor()
        command = f"""
        SELECT name, price 
        FROM items
        WHERE barcode_id = {self.entry_text.get()};"""
        
        cursor.execute(command)
        result = cursor.fetchone()

        if result is not None:
            self.third_label_text.set(result[0])
            self.fourth_label_text.set(result[1])
        else:
            messagebox.showerror("Item not found", "Item is not registered", icon=messagebox.ERROR)

        cursor.close()


        
App()
