import turtle
import random
import time

# --- KELAS-KELAS UNTUK OBJEK GAME ---


class Pemain(turtle.Turtle):
    """Kelas untuk keranjang pemain."""

    def __init__(self):
        super().__init__()
        self.shape("square")
        self.color("saddlebrown")
        self.shapesize(stretch_wid=1, stretch_len=5)
        self.penup()
        self.speed(0)
        self.goto(0, -250)
        self.kecepatan = 25

    def gerak_kiri(self):
        if self.xcor() > -280:
            self.setx(self.xcor() - self.kecepatan)

    def gerak_kanan(self):
        if self.xcor() < 280:
            self.setx(self.xcor() + self.kecepatan)


class ObjekJatuh(turtle.Turtle):
    """Kelas untuk apel dan bom."""

    def __init__(self, tipe_objek):
        super().__init__()
        self.tipe = tipe_objek
        self.penup()
        self.speed(0)
        self.kecepatan_jatuh = random.uniform(2, 5)

        if self.tipe == "apel":
            self.color("red")
            self.shape("circle")
            self.skor = 10
        else:  # bom
            self.color("black")
            self.shape("triangle")
            self.skor = -20  # Mengurangi nyawa

    def reset_posisi(self):
        x_random = random.randint(-280, 280)
        y_random = random.randint(250, 350)
        self.goto(x_random, y_random)
        self.kecepatan_jatuh = random.uniform(2, 5)


class Game:
    """Kelas utama untuk mengontrol seluruh game."""

    def __init__(self):
        # Setup Window
        self.window = turtle.Screen()
        self.window.title("Tangkap Apel Sempurna")
        self.window.bgcolor("lightblue")
        self.window.setup(width=600, height=700)
        self.window.tracer(0)

        # Setup UI (Skor & Nyawa)
        self.pen = turtle.Turtle()
        self.pen.speed(0)
        self.pen.color("black")
        self.pen.penup()
        self.pen.hideturtle()

        # Variabel Game
        self.skor = 0
        self.nyawa = 3
        self.daftar_objek = []
        self.delay_spawn = 0.01  # Interval munculnya objek baru

        # Buat objek pemain
        self.pemain = Pemain()

        # Setup keyboard
        self.setup_keyboard()

    def setup_keyboard(self):
        self.window.listen()
        self.window.onkeypress(self.pemain.gerak_kiri, "Left")
        self.window.onkeypress(self.pemain.gerak_kanan, "Right")
        self.window.onkeypress(self.restart_game, "space")  # Untuk restart
        self.window.onkeypress(self.quit_game, "Escape")  # Untuk keluar

    def spawn_objek(self):
        """Membuat objek baru (apel atau bom) secara random."""
        if random.random() < self.delay_spawn:
            tipe = random.choice(["apel", "bom"])
            objek_baru = ObjekJatuh(tipe)
            objek_baru.reset_posisi()
            self.daftar_objek.append(objek_baru)

    def update_objek(self):
        """Memindahkan semua objek dan mengecek tabrakan."""
        for objek in self.daftar_objek:
            objek.sety(objek.ycor() - objek.kecepatan_jatuh)

            # Cek jika objek ditangkap pemain
            if objek.distance(self.pemain) < 40:
                if objek.tipe == "apel":
                    self.skor += objek.skor
                    # Tingkatkan kesulitan
                    if self.skor % 50 == 0:
                        for o in self.daftar_objek:
                            o.kecepatan_jatuh *= 1.1
                else:  # menangkap bom
                    self.nyawa -= 1

                objek.reset_posisi()

            # Cek jika objek jatuh ke bawah
            if objek.ycor() < -300:
                if objek.tipe == "apel":
                    self.nyawa -= 1
                objek.reset_posisi()

    def update_ui(self):
        """Memperbarui tampilan skor dan nyawa."""
        self.pen.clear()
        self.pen.goto(-290, 320)
        self.pen.write(f"Skor: {self.skor}", align="left", font=("Courier", 18, "bold"))
        self.pen.goto(290, 320)
        self.pen.write(
            f"Nyawa: {self.nyawa}", align="right", font=("Courier", 18, "bold")
        )

    def tampilkan_layar_akhir(self):
        """Menampilkan layar Game Over."""
        self.pen.goto(0, 0)
        self.pen.write("GAME OVER", align="center", font=("Courier", 36, "bold"))
        self.pen.goto(0, -40)
        self.pen.write(
            f"Skor Akhir: {self.skor}", align="center", font=("Courier", 24, "normal")
        )
        self.pen.goto(0, -80)
        self.pen.write(
            "Tekan SPASI untuk Main Lagi",
            align="center",
            font=("Courier", 18, "normal"),
        )
        self.pen.goto(0, -110)
        self.pen.write(
            "Tekan ESC untuk Keluar", align="center", font=("Courier", 18, "normal")
        )

    def reset_game(self):
        """Mengatur ulang semua variabel game ke kondisi awal."""
        self.skor = 0
        self.nyawa = 3
        # Hapus semua objek yang ada
        for objek in self.daftar_objek:
            objek.hideturtle()
        self.daftar_objek.clear()
        self.delay_spawn = 0.01

    def restart_game(self):
        """Fungsi untuk memulai ulang game."""
        self.reset_game()
        self.main_loop()

    def quit_game(self):
        """Fungsi untuk keluar dari game."""
        self.window.bye()

    def main_loop(self):
        """Loop utama permainan."""
        while self.nyawa > 0:
            self.window.update()
            self.spawn_objek()
            self.update_objek()
            self.update_ui()
            time.sleep(0.02)  # Kontrol kecepatan game

        # Jika nyawa habis, tampilkan layar akhir
        self.tampilkan_layar_akhir()
        self.window.mainloop()  # Menunggu input dari user (spasi/esc)


# --- MEMULAI GAME ---
if __name__ == "__main__":
    game = Game()
    game.main_loop()
