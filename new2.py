import turtle
import random
import time
import os

# --- KONSTANTA ---
LEBAR_LAYAR = 700
TINGGI_LAYAR = 800
WARNA_LANGIT = "#87CEEB"
WARNA_RUMPUT = "#90EE90"
DELAY_GAME = 0.02


# --- FUNSI-FUNSI GAMBAR UMUM ---
def gambar_ekor(t, panjang):
    for _ in range(10):
        t.forward(panjang)
        t.backward(panjang)
        t.right(36)


# --- KELAS-KELAS VISUAL ---


class Pemain(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.penup()
        self.speed(0)
        self.lebar_standar = 5
        self.kecepatan = 25
        self.perisai_aktif = False
        self.powerup_timer = {}
        self.shield_turtle = None
        self.gambar_keranjang()

    def gambar_keranjang(self):
        self.clear()
        self.goto(0, -TINGGI_LAYAR // 2 + 60)
        self.shape("square")
        self.shapesize(stretch_wid=1, stretch_len=self.lebar_standar)
        self.color("saddlebrown")
        self.showturtle()
        self.update_perisai_visual()

    def update_perisai_visual(self):
        if self.shield_turtle:
            self.shield_turtle.clear()
            self.shield_turtle.hideturtle()
            self.shield_turtle = None

        if self.perisai_aktif:
            self.shield_turtle = turtle.Turtle()
            self.shield_turtle.hideturtle()
            self.shield_turtle.penup()
            self.shield_turtle.speed(0)
            self.shield_turtle.color("cyan")
            self.shield_turtle.goto(self.xcor(), self.ycor())
            self.shield_turtle.pendown()
            self.shield_turtle.width(3)
            self.shield_turtle.circle(self.lebar_standar * 5)
            self.shield_turtle.penup()

    def gerak_kiri(self):
        if self.xcor() > -LEBAR_LAYAR // 2 + 60:
            self.setx(self.xcor() - self.kecepatan)
            self.update_perisai_visual()

    def gerak_kanan(self):
        if self.xcor() < LEBAR_LAYAR // 2 - 60:
            self.setx(self.xcor() + self.kecepatan)
            self.update_perisai_visual()

    def reset(self):
        self.gambar_keranjang()
        self.perisai_aktif = False
        self.powerup_timer.clear()


class ObjekJatuh(turtle.Turtle):
    def __init__(self, tipe_objek):
        super().__init__()
        self.tipe = tipe_objek
        self.penup()
        self.speed(0)
        self.kecepatan_jatuh = random.uniform(2, 5)
        self.skor = 0
        self.gambar_objek()

    def gambar_objek(self):
        self.hideturtle()
        self.clear()

        if self.tipe == "apel":
            self.skor = 10
            self.shape("circle")
            self.shapesize(stretch_wid=1.2, stretch_len=1.2)
            self.color("red")
            self.showturtle()
            # Gambar daun
            daun = turtle.Turtle()
            daun.hideturtle()
            daun.penup()
            daun.speed(0)
            daun.color("green")
            daun.goto(self.xcor() + 5, self.ycor() + 15)
            daun.shape("circle")
            daun.shapesize(stretch_wid=0.3, stretch_len=0.5)
            daun.showturtle()
            self.ekstra_turtle = daun

        elif self.tipe == "apel_emas":
            self.skor = 50
            self.shape("circle")
            self.shapesize(stretch_wid=1.5, stretch_len=1.5)
            self.color("gold")
            self.showturtle()
            # Gambar bintang
            bintang = turtle.Turtle()
            bintang.hideturtle()
            bintang.penup()
            bintang.speed(0)
            bintang.color("yellow")
            bintang.goto(self.xcor(), self.ycor() + 5)
            gambar_ekor(bintang, 10)
            bintang.showturtle()
            self.ekstra_turtle = bintang

        elif self.tipe == "bom":
            self.skor = 0
            self.shape("circle")
            self.shapesize(stretch_wid=1.2, stretch_len=1.2)
            self.color("black")
            self.showturtle()
            # Gambar sumbu
            sumbu = turtle.Turtle()
            sumbu.hideturtle()
            sumbu.penup()
            sumbu.speed(0)
            sumbu.color("gray")
            sumbu.width(3)
            sumbu.goto(self.xcor(), self.ycor() + 15)
            sumbu.pendown()
            sumbu.goto(self.xcor(), self.ycor() + 25)
            sumbu.penup()
            sumbu.goto(self.xcor(), self.ycor() + 25)
            sumbu.dot(5, "orange")
            sumbu.showturtle()
            self.ekstra_turtle = sumbu

        elif self.tipe == "powerup_perisai":
            self.shape("circle")
            self.shapesize(stretch_wid=1, stretch_len=1)
            self.color("blue")
            self.showturtle()
            perisai_icon = turtle.Turtle()
            perisai_icon.hideturtle()
            perisai_icon.penup()
            perisai_icon.speed(0)
            perisai_icon.color("white")
            perisai_icon.goto(self.xcor(), self.ycor() - 5)
            perisai_icon.write("P", align="center", font=("Arial", 16, "bold"))
            self.ekstra_turtle = perisai_icon

        elif self.tipe == "powerup_lambat":
            self.shape("circle")
            self.shapesize(stretch_wid=1, stretch_len=1)
            self.color("yellow")
            self.showturtle()
            jam_icon = turtle.Turtle()
            jam_icon.hideturtle()
            jam_icon.penup()
            jam_icon.speed(0)
            jam_icon.color("black")
            jam_icon.goto(self.xcor(), self.ycor() - 5)
            jam_icon.write("T", align="center", font=("Arial", 16, "bold"))
            self.ekstra_turtle = jam_icon

        elif self.tipe == "powerup_lebar":
            self.shape("circle")
            self.shapesize(stretch_wid=1, stretch_len=1)
            self.color("green")
            self.showturtle()
            panah_icon = turtle.Turtle()
            panah_icon.hideturtle()
            panah_icon.penup()
            panah_icon.speed(0)
            panah_icon.color("white")
            panah_icon.goto(self.xcor(), self.ycor() - 5)
            panah_icon.write("W", align="center", font=("Arial", 16, "bold"))
            self.ekstra_turtle = panah_icon

    def reset_posisi(self):
        # Hapus ekstra turtle sebelumnya
        if hasattr(self, "ekstra_turtle"):
            self.ekstra_turtle.clear()
            self.ekstra_turtle.hideturtle()

        x_random = random.randint(-LEBAR_LAYAR // 2 + 20, LEBAR_LAYAR // 2 - 20)
        y_random = random.randint(TINGGI_LAYAR // 2 - 50, TINGGI_LAYAR // 2 + 50)
        self.goto(x_random, y_random)
        self.kecepatan_jatuh = random.uniform(2, 5)
        self.gambar_objek()


class EfekVisual:
    def __init__(self):
        self.efek_list = []

    def tambah_efek_teks(self, x, y, text, color):
        efek = turtle.Turtle()
        efek.hideturtle()
        efek.penup()
        efek.speed(0)
        efek.color(color)
        efek.goto(x, y)
        efek.write(text, align="center", font=("Courier", 20, "bold"))
        self.efek_list.append({"turtle": efek, "type": "text", "y": y, "lifetime": 30})

    def tambah_efek_ledakan(self, x, y):
        efek = turtle.Turtle()
        efek.hideturtle()
        efek.penup()
        efek.speed(0)
        efek.shape("circle")
        efek.goto(x, y)
        efek.color("red")
        efek.shapesize(stretch_wid=0.5, stretch_len=0.5)
        efek.showturtle()
        self.efek_list.append(
            {"turtle": efek, "type": "explosion", "size": 0.5, "lifetime": 15}
        )

    def update(self):
        for item in self.efek_list[:]:
            item["lifetime"] -= 1
            if item["lifetime"] <= 0:
                item["turtle"].clear()
                item["turtle"].hideturtle()
                self.efek_list.remove(item)
            else:
                if item["type"] == "text":
                    item["y"] += 2
                    item["turtle"].sety(item["y"])
                elif item["type"] == "explosion":
                    item["size"] += 0.3
                    item["turtle"].shapesize(
                        stretch_wid=item["size"], stretch_len=item["size"]
                    )
                    item["turtle"].color(
                        "orange" if item["lifetime"] % 2 == 0 else "red"
                    )


class Game:
    def __init__(self):
        self.window = turtle.Screen()
        self.window.title("Tangkap Apel: Visual Masterpiece Edition")
        self.window.bgcolor(WARNA_LANGIT)
        self.window.setup(width=LEBAR_LAYAR, height=TINGGI_LAYAR)
        self.window.tracer(0)

        self.pen = turtle.Turtle()
        self.pen.speed(0)
        self.pen.penup()
        self.pen.hideturtle()

        self.high_score = self.load_high_score()
        self.game_state = "MENU"

        self.pemain = Pemain()
        self.daftar_objek = []
        self.efek_visual = EfekVisual()

        self.skor = 0
        self.nyawa = 3
        self.delay_spawn = 0.02
        self.waktu_lambat_aktif = False

        self.gambar_latar()
        self.setup_keyboard()

    def load_high_score(self):
        if os.path.exists("highscore.txt"):
            with open("highscore.txt", "r") as f:
                return int(f.read())
        return 0

    def save_high_score(self):
        with open("highscore.txt", "w") as f:
            f.write(str(self.high_score))

    def gambar_latar(self):
        latar = turtle.Turtle()
        latar.hideturtle()
        latar.speed(0)
        latar.penup()

        # Rumput
        latar.goto(-LEBAR_LAYAR // 2, -TINGGI_LAYAR // 2)
        latar.fillcolor(WARNA_RUMPUT)
        latar.begin_fill()
        latar.setheading(0)
        latar.forward(LEBAR_LAYAR)
        latar.left(90)
        latar.forward(100)
        latar.left(90)
        latar.forward(LEBAR_LAYAR)
        latar.left(90)
        latar.forward(100)
        latar.end_fill()

        # Pohon
        for i in range(3):
            x_pohon = -200 + i * 200
            # Batang
            latar.goto(x_pohon, -TINGGI_LAYAR // 2 + 100)
            latar.color("saddlebrown")
            latar.pendown()
            latar.width(20)
            latar.setheading(90)
            latar.forward(150)
            latar.penup()
            # Mahkota
            latar.goto(x_pohon, -TINGGI_LAYAR // 2 + 250)
            latar.color("green")
            latar.dot(120, "green")
            latar.dot(100, "darkgreen")

        # Awan
        for i in range(4):
            x_awan = -250 + i * 150
            y_awan = TINGGI_LAYAR // 2 - 100
            latar.color("white")
            latar.goto(x_awan, y_awan)
            latar.dot(60)
            latar.goto(x_awan + 25, y_awan)
            latar.dot(50)
            latar.goto(x_awan - 25, y_awan)
            latar.dot(50)

    def setup_keyboard(self):
        self.window.listen()
        self.window.onkeypress(self.pemain.gerak_kiri, "Left")
        self.window.onkeypress(self.pemain.gerak_kanan, "Right")
        self.window.onkeypress(self.toggle_pause, "p")
        self.window.onkeypress(self.start_game, "space")
        self.window.onkeypress(self.quit_game, "Escape")

    def toggle_pause(self):
        if self.game_state == "PLAYING":
            self.game_state = "PAUSED"
        elif self.game_state == "PAUSED":
            self.game_state = "PLAYING"

    def start_game(self):
        if self.game_state in ["MENU", "GAME_OVER"]:
            self.reset_game()
            self.game_state = "PLAYING"

    def quit_game(self):
        self.window.bye()

    def reset_game(self):
        self.pen.clear()
        for objek in self.daftar_objek:
            if hasattr(objek, "ekstra_turtle"):
                objek.ekstra_turtle.clear()
                objek.ekstra_turtle.hideturtle()
            objek.hideturtle()
        self.daftar_objek.clear()
        self.pemain.reset()
        self.skor = 0
        self.nyawa = 3
        self.delay_spawn = 0.02
        self.waktu_lambat_aktif = False
        self.efek_visual = EfekVisual()

    def show_menu(self):
        self.pen.clear()
        self.pen.goto(0, 150)
        self.pen.write(
            "TANGKAP APEL: VISUAL MASTERPIECE",
            align="center",
            font=("Courier", 24, "bold"),
        )
        self.pen.goto(0, 80)
        self.pen.write(
            f"High Score: {self.high_score}",
            align="center",
            font=("Courier", 20, "normal"),
        )
        self.pen.goto(0, 0)
        self.pen.write(
            "Tekan SPACE untuk Mulai", align="center", font=("Courier", 18, "normal")
        )
        self.pen.goto(0, -40)
        self.pen.write(
            "Tekan ESC untuk Keluar", align="center", font=("Courier", 18, "normal")
        )

    def show_game_over(self):
        if self.skor > self.high_score:
            self.high_score = self.skor
            self.save_high_score()
        self.pen.clear()
        self.pen.goto(0, 100)
        self.pen.write("GAME OVER", align="center", font=("Courier", 36, "bold"))
        self.pen.goto(0, 30)
        self.pen.write(
            f"Skor Akhir: {self.skor}", align="center", font=("Courier", 24, "normal")
        )
        self.pen.goto(0, -10)
        self.pen.write(
            f"High Score: {self.high_score}",
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

    def show_pause(self):
        self.pen.goto(0, 0)
        self.pen.write("DIJEDA", align="center", font=("Courier", 48, "bold"))
        self.pen.goto(0, -50)
        self.pen.write(
            "Tekan P untuk Lanjut", align="center", font=("Courier", 18, "normal")
        )

    def update_ui(self):
        self.pen.clear()
        # Kotak UI
        self.pen.goto(-LEBAR_LAYAR // 2 + 10, TINGGI_LAYAR // 2 - 10)
        self.pen.fillcolor("white")
        self.pen.begin_fill()
        self.pen.pendown()
        for _ in range(2):
            self.pen.forward(200)
            self.pen.right(90)
            self.pen.forward(40)
            self.pen.right(90)
        self.pen.end_fill()
        self.pen.penup()

        # Teks Skor
        self.pen.goto(-LEBAR_LAYAR // 2 + 20, TINGGI_LAYAR // 2 - 30)
        self.pen.write(f"Skor: {self.skor}", align="left", font=("Courier", 18, "bold"))

        # Ikon Nyawa (Hati)
        for i in range(self.nyawa):
            self.pen.goto(LEBAR_LAYAR // 2 - 30 - (i * 35), TINGGI_LAYAR // 2 - 20)
            self.pen.color("red")
            self.pen.write("♥", align="center", font=("Arial", 24, "normal"))

        # Status Power-up
        y_status = TINGGI_LAYAR // 2 - 70
        if self.pemain.perisai_aktif:
            self.pen.goto(0, y_status)
            self.pen.write(
                "PERISAI AKTIF",
                align="center",
                font=("Courier", 14, "normal"),
                color="blue",
            )
        if "lebar" in self.pemain.powerup_timer:
            self.pen.goto(0, y_status - 20)
            sisa_waktu = int(self.pemain.powerup_timer["lebar"] - time.time())
            self.pen.write(
                f"KERANJANG LEBAR: {sisa_waktu}s",
                align="center",
                font=("Courier", 14, "normal"),
                color="green",
            )
        if self.waktu_lambat_aktif:
            self.pen.goto(0, y_status - 40)
            sisa_waktu = int(self.pemain.powerup_timer["lambat"] - time.time())
            self.pen.write(
                f"WAKTU LAMBAT: {sisa_waktu}s",
                align="center",
                font=("Courier", 14, "normal"),
                color="yellow",
            )

    def spawn_objek(self):
        if random.random() < self.delay_spawn:
            pilihan = random.choices(
                [
                    "apel",
                    "apel_emas",
                    "bom",
                    "powerup_perisai",
                    "powerup_lambat",
                    "powerup_lebar",
                ],
                weights=[50, 5, 30, 5, 5, 5],
                k=1,
            )[0]
            objek_baru = ObjekJatuh(pilihan)
            objek_baru.reset_posisi()
            self.daftar_objek.append(objek_baru)

    def update_objek(self):
        for objek in self.daftar_objek:
            kecepatan = (
                objek.kecepatan_jatuh * 0.3
                if self.waktu_lambat_aktif
                else objek.kecepatan_jatuh
            )
            objek.sety(objek.ycor() - kecepatan)
            if hasattr(objek, "ekstra_turtle"):
                objek.ekstra_turtle.sety(objek.ekstra_turtle.ycor() - kecepatan)

            if objek.distance(self.pemain) < 40:
                self.handle_koleksi(objek)
                # Hapus ekstra turtle saat dikoleksi
                if hasattr(objek, "ekstra_turtle"):
                    objek.ekstra_turtle.clear()
                    objek.ekstra_turtle.hideturtle()
                objek.hideturtle()
                self.daftar_objek.remove(objek)

            if objek.ycor() < -TINGGI_LAYAR // 2:
                if objek.tipe in ["apel", "apel_emas"]:
                    self.nyawa -= 1
                # Hapus ekstra turtle saat jatuh
                if hasattr(objek, "ekstra_turtle"):
                    objek.ekstra_turtle.clear()
                    objek.ekstra_turtle.hideturtle()
                objek.hideturtle()
                self.daftar_objek.remove(objek)

    def handle_koleksi(self, objek):
        if objek.tipe == "apel":
            self.skor += objek.skor
            self.efek_visual.tambah_efek_teks(
                objek.xcor(), objek.ycor(), "+10", "green"
            )
        elif objek.tipe == "apel_emas":
            self.skor += objek.skor
            self.efek_visual.tambah_efek_teks(objek.xcor(), objek.ycor(), "+50", "gold")
        elif objek.tipe == "bom":
            self.efek_visual.tambah_efek_ledakan(objek.xcor(), objek.ycor())
            if self.pemain.perisai_aktif:
                self.pemain.perisai_aktif = False
                self.pemain.update_perisai_visual()
            else:
                self.nyawa -= 1
        elif objek.tipe == "powerup_perisai":
            self.pemain.perisai_aktif = True
            self.pemain.update_perisai_visual()
        elif objek.tipe == "powerup_lambat":
            self.waktu_lambat_aktif = True
            self.pemain.powerup_timer["lambat"] = time.time() + 5
        elif objek.tipe == "powerup_lebar":
            self.pemain.shapesize(
                stretch_wid=1, stretch_len=self.pemain.lebar_standar * 2
            )
            self.pemain.powerup_timer["lebar"] = time.time() + 7

        if self.skor % 100 == 0 and self.skor > 0:
            for o in self.daftar_objek:
                o.kecepatan_jatuh *= 1.1

    def update_powerups(self):
        waktu_sekarang = time.time()
        if (
            "lambat" in self.pemain.powerup_timer
            and waktu_sekarang > self.pemain.powerup_timer["lambat"]
        ):
            self.waktu_lambat_aktif = False
            del self.pemain.powerup_timer["lambat"]

        if (
            "lebar" in self.pemain.powerup_timer
            and waktu_sekarang > self.pemain.powerup_timer["lebar"]
        ):
            self.pemain.shapesize(stretch_wid=1, stretch_len=self.pemain.lebar_standar)
            del self.pemain.powerup_timer["lebar"]

    def run(self):
        while True:
            if self.game_state == "MENU":
                self.show_menu()
                self.window.update()
                time.sleep(DELAY_GAME)
            elif self.game_state == "PLAYING":
                self.spawn_objek()
                self.update_objek()
                self.update_powerups()
                self.update_ui()
                self.efek_visual.update()
                self.window.update()
                time.sleep(DELAY_GAME)
                if self.nyawa <= 0:
                    self.game_state = "GAME_OVER"
            elif self.game_state == "PAUSED":
                self.show_pause()
                self.window.update()
                time.sleep(DELAY_GAME)
            elif self.game_state == "GAME_OVER":
                self.show_game_over()
                self.window.update()
                time.sleep(DELAY_GAME)


# --- MEMULAI GAME ---
if __name__ == "__main__":
    game = Game()
    game.run()
