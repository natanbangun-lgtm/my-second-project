import tkinter as tk
from tkinter import font


class ProfessionalCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Kalkulator Profesional")
        self.geometry("400x600")
        self.resizable(False, False)
        self.configure(bg="#1e1e1e")  # Background gelap

        # --- Variabel State ---
        self.reset_state()

        # --- Membuat Widget ---
        self.create_widgets()
        self.bind_keyboard_events()

    def reset_state(self):
        self.first_operand = None
        self.operator = None
        self.waiting_for_new_operand = True
        self.error_state = False
        self.update_display("0")
        self.update_history("")

    def create_widgets(self):
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)

        # --- Display History ---
        self.history_display = tk.Label(
            self, text="", font=("Arial", 14), bg="#1e1e1e", fg="#888888", anchor="e"
        )
        self.history_display.grid(
            row=0, column=0, columnspan=4, padx=10, pady=(10, 0), sticky="ew"
        )

        # --- Display Utama ---
        self.display_var = tk.StringVar()
        self.display = tk.Entry(
            self,
            textvariable=self.display_var,
            font=("Arial", 36, "bold"),
            justify="right",
            bd=0,
            bg="#1e1e1e",
            fg="white",
            insertbackground="white",
        )
        self.display.grid(
            row=1, column=0, columnspan=4, padx=10, pady=(0, 10), sticky="ew"
        )

        # --- Tombol-tombol ---
        buttons = [
            ("C", 2, 0, 1),
            ("±", 2, 1, 1),
            ("%", 2, 2, 1),
            ("÷", 2, 3, 1),
            ("7", 3, 0, 1),
            ("8", 3, 1, 1),
            ("9", 3, 2, 1),
            ("×", 3, 3, 1),
            ("4", 4, 0, 1),
            ("5", 4, 1, 1),
            ("6", 4, 2, 1),
            ("-", 4, 3, 1),
            ("1", 5, 0, 1),
            ("2", 5, 1, 1),
            ("3", 5, 2, 1),
            ("+", 5, 3, 1),
            ("0", 6, 0, 2),
            (".", 6, 2, 1),
            ("=", 6, 3, 1),
        ]
        self.grid_rowconfigure(6, weight=1)

        for text, row, col, colspan in buttons:
            self.create_button(text, row, col, colspan)

    def create_button(self, text, row, col, colspan):
        bg_color = "#505050"
        fg_color = "white"
        if text in "C±%":
            bg_color = "#a0a0a0"
            fg_color = "black"
        elif text in "÷×-+":
            bg_color = "#FF9500"

        btn = tk.Button(
            self,
            text=text,
            font=("Arial", 24),
            bg=bg_color,
            fg=fg_color,
            relief=tk.FLAT,
            bd=0,
            command=lambda t=text: self.on_button_click(t),
        )
        btn.grid(row=row, column=col, columnspan=colspan, padx=5, pady=5, sticky="nsew")

    def on_button_click(self, char):
        if self.error_state and char != "C":
            return

        if char == "C":
            self.reset_state()
        elif char in "0123456789":
            self.input_digit(char)
        elif char == ".":
            self.input_decimal()
        elif char in "÷×-+":
            self.input_operator(char)
        elif char == "=":
            self.calculate_result()
        elif char == "±":
            self.toggle_sign()
        elif char == "%":
            self.calculate_percentage()

    def input_digit(self, digit):
        current_text = self.display.get()
        if self.waiting_for_new_operand:
            self.update_display(digit)
            self.waiting_for_new_operand = False
        else:
            if current_text == "0":
                self.update_display(digit)
            else:
                self.update_display(current_text + digit)

    def input_decimal(self):
        current_text = self.display.get()
        if self.waiting_for_new_operand:
            self.update_display("0.")
            self.waiting_for_new_operand = False
        elif "." not in current_text:
            self.update_display(current_text + ".")

    def input_operator(self, op):
        current_value = float(self.display.get())
        if self.operator is not None and not self.waiting_for_new_operand:
            self.first_operand = self.perform_calculation(
                self.first_operand, current_value, self.operator
            )
            if self.first_operand is not None:
                self.update_display(str(self.first_operand))
        else:
            self.first_operand = current_value

        self.operator = op
        self.waiting_for_new_operand = True
        self.update_history(f"{self.first_operand} {op}")

    def calculate_result(self):
        if self.operator is None or self.waiting_for_new_operand:
            return

        second_operand = float(self.display.get())
        result = self.perform_calculation(
            self.first_operand, second_operand, self.operator
        )

        if result is not None:
            self.update_history(
                f"{self.first_operand} {self.operator} {second_operand} ="
            )
            self.update_display(str(result))

        self.first_operand = result
        self.operator = None
        self.waiting_for_new_operand = True

    def perform_calculation(self, first, second, op):
        try:
            if op == "+":
                return first + second
            elif op == "-":
                return first - second
            elif op == "×":
                return first * second
            elif op == "÷":
                if second == 0:
                    raise ZeroDivisionError
                return first / second
        except ZeroDivisionError:
            self.error_state = True
            self.update_history("Tidak bisa dibagi 0")
            self.update_display("Error")
            return None
        except Exception:
            self.error_state = True
            self.update_history("Input tidak valid")
            self.update_display("Error")
            return None

    def toggle_sign(self):
        if self.error_state:
            return
        current_value = float(self.display.get())
        self.update_display(str(-current_value))
        if self.waiting_for_new_operand and self.first_operand is not None:
            self.first_operand = -self.first_operand

    def calculate_percentage(self):
        if self.error_state:
            return
        current_value = float(self.display.get())
        result = current_value / 100
        self.update_display(str(result))
        if self.waiting_for_new_operand and self.first_operand is not None:
            self.first_operand = result

    def update_display(self, value):
        self.display_var.set(value)

    def update_history(self, value):
        self.history_display.configure(text=value)

    def bind_keyboard_events(self):
        self.bind("<Key>", self.on_key_press)
        self.focus_set()

    def on_key_press(self, event):
        key = event.keysym
        if key in "0123456789":
            self.on_button_click(key)
        elif key == "period":
            self.on_button_click(".")
        elif key == "plus":
            self.on_button_click("+")
        elif key == "minus":
            self.on_button_click("-")
        elif key == "asterisk":
            self.on_button_click("×")
        elif key == "slash":
            self.on_button_click("÷")
        elif key == "Return" or key == "equal":
            self.on_button_click("=")
        elif key == "Escape":
            self.on_button_click("C")


if __name__ == "__main__":
    app = ProfessionalCalculator()
    app.mainloop()
