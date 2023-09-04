import customtkinter as ctk


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self._set_appearance_mode("dark")

        # Zoomed state
        self.after(1, lambda: self.state("zoomed"))

        self.mainloop()


App()
