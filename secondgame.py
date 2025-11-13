import turtle
import random
import time
import os
import winsound
import math

# --- KONSTANTA ---
LEBAR_LAYAR = 1000
TINGGI_LAYAR = 800
LEBAR_MINIMAP = 150
TINGGI_MINIMAP = 150
WARNA_LANGIT_SIANG = "#87CEEB"
WARNA_LANGIT_PAGI = "#FFD700"
WARNA_LANGIT_MALAM = "#191970"
WARNA_LANGIT_SUBUH = "#4B0082"
WARNA_HUJAN = "#A9A9A9"

# --- MANAJER SUARA ---
class SoundManager:
    @staticmethod
    def play(sound_type):
        try:
            if sound_type == "chop": winsound.Beep(500, 50)
            elif sound_type == "eat": winsound.Beep(1000, 100)
            elif sound_type == "craft": winsound.Beep(800, 150)
            elif sound_type == "hurt": winsound.Beep(200, 200)
            elif sound_type == "shoot": winsound.Beep(1500, 50)
            elif sound_type == "night": winsound.Beep(150, 1000)
            elif sound_type == "rain": winsound.Beep(300, 200) # Suara petir singkat
        except: pass

# --- KELAS-KELAS SISTEM ---

class Particle(turtle.Turtle):
    def __init__(self, x, y, color, velocity, size=0.1):
        super().__init__()
        self.hideturtle()
        self.penup()
        self.speed(0)
        self.goto(x, y)
        self.color(color)
        self.shape("circle")
        self.shapesize(stretch_wid=size, stretch_len=size)
        self.velocity = velocity
        self.lifetime = 20
        self.showturtle()

    def update(self):
        self.setx(self.xcor() + self.velocity[0])
        self.sety(self.ycor() + self.velocity[1])
        self.velocity = (self.velocity[0] * 0.95, self.velocity[1] * 0.95)
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.clear()
            self.hideturtle()
            return False
        return True

class ParticleSystem:
    def __init__(self):
        self.particles = []
    def emit(self, x, y, color, count=10, speed=3, size=0.1):
        for _ in range(count):
            velocity = (random.uniform(-speed, speed), random.uniform(-speed, 0))
            self.particles.append(Particle(x, y, color, velocity, size))
    def update(self):
        for particle in self.particles[:]:
            if not particle.update():
                self.particles.remove(particle)

