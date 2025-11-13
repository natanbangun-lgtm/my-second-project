import turtle
import random
import time
import os

# --- KONSTANTA ---
LEBAR_LAYAR = 800
TINGGI_LAYAR = 600
WARNA_SIANG = "#87CEEB"
WARNA_PAGI = "#FFD700"
WARNA_MALAM = "#191970"
WARNA_SUBUH = "#4B0082"

# --- KELAS-KELAS GAME ---


class Pemain(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("saddlebrown")
        self.penup()
        self.speed(0)
        self.health = 100
        self.hunger = 100
        self.kecepatan = 15
        self.inventori = {"kayu": 0, "batu": 0, "beri": 0}
        self.mempunyai_kapak = False
        self.mempunyai_perapian = False
        self.mempunyai_shelter = False

    def gerak_atas(self):
        if self.ycor() < TINGGI_LAYAR // 2 - 20:
            self.sety(self.ycor() + self.kecepatan)

    def gerak_bawah(self):
        if self.ycor() > -TINGGI_LAYAR // 2 + 20:
            self.sety(self.ycor() - self.kecepatan)

    def gerak_kiri(self):
        if self.xcor() > -LEBAR_LAYAR // 2 + 20:
            self.setx(self.xcor() - self.kecepatan)

    def gerak_kanan(self):
        if self.xcor() < LEBAR_LAYAR // 2 - 20:
            self.setx(self.xcor() + self.kecepatan)

    def makan_beri(self):
        if self.inventori["beri"] > 0 and self.hunger < 100:
            self.inventori["beri"] -= 1
            self.hunger = min(100, self.hunger + 30)
            return True
        return False

    def istirahat_di_shelter(self):
        if self.mempunyai_shelter and self.health < 100:
            self.health = min(100, self.health + 50)
            return True
        return False


class SumberDaya(turtle.Turtle):
    def __init__(self, tipe, x, y):
        super().__init__()
        self.tipe = tipe
        self.penup()
        self.speed(0)
        self.goto(x, y)
        self.jumlah = random.randint(3, 5)
        self.waktu_respawn = 0
        self.setup_gambar()

    def setup_gambar(self):
        self.hideturtle()
        self.clear()
        if self.tipe == "pohon":
            self.color("saddlebrown")
            self.shape("square")
            self.shapesize(stretch_wid=4, stretch_len=1)
            self.stamp()
            self.color("green")
            self.shape("circle")
            self.shapesize(stretch_wid=2, stretch_len=2)
            self.stamp()
        elif self.tipe == "batu":
            self.color("gray")
            self.shape("circle")
            self.shapesize(stretch_wid=1.5, stretch_len=1.5)
        elif self.tipe == "beri":
            self.color("darkgreen")
            self.shape("circle")
            self.shapesize(stretch_wid=1, stretch_len=1)
        self.showturtle()

    def kumpulkan(self, pemain):
        if self.tipe == "pohon":
            hasil = 2 if pemain.mempunyai_kapak else 1
            pemain.inventori["kayu"] += hasil
        elif self.tipe == "batu":
            pemain.inventori["batu"] += 1
        elif self.tipe == "beri":
            pemain.inventori["beri"] += 1

        self.jumlah -= 1
        if self.jumlah <= 0:
            self.hideturtle()
            self.waktu_respawn = time.time() + 20  # Respawn setelah 20 detik

    def update(self):
        if self.waktu_respawn > 0 and time.time() > self.waktu_respawn:
            self.jumlah = random.randint(3, 5)
            self.waktu_respawn = 0
            self.setup_gambar()


class Predator(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("triangle")
        self.color("darkred")
        self.penup()
        self.speed(0)
        self.kecepatan = random.uniform(1.5, 2.5)
        self.arah = random.uniform(0, 360)
        self.goto(random.randint(-300, 300), random.randint(-200, 200))

    def bergerak(self, pemain):
        # AI sederhana: bergerak menuju pemain
        if self.distance(pemain) > 20:
            self.setheading(self.towards(pemain.xcor(), pemain.ycor()))
            self.forward(self.kecepatan)

    def serang(self, pemain):
        if self.distance(pemain) < 20:
            if pemain.mempunyai_perapian:
                # Predator takut api dan lari
                self.setheading(self.towards(pemain.xcor(), pemain.ycor()) + 180)
                self.forward(self.kecepatan * 5)
            else:
                return True  # Serangan berhasil
        return False


class Game:
    def __init__(self):
        self.window = turtle.Screen()
        self.window.title("Stone Age Survivor")
        self.window.bgcolor(WARNA_SIANG)
        self.window.setup(width=LEBAR_LAYAR, height=TINGGI_LAYAR)
        self.window.tracer(0)

        self.pen = turtle.Turtle()
        self.pen.speed(0)
        self.pen.penup()
        self.pen.hideturtle()

        self.pemain = Pemain()
        self.daftar_sumberdaya = []
        self.daftar_predator = []

        self.hari = 1
        self.waktu = 180  # 3 menit per hari
        self.siang = True
        self.game_state = "MENU"
        self.high_score = self.load_high_score()

        self.generate_dunia()
        self.setup_keyboard()

    def load_high_score(self):
        if os.path.exists("survivor_highscore.txt"):
            with open("survivor_highscore.txt", "r") as f:
                return int(f.read())
        return 0

    def save_high_score(self):
        with open("survivor_highscore.txt", "w") as f:
            f.write(str(self.high_score))

    def generate_dunia(self):
        # Generate pohon
        for _ in range(8):
            x = random.randint(-LEBAR_LAYAR // 2 + 50, LEBAR_LAYAR // 2 - 50)
            y = random.randint(-TINGGI_LAYAR // 2 + 50, TINGGI_LAYAR // 2 - 100)
            self.daftar_sumberdaya.append(SumberDaya("pohon", x, y))
        # Generate batu
        for _ in range(5):
            x = random.randint(-LEBAR_LAYAR // 2 + 50, LEBAR_LAYAR // 2 - 50)
            y = random.randint(-TINGGI_LAYAR // 2 + 50, TINGGI_LAYAR // 2 - 100)
            self.daftar_sumberdaya.append(SumberDaya("batu", x, y))
        # Generate beri
        for _ in range(6):
            x = random.randint(-LEBAR_LAYAR // 2 + 50, LEBAR_LAYAR // 2 - 50)
            y = random.randint(-TINGGI_LAYAR // 2 + 50, TINGGI_LAYAR // 2 - 100)
            self.daftar_sumberdaya.append(SumberDaya("beri", x, y))

    def setup_keyboard(self):
        self.window.listen()
        # Gerakan
        self.window.onkeypress(self.pemain.gerak_atas, "Up")
        self.window.onkeypress(self.pemain.gerak_bawah, "Down")
        self.window.onkeypress(self.pemain.gerak_kiri, "Left")
        self.window.onkeypress(self.pemain.gerak_kanan, "Right")
        # Aksi
        self.window.onkeypress(self.buka_menu_crafting, "c")
        self.window.onkeypress(self.pemain.makan_beri, "e")
        self.window.onkeypress(self.pemain.istirahat_di_shelter, "r")
        # Menu
        self.window.onkeypress(self.start_game, "space")
        self.window.onkeypress(self.quit_game, "Escape")

    def buka_menu_crafting(self):
        if self.game_state != "PLAYING":
            return

        self.pen.clear()
        self.pen.goto(0, 150)
        self.pen.write(
            "--- MENU CRAFTING ---", align="center", font=("Courier", 20, "bold")
        )

        resep = [
            (
                "Kapak Batu",
                "2 Kayu, 1 Batu",
                "1",
                self.pemain.inventori["kayu"] >= 2
                and self.pemain.inventori["batu"] >= 1
                and not self.pemain.mempunyai_kapak,
            ),
            (
                "Perapian",
                "3 Kayu",
                "2",
                self.pemain.inventori["kayu"] >= 3
                and not self.pemain.mempunyai_perapian,
            ),
            (
                "Shelter",
                "5 Kayu, 3 Batu",
                "3",
                self.pemain.inventori["kayu"] >= 5
                and self.pemain.inventori["batu"] >= 3
                and not self.pemain.mempunyai_shelter,
            ),
        ]

        y_pos = 100
        for nama, butuh, key, bisa_dibuat in resep:
            warna = "green" if bisa_dibuat else "red"
            self.pen.goto(0, y_pos)
            self.pen.write(
                f"[{key}] {nama} ({butuh})",
                align="center",
                font=("Courier", 16, "normal"),
                color=warna,
            )
            y_pos -= 30

        self.pen.goto(0, y_pos - 30)
        self.pen.write(
            "Tekan angka untuk craft, ESC untuk tutup",
            align="center",
            font=("Courier", 14, "italic"),
        )

        # Tunggu input
        pilihan = self.window.textinput(
            "Crafting", "Masukkan nomor (1/2/3) atau batal:"
        )

        if pilihan == "1" and resep[0][3]:
            self.pemain.inventori["kayu"] -= 2
            self.pemain.inventori["batu"] -= 1
            self.pemain.mempunyai_kapak = True
            self.pemain.kecepatan = 20
        elif pilihan == "2" and resep[1][3]:
            self.pemain.inventori["kayu"] -= 3
            self.pemain.mempunyai_perapian = True
        elif pilihan == "3" and resep[2][3]:
            self.pemain.inventori["kayu"] -= 5
            self.pemain.inventori["batu"] -= 3
            self.pemain.mempunyai_shelter = True

        self.pen.clear()

    def update_siklus_waktu(self):
        self.waktu -= 1
        if self.waktu <= 0:
            self.waktu = 180
            self.hari += 1
            self.siang = not self.siang  # Toggle siang/malam

            if self.siang:
                # Pagi, predator hilang
                for p in self.daftar_predator:
                    p.hideturtle()
                self.daftar_predator.clear()
            else:
                # Malam, spawn predator
                for _ in range(self.hari // 2 + 1):  # Semakin banyak predator
                    self.daftar_predator.append(Predator())

        # Ubah warna langit berdasarkan waktu
        if self.siang:
            if self.waktu > 150:
                self.window.bgcolor(WARNA_SIANG)
            elif self.waktu > 140:
                self.window.bgcolor(WARNA_PAGI)
        else:  # Malam
            if self.waktu > 30:
                self.window.bgcolor(WARNA_MALAM)
            else:
                self.window.bgcolor(WARNA_SUBUH)

    def update_ui(self):
        self.pen.clear()
        # Health Bar
        self.pen.goto(-LEBAR_LAYAR // 2 + 20, TINGGI_LAYAR // 2 - 30)
        self.pen.write(
            f"Health: {self.pemain.health}", align="left", font=("Courier", 16, "bold")
        )
        # Hunger Bar
        self.pen.goto(-LEBAR_LAYAR // 2 + 20, TINGGI_LAYAR // 2 - 55)
        self.pen.write(
            f"Hunger: {self.pemain.hunger}", align="left", font=("Courier", 16, "bold")
        )
        # Inventori
        self.pen.goto(-LEBAR_LAYAR // 2 + 20, TINGGI_LAYAR // 2 - 80)
        self.pen.write(
            f"Inv: Kayu({self.pemain.inventori['kayu']}) Batu({self.pemain.inventori['batu']}) Beri({self.pemain.inventori['beri']})",
            align="left",
            font=("Courier", 14, "normal"),
        )
        # Hari & Waktu
        status_waktu = "Siang" if self.siang else "Malam"
        self.pen.goto(LEBAR_LAYAR // 2 - 20, TINGGI_LAYAR // 2 - 30)
        self.pen.write(
            f"Hari: {self.hari} ({status_waktu})",
            align="right",
            font=("Courier", 16, "bold"),
        )
        # Alat
        self.pen.goto(0, -TINGGI_LAYAR // 2 + 20)
        alat_str = ""
        if self.pemain.mempunyai_kapak:
            alat_str += "Kapak "
        if self.pemain.mempunyai_perapian:
            alat_str += "Perapian "
        if self.pemain.mempunyai_shelter:
            alat_str += "Shelter "
        self.pen.write(
            f"Alat: {alat_str}", align="center", font=("Courier", 14, "italic")
        )

    def show_menu(self):
        self.pen.clear()
        self.pen.goto(0, 100)
        self.pen.write(
            "STONE AGE SURVIVOR", align="center", font=("Courier", 28, "bold")
        )
        self.pen.goto(0, 30)
        self.pen.write(
            f"Hari Tertinggi: {self.high_score}",
            align="center",
            font=("Courier", 20, "normal"),
        )
        self.pen.goto(0, -20)
        self.pen.write(
            "Kumpulkan, Crafting, dan Bertahanlah!",
            align="center",
            font=("Courier", 16, "italic"),
        )
        self.pen.goto(0, -70)
        self.pen.write(
            "Tekan SPACE untuk Mulai", align="center", font=("Courier", 18, "normal")
        )
        self.pen.goto(0, -100)
        self.pen.write(
            "Tekan ESC untuk Keluar", align="center", font=("Courier", 18, "normal")
        )

    def show_game_over(self):
        if self.hari > self.high_score:
            self.high_score = self.hari
            self.save_high_score()
        self.pen.clear()
        self.pen.goto(0, 100)
        self.pen.write("KAMU MATI", align="center", font=("Courier", 36, "bold"))
        self.pen.goto(0, 30)
        self.pen.write(
            f"Bertahan Selama: {self.hari} Hari",
            align="center",
            font=("Courier", 24, "normal"),
        )
        self.pen.goto(0, -10)
        self.pen.write(
            f"Tertinggi: {self.high_score} Hari",
            align="center",
            font=("Courier", 20, "normal"),
        )
        self.pen.goto(0, -60)
        self.pen.write(
            "Tekan SPACE untuk Main Lagi",
            align="center",
            font=("Courier", 18, "normal"),
        )
        self.pen.goto(0, -90)
        self.pen.write(
            "Tekan ESC untuk Keluar", align="center", font=("Courier", 18, "normal")
        )

    def start_game(self):
        if self.game_state in ["MENU", "GAME_OVER"]:
            self.reset_game()
            self.game_state = "PLAYING"

    def quit_game(self):
        self.window.bye()

    def reset_game(self):
        self.pemain = Pemain()
        self.daftar_sumberdaya.clear()
        self.daftar_predator.clear()
        self.generate_dunia()
        self.hari = 1
        self.waktu = 180
        self.siang = True

    def run(self):
        while True:
            if self.game_state == "MENU":
                self.show_menu()
                self.window.update()
                time.sleep(0.1)
            elif self.game_state == "PLAYING":
                # Update logika game
                self.update_siklus_waktu()
                self.pemain.hunger -= 0.1
                if self.pemain.hunger <= 0:
                    self.pemain.health -= 0.5

                # Update sumber daya
                for sumber in self.daftar_sumberdaya:
                    sumber.update()
                    if self.pemain.distance(sumber) < 30 and sumber.isvisible():
                        sumber.kumpulkan(self.pemain)

                # Update predator
                if not self.siang:
                    for predator in self.daftar_predator:
                        predator.bergerak(self.pemain)
                        if predator.serang(self.pemain):
                            self.pemain.health -= 10

                self.update_ui()

                # Cek Game Over
                if self.pemain.health <= 0:
                    self.game_state = "GAME_OVER"

                self.window.update()
                time.sleep(0.05)
            elif self.game_state == "GAME_OVER":
                self.show_game_over()
                self.window.update()
                time.sleep(0.1)


# --- MEMULAI GAME ---
if __name__ == "__main__":
    game = Game()
    game.run()
