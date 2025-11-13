import customtkinter as ctk
import tkinter as tk

# --- Pengaturan Tema dan Tampilan ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class AdvancedCalculator(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Konfigurasi Jendela Utama ---
        self.title("Kalkulator Profesional")
        self.geometry("420x650")
        self.resizable(False, False)  # Ukuran tetap untuk konsistensi desain
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Font ---
        self.font_display = ("SF Pro Display", 40, "bold")  # Font modern
        self.font_history = ("SF Pro Display", 16)
        self.font_button = ("SF Pro Display", 28)

        # --- Variabel State untuk Logika Kalkulator ---
        self.reset_state()

        # --- Membuat Widget ---
        self.create_widgets()

        # --- Bind Keyboard ---
        self.bind_keyboard_events()

    def reset_state(self):
        """Mengatur ulang semua variabel state ke kondisi awal."""
        self.first_operand = None
        self.operator = None
        self.waiting_for_new_operand = True
        self.error_state = False
        self.update_display("0")
        self.update_history("")

    def create_widgets(self):
        # --- Frame Utama (untuk tampilan yang membulat) ---
        self.main_frame = ctk.CTkFrame(self, corner_radius=20)
        self.main_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.main_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.main_frame.grid_rowconfigure((1, 2, 3, 4, 5, 6), weight=1)

        # --- Display History ---
        self.history_display = ctk.CTkLabel(
            self.main_frame,
            text="",
            font=self.font_history,
            text_color="#888888",
            anchor="e",
        )
        self.history_display.grid(
            row=1, column=0, columnspan=4, padx=(20, 20), pady=(20, 0), sticky="ew"
        )

        # --- Display Utama ---
        self.display = ctk.CTkEntry(
            self.main_frame,
            font=self.font_display,
            justify="right",
            state="disabled",
            border_width=0,
        )
        self.display.grid(
            row=2, column=0, columnspan=4, padx=20, pady=(0, 20), sticky="ew"
        )

        # --- Tombol-tombol Kalkulator ---
        buttons = [
            ("C", 3, 0, 1),
            ("±", 3, 1, 1),
            ("%", 3, 2, 1),
            ("÷", 3, 3, 1),
            ("7", 4, 0, 1),
            ("8", 4, 1, 1),
            ("9", 4, 2, 1),
            ("×", 4, 3, 1),
            ("4", 5, 0, 1),
            ("5", 5, 1, 1),
            ("6", 5, 2, 1),
            ("-", 5, 3, 1),
            ("1", 6, 0, 1),
            ("2", 6, 1, 1),
            ("3", 6, 2, 1),
            ("+", 6, 3, 1),
            ("0", 7, 0, 2),
            (".", 7, 2, 1),
            ("=", 7, 3, 1),
        ]
        self.main_frame.grid_rowconfigure(7, weight=1)  # Tambahkan baris untuk tombol 0

        for text, row, col, colspan in buttons:
            self.create_button(text, row, col, colspan)

    def create_button(self, text, row, col, colspan):
        # Menentukan warna tombol
        fg_color = None
        hover_color = None
        text_color = "white"

        if text in "C±%":
            fg_color = ("#a0a0a0", "#505050")  # Warna untuk mode terang/gelap
            hover_color = ("#808080", "#404040")
        elif text in "÷×-+":
            fg_color = ("#FF9500", "#FF9500")
            hover_color = ("#e68500", "#e68500")
        elif text == "=":
            fg_color = ("#FF9500", "#FF9500")
            hover_color = ("#e68500", "#e68500")
        else:
            fg_color = ("#333333", "#c7c7c7")
            hover_color = ("#4a4a4a", "#a7a7a7")
            text_color = ("white", "black")

        button = ctk.CTkButton(
            self.main_frame,
            text=text,
            font=self.font_button,
            fg_color=fg_color,
            hover_color=hover_color,
            text_color=text_color,
            corner_radius=10,
            command=lambda t=text, b=None: self.on_button_click(t),  # Simulasi animasi
        )
        button.grid(
            row=row,
            column=col,
            columnspan=colspan,
            padx=(10, 5) if col == 0 else (5, 10) if col == 3 else 5,
            pady=5,
            sticky="nsew",
        )

        # Simpan referensi tombol untuk animasi
        button.configure(
            command=lambda t=text, btn=button: self.on_button_click(t, btn)
        )

    def on_button_click(self, char, button_widget=None):
        # Animasi tombol ditekan
        if button_widget:
            button_widget.configure(state="disabled")
            self.after(100, lambda: button_widget.configure(state="normal"))

        # Jika dalam keadaan error, hanya tombol 'C' yang berfungsi
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
        # Update history untuk menunjukkan operasi yang akan datang
        self.update_history(f"{self.first_operand} {op}")

    def calculate_result(self):
        if self.operator is None or self.waiting_for_new_operand:
            return

        second_operand = float(self.display.get())
        result = self.perform_calculation(
            self.first_operand, second_operand, self.operator
        )

        if result is not None:
            # Tampilkan perhitungan lengkap di history
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
        self.display.configure(state="normal")
        self.display.delete(0, tk.END)
        self.display.insert(0, value)
        self.display.configure(state="disabled")

    def update_history(self, value):
        self.history_display.configure(text=value)

    def bind_keyboard_events(self):
        """Menghubungkan tombol keyboard ke fungsi kalkulator."""
        self.bind("<Key>", self.on_key_press)
        self.focus_set()  # Agar jendela bisa menerima input keyboard

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
        elif key == "BackSpace":
            # Fungsi sederhana untuk hapus digit terakhir
            if not self.error_state:
                current_text = self.display.get()
                if len(current_text) > 1:
                    self.update_display(current_text[:-1])
                else:
                    self.update_display("0")
        elif key == "Escape":
            self.on_button_click("C")


# --- Menjalankan Aplikasi ---
if __name__ == "__main__":
    app = AdvancedCalculator()
    app.mainloop()
