from pygame import *
from random import randint
from time import time as timer #імпортуємо функцію для засікання часу, щоб інтерпретатор не шукав цю функцію в pygame модулі time, даємо їй іншу назву самі


#підвантажуємо окремо функції для роботи зі шрифтом


# шрифти і написи
font.init()
font1 = font.Font(None, 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
font2 = font.Font(None, 36)


# фонова музика
mixer.init()
mixer.music.load('music.mp3')
mixer.music.play()
 
# нам потрібні такі картинки:
img_back = "fon.png"  # фон гри
img_hero = "mycar2.png"  # герой
img_enemy = "carwar.png"  # ворог

score = 0  # збито кораблів
goal = 10 # стільки кораблів потрібно збити для перемоги
lost = 30  # пропущено кораблів
max_lost = 3 # програли, якщо пропустили стільки
life = 3  # очки життя


# клас-батько для інших спрайтів
class GameSprite(sprite.Sprite):
    # конструктор класу
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # викликаємо конструктор класу (Sprite):
        sprite.Sprite.__init__(self)
 
        # кожен спрайт повинен зберігати властивість image - зображення
        self.image = transform.scale(
            image.load(player_image), (size_x, size_y))
        self.speed = player_speed
 
        # кожен спрайт повинен зберігати властивість rect - прямокутник, в який він вписаний
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
    # метод, що малює героя у вікні
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
 
# клас головного гравця
class Player(GameSprite):
    # метод для керування спрайтом стрілками клавіатури
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 20:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed
                # метод "постріл" (використовуємо місце гравця, щоб створити там кулю)

 
# клас спрайта-ворога
class Enemy(GameSprite):
    # рух ворога
    def update(self):
        self.rect.y += self.speed
        global lost
        # зникає, якщо дійде до краю екрана
        if self.rect.y > win_height:
            self.rect.x = randint(0, win_width)
            self.rect.y = 0
            lost-=1
           


# клас спрайта-кулі  


# створюємо віконце
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
 
# створюємо спрайти
ship = Player(img_hero, 5, win_height - 100, 50, 100, 10)


# створення групи спрайтів-ворогів
monsters = sprite.Group()
for i in range(5, 10):
    monster = Enemy(img_enemy, randint(
        0, win_width), -40, 80, 50, randint(15, 20))
    monsters.add(monster)


# створення групи спрайтів-астероїдів



bullets = sprite.Group()


# змінна "гра закінчилася": як тільки вона стає True, в основному циклі перестають працювати спрайти
finish = False
# Основний цикл гри:
run = True  # прапорець скидається кнопкою закриття вікна


rel_time = False  # прапор, що відповідає за перезаряджання


num_fire = 0  # змінна для підрахунку пострілів    
by = 0

while run:
    # подія натискання на кнопку Закрити
    for e in event.get():
        if e.type == QUIT:
            run = False
        #подія натискання на пробіл - спрайт стріляє


    # сама гра: дії спрайтів, перевірка правил гри, перемальовка
    if not finish:
        # оновлюємо фон
        window.blit(background, (0, by))
        window.blit(background,(0, by-500))


        # рухи спрайтів
        ship.update()
        monsters.update()
    
        
 
        #оновлюємо їх у новому місці при кожній ітерації циклу
        ship.reset()
        monsters.draw(window)
        


        # перезарядка
        
        # якщо спрайт торкнувся ворога зменшує життя
        if sprite.spritecollide(ship, monsters, False):
            sprite.spritecollide(ship, monsters, True)
           
            for i in range(1):
                monster = Enemy(img_enemy, randint(0, win_width), -40, 80, 50, randint(1, 5))
                monsters.add(monster)
            life = life -1


        #програш
        if life == 0:
            finish = True # проиграли, ставим фон и больше не управляем спрайтами.
            window.blit(lose, (200, 200))


        # перевірка виграшу: скільки очок набрали?
        if lost <= 0:
            finish = True
            window.blit(win, (200, 200))


        # пишемо текст на екрані
        text = font2.render("Рахунок: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
 
        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))


        # задаємо різний колір залежно від кількості життів
        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0, 0)

        by += 5
        if by == 500:
            by = 0
       
        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (650, 10))


        display.update()


    #бонус: автоматичний перезапуск гри
    else:
        mixer.music.play()
        finish = False
        score = 0
        lost = 30
        num_fire = 0
        life = 3
        for m in monsters:
            m.kill()
       
     
        time.delay(3000)
        for i in range(5, 10):
            monster = Enemy(img_enemy, randint(0, win_width ), -40, 80, 50, randint(15, 20))
            monsters.add(monster) 


    # цикл спрацьовує кожні 0.05 секунд
    time.delay(50)