class Weather:
    def __init__(self, renderer):
        self.renderer = renderer
        self.is_raining = False
        self.rain_timer = 0
        self.rain_particles = []
        self.next_rain_change = time.time() + random.randint(30, 60)

    def update(self):
        if time.time() > self.next_rain_change:
            self.is_raining = not self.is_raining
            self.next_rain_change = time.time() + random.randint(30, 90)
            if self.is_raining:
                SoundManager.play("rain")
        
        if self.is_raining:
            for _ in range(5):
                x = random.randint(-LEBAR_LAYAR//2, LEBAR_LAYAR//2)
                y = TINGGI_LAYAR//2
                self.rain_particles.append(Particle(x, y, WARNA_HUJAN, (0, -random.uniform(8, 12)), 0.05))
            
            for particle in self.rain_particles[:]:
                if not particle.update():
                    self.rain_particles.remove(particle)

class Minimap(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.penup()
        self.speed(0)
        self.pensize(1)
        
    def draw(self, player, resources, predators, structures):
        self.clear()
        # Background
        self.goto(LEBAR_LAYAR//2 - LEBAR_MINIMAP//2 - 10, TINGGI_LAYAR//2 - 10)
        self.pendown()
        self.fillcolor("black")
        self.begin_fill()
        for _ in range(2):
            self.forward(LEBAR_MINIMAP)
            self.right(90)
            self.forward(TINGGI_MINIMAP)
            self.right(90)
        self.end_fill()
        self.penup()

        # Draw objects
        scale_x = LEBAR_MINIMAP / LEBAR_LAYAR
        scale_y = TINGGI_MINIMAP / TINGGI_LAYAR

        # Resources
        for res in resources:
            if res.jumlah > 0:
                x = LEBAR_LAYAR//2 - LEBAR_MINIMAP//2 - 10 + (res.x + LEBAR_LAYAR//2) * scale_x
                y = TINGGI_LAYAR//2 - 10 - (res.y + TINGGI_LAYAR//2) * scale_y
                self.goto(x, y)
                if res.tipe == "pohon": self.dot(3, "green")
                elif res.tipe == "batu": self.dot(3, "gray")
                elif res.tipe == "beri": self.dot(3, "red")
        
        # Structures
        for struct in structures:
            x = LEBAR_LAYAR//2 - LEBAR_MINIMAP//2 - 10 + (struct.x + LEBAR_LAYAR//2) * scale_x
            y = TINGGI_LAYAR//2 - 10 - (struct.y + TINGGI_LAYAR//2) * scale_y
            self.goto(x, y)
            self.dot(5, "brown")

        # Predators
        for pred in predators:
            x = LEBAR_LAYAR//2 - LEBAR_MINIMAP//2 - 10 + (pred.xcor() + LEBAR_LAYAR//2) * scale_x
            y = TINGGI_LAYAR//2 - 10 - (pred.ycor() + TINGGI_LAYAR//2) * scale_y
            self.goto(x, y)
            self.dot(3, "darkred")

        # Player
        px = LEBAR_LAYAR//2 - LEBAR_MINIMAP//2 - 10 + (player.xcor() + LEBAR_LAYAR//2) * scale_x
        py = TINGGI_LAYAR//2 - 10 - (player.ycor() + TINGGI_LAYAR//2) * scale_y
        self.goto(px, py)
        self.dot(4, "blue")


class Projectile(turtle.Turtle):
    def __init__(self, x, y, angle):
        super().__init__()
        self.shape("square")
        self.shapesize(0.2, 0.5)
        self.color("saddlebrown")
        self.penup()
        self.speed(0)
        self.goto(x, y)
        self.setheading(angle)
        self.kecepatan = 20
        self.lifetime = 40

    def update(self):
        self.forward(self.kecepatan)
        self.lifetime -= 1
        if self.lifetime <= 0 or not (-LEBAR_LAYAR//2 < self.xcor() < LEBAR_LAYAR//2 and -TINGGI_LAYAR//2 < self.ycor() < TINGGI_LAYAR//2):
            self.hideturtle()
            return False
        return True

class Structure:
    def __init__(self, renderer, tipe, x, y):
        self.renderer = renderer
        self.tipe = tipe
        self.x = x
        self.y = y
        self.health = 100

    def draw(self):
        if self.tipe == "wall":
            self.renderer.draw_wall(self.x, self.y)
        elif self.tipe == "shelter":
            self.renderer.draw_shelter(self.x, self.y)

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            return True # Hancur
        return False

# --- KELAS RENDERER ---
class Renderer:
    def __init__(self, pen):
        self.pen = pen
        self.pen.speed(0)
        self.pen.hideturtle()
        self.stars = self.generate_stars()

    def generate_stars(self):
        return [(random.randint(-LEBAR_LAYAR//2, LEBAR_LAYAR//2), random.randint(100, TINGGI_LAYAR//2)) for _ in range(150)]

    def draw_sky(self, waktu, siang):
        progress = 1 - (waktu / 180)
        if siang:
            if progress < 0.2: color = WARNA_LANGIT_SUBUH
            elif progress < 0.3: color = WARNA_LANGIT_PAGI
            else: color = WARNA_LANGIT_SIANG
        else:
            if progress > 0.8: color = WARNA_LANGIT_SUBUH
            else: color = WARNA_LANGIT_MALAM
        turtle.bgcolor(color)
        
        if not siang:
            self.pen.color("white")
            for star in self.stars:
                self.pen.goto(star[0], star[1])
                self.pen.dot(random.uniform(1, 2))

    def draw_celestial_body(self, waktu, siang):
        self.pen.penup()
        progress = 1 - (waktu / 180)
        x = LEBAR_LAYAR * progress - LEBAR_LAYAR / 2
        y = TINGGI_LAYAR / 2 - 50
        if siang: self.pen.color("yellow"); self.pen.goto(x, y); self.pen.dot(40)
        else: self.pen.color("lightgray"); self.pen.goto(x, y); self.pen.dot(35); self.pen.color(WARNA_LANGIT_MALAM); self.pen.goto(x + 10, y); self.pen.dot(35)

    def draw_ground(self):
        self.pen.penup(); self.pen.goto(-LEBAR_LAYAR//2, -TINGGI_LAYAR//2); self.pen.pendown()
        self.pen.fillcolor("#654321"); self.pen.begin_fill()
        for _ in range(2): self.pen.forward(LEBAR_LAYAR); self.pen.left(90); self.pen.forward(150); self.pen.left(90)
        self.pen.end_fill(); self.pen.penup()

    def draw_tree(self, x, y):
        self.pen.color("saddlebrown"); self.pen.penup(); self.pen.goto(x, y); self.pen.pendown(); self.pen.width(10); self.pen.setheading(90); self.pen.forward(60); self.pen.width(1)
        self.pen.penup(); self.pen.goto(x - 30, y + 40); self.pen.pendown(); self.pen.fillcolor("green"); self.pen.begin_fill(); self.pen.circle(30); self.pen.end_fill(); self.pen.penup()

    def draw_rock(self, x, y):
        self.pen.penup(); self.pen.goto(x, y); self.pen.pendown(); self.pen.fillcolor("gray"); self.pen.begin_fill()
        self.pen.setheading(60); self.pen.forward(20); self.pen.right(120); self.pen.forward(20); self.pen.right(120); self.pen.forward(20); self.pen.end_fill(); self.pen.penup()

    def draw_berry_bush(self, x, y):
        self.pen.penup(); self.pen.goto(x, y); self.pen.pendown(); self.pen.color("darkgreen"); self.pen.dot(25)
        self.pen.color("red"); for _ in range(5): self.pen.goto(x + random.randint(-10, 10), y + random.randint(-10, 10)); self.pen.dot(5); self.pen.penup()

    def draw_player(self, x, y, facing_right, is_shooting):
        self.pen.penup(); self.pen.goto(x, y); self.pen.color("saddlebrown"); self.pen.pendown(); self.pen.width(3); self.pen.setheading(90); self.pen.forward(20)
        self.pen.penup(); self.pen.goto(x, y + 20); self.pen.color("peachpuff"); self.pen.dot(15)
        self.pen.color("saddlebrown"); self.pen.width(2); self.pen.goto(x - 5, y); self.pen.pendown()
        self.pen.setheading(-45 if facing_right else -135); self.pen.forward(10)
        self.pen.penup(); self.pen.goto(x + 5, y); self.pen.pendown()
        self.pen.setheading(-135 if facing_right else -45); self.pen.forward(10)
        
        if is_shooting:
            self.pen.penup(); self.pen.goto(x + (10 if facing_right else -10), y + 15)
            self.pen.color("saddlebrown"); self.pen.pendown(); self.pen.width(2)
            self.pen.setheading(45 if facing_right else 135); self.pen.forward(20)
            self.pen.setheading(0 if facing_right else 180); self.pen.forward(15)
            self.pen.penup(); self.pen.width(1)

    def draw_predator(self, x, y):
        self.pen.penup(); self.pen.goto(x, y); self.pen.pendown(); self.pen.color("darkred"); self.pen.width(3)
        for _ in range(8): self.pen.forward(5); self.pen.left(45); self.pen.forward(5); self.pen.right(90); self.pen.forward(5); self.pen.left(45)
        self.pen.penup(); self.pen.width(1)

    def draw_campfire(self, x, y):
        for i in range(3):
            self.pen.goto(x + random.randint(-5,5), y)
            self.pen.color("orange" if i % 2 == 0 else "red")
            self.pen.dot(random.randint(5, 10))

    def draw_wall(self, x, y):
        self.pen.penup(); self.pen.goto(x-15, y-15); self.pen.pendown(); self.pen.fillcolor("#8B4513"); self.pen.begin_fill()
        for _ in range(2): self.pen.forward(30); self.pen.left(90); self.pen.forward(30); self.pen.left(90)
        self.pen.end_fill(); self.pen.penup()

    def draw_shelter(self, x, y):
        self.pen.penup(); self.pen.goto(x-40, y-20); self.pen.pendown(); self.pen.fillcolor("#A0522D"); self.pen.begin_fill()
        for _ in range(2): self.pen.forward(80); self.pen.left(90); self.pen.forward(60); self.pen.left(90)
        self.pen.end_fill()
        # Atap
        self.pen.goto(x-50, y-20); self.pen.fillcolor("#654321"); self.pen.begin_fill()
        self.pen.setheading(0); self.pen.forward(100); self.pen.setheading(150); self.pen.forward(60); self.pen.setheading(210); self.pen.forward(60)
        self.pen.end_fill(); self.pen.penup()

    def draw_ui_bar(self, x, y, label, value, max_value, color):
        self.pen.goto(x, y + 15); self.pen.color("black"); self.pen.write(label, font=("Courier", 12, "bold"))
        self.pen.goto(x, y); self.pen.pendown(); self.pen.color("gray")
        for _ in range(2): self.pen.forward(104); self.pen.left(90); self.pen.forward(14); self.pen.left(90); self.pen.forward(104); self.pen.left(90); self.pen.forward(14); self.pen.left(90)
        self.pen.penup()
        if value > 0:
            self.pen.goto(x + 2, y + 2); self.pen.pendown(); self.pen.fillcolor(color); self.pen.begin_fill()
            bar_width = (value / max_value) * 100; self.pen.forward(bar_width); self.pen.left(90); self.pen.forward(10); self.pen.left(90); self.pen.forward(bar_width); self.pen.left(90); self.pen.forward(10); self.pen.left(90)
            self.pen.end_fill(); self.pen.penup()

# --- KELAS-KELAS GAME ---

class Pemain(turtle.Turtle):
    def __init__(self, renderer, particle_system):
        super().__init__()
        self.renderer = renderer; self.particle_system = particle_system
        self.shape("square"); self.shapesize(0.1, 0.1); self.penup(); self.speed(0)
        self.health = 100; self.hunger = 100; self.kecepatan = 15
        self.inventori = {"kayu": 0, "batu": 0, "beri": 0, "serat": 0, "tali": 0, "busur": 0, "panah": 0}
        self.mempunyai_kapak = False; self.mempunyai_perapian = False
        self.facing_right = True; self.last_x = 0; self.is_shooting = False

    def update_visual(self):
        if self.xcor() > self.last_x: self.facing_right = True
        elif self.xcor() < self.last_x: self.facing_right = False
        self.last_x = self.xcor()
        self.renderer.draw_player(self.xcor(), self.ycor(), self.facing_right, self.is_shooting)
        self.is_shooting = False

    def gerak_atas(self):
        if self.ycor() < -50: self.sety(self.ycor() + self.kecepatan)
    def gerak_bawah(self):
        if self.ycor() > -TINGGI_LAYAR // 2 + 20: self.sety(self.ycor() - self.kecepatan)
    def gerak_kiri(self):
        if self.xcor() > -LEBAR_LAYAR // 2 + 20: self.setx(self.xcor() - self.kecepatan)
    def gerak_kanan(self):
        if self.xcor() < LEBAR_LAYAR // 2 - 20: self.setx(self.xcor() + self.kecepatan)
            
    def makan_beri(self):
        if self.inventori["beri"] > 0 and self.hunger < 100:
            self.inventori["beri"] -= 1; self.hunger = min(100, self.hunger + 30); SoundManager.play("eat")
            self.particle_system.emit(self.xcor(), self.ycor(), "green", 5, 2); return True
        return False

    def tembak(self, projectiles):
        if self.inventori["busur"] > 0 and self.inventori["panah"] > 0:
            self.is_shooting = True
            angle = self.towards(mouse_x, mouse_y)
            projectiles.append(Projectile(self.xcor(), self.ycor() + 20, angle))
            self.inventori["panah"] -= 1
            SoundManager.play("shoot")


class SumberDaya:
    def __init__(self, renderer, tipe, x, y):
        self.renderer = renderer; self.tipe = tipe; self.x = x; self.y = y
        self.jumlah = random.randint(3, 5); self.waktu_respawn = 0

    def gambar(self):
        if self.jumlah > 0:
            if self.tipe == "pohon": self.renderer.draw_tree(self.x, self.y)
            elif self.tipe == "batu": self.renderer.draw_rock(self.x, self.y)
            elif self.tipe == "beri": self.renderer.draw_berry_bush(self.x, self.y)

    def kumpulkan(self, pemain):
        if self.tipe == "pohon":
            hasil = 2 if pemain.mempunyai_kapak else 1
            pemain.inventori["kayu"] += hasil; pemain.inventori["serat"] += 1
            SoundManager.play("chop"); pemain.particle_system.emit(self.x, self.y + 30, "saddlebrown", 5)
        elif self.tipe == "batu":
            pemain.inventori["batu"] += 1
        elif self.tipe == "beri":
            pemain.inventori["beri"] += 1
        self.jumlah -= 1
        if self.jumlah <= 0: self.waktu_respawn = time.time() + 30

    def update(self):
        if self.waktu_respawn > 0 and time.time() > self.waktu_respawn:
            self.jumlah = random.randint(3, 5); self.waktu_respawn = 0

class Predator(turtle.Turtle):
    def __init__(self, renderer, particle_system):
        super().__init__()
        self.renderer = renderer; self.particle_system = particle_system
        self.shape("square"); self.shapesize(0.1, 0.1); self.penup(); self.speed(0)
        self.kecepatan = random.uniform(1.5, 2.5); self.health = 50
        self.goto(random.randint(-300, 300), random.randint(-200, 200))

    def gambar(self):
        self.renderer.draw_predator(self.xcor(), self.ycor())

    def bergerak(self, pemain):
        if self.distance(pemain) > 20:
            self.setheading(self.towards(pemain.xcor(), pemain.ycor())); self.forward(self.kecepatan)

    def serang(self, pemain):
        if self.distance(pemain) < 20:
            if pemain.mempunyai_perapian:
                self.setheading(self.towards(pemain.xcor(), pemain.ycor()) + 180); self.forward(self.kecepatan * 5)
            else:
                SoundManager.play("hurt"); pemain.particle_system.emit(pemain.xcor(), pemain.ycor(), "red", 10); return True
        return False

    def take_damage(self, amount):
        self.health -= amount
        self.particle_system.emit(self.xcor(), self.ycor(), "darkred", 5)
        if self.health <= 0:
            return True # Mati
        return False

# --- GAME UTAMA ---
class Game:
    def __init__(self):
        self.window = turtle.Screen(); self.window.title("Stone Age Survivor: Ultimate Edition"); self.window.bgcolor(WARNA_LANGIT_SIANG)
        self.window.setup(width=LEBAR_LAYAR, height=TINGGI_LAYAR); self.window.tracer(0)
        self.pen = turtle.Turtle()
        self.renderer = Renderer(self.pen)
        self.particle_system = ParticleSystem()
        self.weather = Weather(self.renderer)
        self.minimap = Minimap()
        
        self.pemain = Pemain(self.renderer, self.particle_system)
        self.daftar_sumberdaya = []; self.daftar_predator = []; self.daftar_struktur = []
        self.projectiles = []
        
        self.hari = 1; self.waktu = 180; self.siang = True; self.game_state = "MENU"
        self.high_score = self.load_high_score()
        self.build_mode = None; self.ghost_structure = None

        self.generate_dunia(); self.setup_keyboard()
        global mouse_x, mouse_y
        mouse_x, mouse_y = 0, 0
        self.window.getcanvas().bind("<Motion>", self.on_mouse_move)
        self.window.getcanvas().bind("<Button-1>", self.on_mouse_click)

    def on_mouse_move(self, event):
        global mouse_x, mouse_y
        mouse_x = event.x - LEBAR_LAYAR // 2
        mouse_y = -event.y + TINGGI_LAYAR // 2

    def on_mouse_click(self, event):
        if self.build_mode and self.game_state == "PLAYING":
            x = event.x - LEBAR_LAYAR // 2
            y = -event.y + TINGGI_LAYAR // 2
            if self.place_structure(self.build_mode, x, y):
                self.build_mode = None
                if self.ghost_structure:
                    self.ghost_structure.hideturtle()
                    self.ghost_structure = None

    def load_high_score(self):
        if os.path.exists("survivor_ultimate_highscore.txt"):
            with open("survivor_ultimate_highscore.txt", "r") as f: return int(f.read())
        return 0

    def save_high_score(self):
        with open("survivor_ultimate_highscore.txt", "w") as f: f.write(str(self.high_score))

    def generate_dunia(self):
        for _ in range(10):
            x = random.randint(-LEBAR_LAYAR//2 + 50, LEBAR_LAYAR//2 - 50); y = random.randint(-40, 200)
            self.daftar_sumberdaya.append(SumberDaya(self.renderer, "pohon", x, y))
        for _ in range(6):
            x = random.randint(-LEBAR_LAYAR//2 + 50, LEBAR_LAYAR//2 - 50); y = random.randint(-40, 200)
            self.daftar_sumberdaya.append(SumberDaya(self.renderer, "batu", x, y))
        for _ in range(8):
            x = random.randint(-LEBAR_LAYAR//2 + 50, LEBAR_LAYAR//2 - 50); y = random.randint(-40, 200)
            self.daftar_sumberdaya.append(SumberDaya(self.renderer, "beri", x, y))

    def setup_keyboard(self):
        self.window.listen()
        self.window.onkeypress(self.pemain.gerak_atas, "Up"); self.window.onkeypress(self.pemain.gerak_bawah, "Down")
        self.window.onkeypress(self.pemain.gerak_kiri, "Left"); self.window.onkeypress(self.pemain.gerak_kanan, "Right")
        self.window.onkeypress(self.buka_menu_crafting, "c"); self.window.onkeypress(self.pemain.makan_beri, "e")
        self.window.onkeypress(self.start_game, "space"); self.window.onkeypress(self.quit_game, "Escape")
        self.window.onkeypress(lambda: self.set_build_mode("wall"), "1")
        self.window.onkeypress(lambda: self.set_build_mode("shelter"), "2")
        self.window.onkeypress(self.pemain.tembak, "f") # F untuk fire/shoot

    def set_build_mode(self, tipe):
        if self.game_state == "PLAYING":
            self.build_mode = tipe
            if not self.ghost_structure:
                self.ghost_structure = turtle.Turtle()
                self.ghost_structure.hideturtle(); self.ghost_structure.penup(); self.ghost_structure.speed(0)
            self.ghost_structure.shape("square"); self.ghost_structure.color("gray"); self.ghost_structure.shapesize(0.5, 0.5)

    def place_structure(self, tipe, x, y):
        cost = {"wall": {"kayu": 5}, "shelter": {"kayu": 10, "batu": 5}}
        item_cost = cost.get(tipe, {})
        can_build = all(self.pemain.inventori[res] >= amt for res, amt in item_cost.items())
        
        if can_build:
            for res, amt in item_cost.items(): self.pemain.inventori[res] -= amt
            self.daftar_struktur.append(Structure(self.renderer, tipe, x, y))
            SoundManager.play("craft")
            return True
        return False

    def buka_menu_crafting(self):
        if self.game_state != "PLAYING": return
        pilihan = self.window.textinput("Crafting", "1:Tali(2Serat) 2:Busur(3K,1Tali) 3:Panah(1K,1Batu) 4:Perapian(3K)")
        if pilihan == "1" and self.pemain.inventori["serat"] >= 2:
            self.pemain.inventori["serat"] -= 2; self.pemain.inventori["tali"] += 1; SoundManager.play("craft")
        elif pilihan == "2" and self.pemain.inventori["kayu"] >= 3 and self.pemain.inventori["tali"] >= 1:
            self.pemain.inventori["kayu"] -= 3; self.pemain.inventori["tali"] -= 1; self.pemain.inventori["busur"] += 1; SoundManager.play("craft")
        elif pilihan == "3" and self.pemain.inventori["kayu"] >= 1 and self.pemain.inventori["batu"] >= 1:
            self.pemain.inventori["kayu"] -= 1; self.pemain.inventori["batu"] -= 1; self.pemain.inventori["panah"] += 5; SoundManager.play("craft")
        elif pilihan == "4" and self.pemain.inventori["kayu"] >= 3 and not self.pemain.mempunyai_perapian:
            self.pemain.inventori["kayu"] -= 3; self.pemain.mempunyai_perapian = True; SoundManager.play("craft")

    def update_siklus_waktu(self):
        self.waktu -= 1
        if self.waktu <= 0:
            self.waktu = 180; self.hari += 1; self.siang = not self.siang
            if not self.siang: SoundManager.play("night")
            else: self.daftar_predator.clear()
            if not self.siang:
                for _ in range(self.hari // 2 + 1): self.daftar_predator.append(Predator(self.renderer, self.particle_system))

    def update_ui(self):
        self.renderer.draw_ui_bar(-LEBAR_LAYAR//2 + 20, TINGGI_LAYAR//2 - 40, "Health", self.pemain.health, 100, "red")
        self.renderer.draw_ui_bar(-LEBAR_LAYAR//2 + 20, TINGGI_LAYAR//2 - 80, "Hunger", self.pemain.hunger, 100, "orange")
        
        self.pen.goto(0, TINGGI_LAYAR//2 - 50); self.pen.color("black")
        inv_str = f"K:{self.pemain.inventori['kayu']} B:{self.pemain.inventori['batu']} Be:{self.pemain.inventori['beri']} S:{self.pemain.inventori['serat']} T:{self.pemain.inventori['tali']} Bow:{self.pemain.inventori['busur']} Arr:{self.pemain.inventori['panah']}"
        self.pen.write(inv_str, align="center", font=("Courier", 10, "bold"))
        
        self.pen.goto(LEBAR_LAYAR//2 - 20, TINGGI_LAYAR//2 - 50)
        status_waktu = "Siang" if self.siang else "Malam"
        self.pen.write(f"Hari {self.hari} ({status_waktu})", align="right", font=("Courier", 16, "bold"))
        
        if self.build_mode:
            self.pen.goto(0, -TINGGI_LAYAR//2 + 50)
            self.pen.write(f"Building Mode: {self.build_mode.capitalize()}. Click to place. ESC to cancel.", align="center", font=("Courier", 12, "italic"), color="yellow")

    def show_menu(self):
        self.renderer.clear_background()
        self.pen.goto(0, 100); self.pen.write("STONE AGE SURVIVOR: ULTIMATE", align="center", font=("Courier", 24, "bold"))
        self.pen.goto(0, 30); self.pen.write(f"Hari Tertinggi: {self.high_score}", align="center", font=("Courier", 20, "normal"))
        self.pen.goto(0, -20); self.pen.write("Kumpulkan, Crafting, Bangun, dan Bertahan!", align="center", font=("Courier", 16, "italic"))
        self.pen.goto(0, -50); self.pen.write("Gunakan F untuk menembak, 1/2 untuk membangun.", align="center", font=("Courier", 14, "italic"))
        self.pen.goto(0, -90); self.pen.write("Tekan SPACE untuk Memulai", align="center", font=("Courier", 18, "normal"))

    def show_game_over(self):
        if self.hari > self.high_score: self.high_score = self.hari; self.save_high_score()
        self.renderer.clear_background()
        self.pen.goto(0, 100); self.pen.write("KAMU TELAH MENINGGAL", align="center", font=("Courier", 36, "bold"))
        self.pen.goto(0, 30); self.pen.write(f"Bertahan Selama: {self.hari} Hari", align="center", font=("Courier", 24, "normal"))
        self.pen.goto(0, -10); self.pen.write(f"Tertinggi: {self.high_score} Hari", align="center", font=("Courier", 20, "normal"))
        self.pen.goto(0, -60); self.pen.write("Tekan SPACE untuk Coba Lagi", align="center", font=("Courier", 18, "normal"))

    def start_game(self):
        if self.game_state in ["MENU", "GAME_OVER"]: self.reset_game(); self.game_state = "PLAYING"
    def quit_game(self):
        self.window.bye()
    def reset_game(self):
        self.pemain = Pemain(self.renderer, self.particle_system); self.daftar_sumberdaya.clear(); self.daftar_predator.clear(); self.daftar_struktur.clear(); self.projectiles.clear()
        self.generate_dunia(); self.hari = 1; self.waktu = 180; self.siang = True

    def run(self):
        while True:
            if self.game_state == "MENU":
                self.show_menu(); self.window.update(); time.sleep(0.1)
            elif self.game_state == "PLAYING":
                self.renderer.clear_background()
                self.renderer.draw_sky(self.waktu, self.siang)
                self.renderer.draw_celestial_body(self.waktu, self.siang)
                self.renderer.draw_ground()
                
                self.update_siklus_waktu()
                self.pemain.hunger -= 0.15 if self.weather.is_raining else 0.1
                if self.pemain.hunger <= 0: self.pemain.health -= 0.5
                
                for sumber in self.daftar_sumberdaya:
                    sumber.update(); sumber.gambar()
                    if self.pemain.distance(sumber.x, sumber.y) < 40 and sumber.jumlah > 0: sumber.kumpulkan(self.pemain)
                
                for struct in self.daftar_struktur: struct.draw()

                if not self.siang:
                    for predator in self.daftar_predator[:]:
                        predator.bergerak(self.pemain); predator.gambar()
                        if predator.serang(self.pemain): self.pemain.health -= 10

                for proj in self.projectiles[:]:
                    if not proj.update(): self.projectiles.remove(proj)
                    else:
                        for predator in self.daftar_predator[:]:
                            if proj.distance(predator) < 20:
                                if predator.take_damage(25):
                                    predator.hideturtle()
                                    self.daftar_predator.remove(predator)
                                self.projectiles.remove(proj)
                                break
                
                self.pemain.update_visual()
                self.particle_system.update()
                self.weather.update()
                self.weather.rain_particles.extend(self.particle_system.particles) # Gabungkan partikel
                self.minimap.draw(self.pemain, self.daftar_sumberdaya, self.daftar_predator, self.daftar_struktur)

                if self.build_mode and self.ghost_structure:
                    self.ghost_structure.showturtle()
                    self.ghost_structure.goto(mouse_x, mouse_y)
                elif self.ghost_structure:
                    self.ghost_structure.hideturtle()

                if self.pemain.mempunyai_perapian:
                    self.renderer.draw_campfire(self.pemain.xcor(), self.pemain.ycor() - 40)

                self.update_ui()
                if self.pemain.health <= 0: self.game_state = "GAME_OVER"
                
                self.window.update(); time.sleep(0.05)
            elif self.game_state == "GAME_OVER":
                self.show_game_over(); self.window.update(); time.sleep(0.1)

# --- MEMULAI GAME ---
if __name__ == "__main__":
    game = Game()
    game.run()