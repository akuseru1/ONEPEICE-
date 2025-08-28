import pygame
import sys
import math

pygame.init()

WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("サルでもわかるONE PIECE")
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (80, 80, 80)
BROWN = (148, 58, 2)


font_title = pygame.font.SysFont("msgothic", 60)
font_button = pygame.font.SysFont("msgothic", 36)
font_sentence_1 = pygame.font.SysFont("msgothic", 15)
font_sentence_2 = pygame.font.SysFont("msgothic", 12)
font_sentence_3 = pygame.font.SysFont("msgothic", 15)

start_button = pygame.Rect(100, 380, 200, 50)
save_button = pygame.Rect(100, 460, 200, 50)
load_button = pygame.Rect(100, 540, 200, 50)

chapter_1_button = pygame.Rect(10, 110, 200, 50)

chapter_screen = False
buttons = {
    "chapter_1": pygame.Rect(850, 100, 100, 100),
    "chapter_2": pygame.Rect(745, 125, 50, 50),
    "chapter_3": pygame.Rect(720, 200, 100, 100),
    "chapter_4": pygame.Rect(615, 225, 50, 50),
    "chapter_5": pygame.Rect(590, 300, 100, 100),
    "return_4": pygame.Rect(0, 0, 50, 50),
    "shop_button": pygame.Rect(785, 535, 200, 50)
}

route_points = [
    (850, 150),
    (770, 150),
    (770, 200),
    (720, 250),
    (640, 250),
    (640, 300),
    (640, 350)
]

button_targets = {
    "chapter_1": (buttons["chapter_1"].centerx, buttons["chapter_1"].top),
    "chapter_2": (buttons["chapter_2"].centerx, buttons["chapter_2"].top),
    "chapter_3": (buttons["chapter_3"].centerx, buttons["chapter_3"].top),
    "chapter_4": (buttons["chapter_4"].centerx, buttons["chapter_4"].top),
    "chapter_5": (buttons["chapter_5"].centerx, buttons["chapter_5"].top)
}

shop_buttons = {
    "shop_title": pygame.Rect(0, 0, 1000, 150),
    "rozya_syouhin" : pygame.Rect(50, 310, 150, 50),
    "Rocks_syouhin" : pygame.Rect(220, 310, 170, 50)
}


moving = False
move_path = []
move_index = 0
speed = 1.5j

def find_route(start, goal, route_points):
    def nearest(pt):
        return min(route_points, key=lambda p: math.hypot(pt[0]-p[0], pt[1]-p[1]))
    start_p = nearest(start)
    goal_p = nearest(goal)
    start_idx = route_points.index(start_p)
    goal_idx = route_points.index(goal_p)
    if start_idx <= goal_idx:
        path = route_points[start_idx:goal_idx+1]
    else:
        path = [route_points[i] for i in range(start_idx, goal_idx-1, -1)]
    path = [start] + path + [goal]
    return path

try:
    image = pygame.image.load("img/ルフィ.png")
    image = pygame.transform.scale(image, (400, 400))

    kyara_list = {

        "stop_image" : pygame.image.load("img/ルフィ停止画像.png"),
        "rozya_stop_image" : pygame.image.load("img/ロジャードット絵.png"),
        "Rocks_image" : pygame.image.load("img/ロックスDジーベック_ドット絵.png"),
    }

    stop_image = pygame.transform.scale(kyara_list["stop_image"], (50, 65))        
    rozya_stop_image = pygame.transform.scale(kyara_list["rozya_stop_image"], (170, 130))
    Rocks_image = pygame.transform.scale(kyara_list["Rocks_image"], (140, 140))

    kazi = pygame.image.load("img/舵 2.png")
    kazi = pygame.transform.scale(kazi, (150, 150))
    ikari = pygame.image.load("img/碇.png")
    ikari = pygame.transform.scale(ikari, (300, 300))
    ikari = pygame.transform.rotate(ikari, 45)

except:
    image = None

game_started = False
kidou = False

stop_image_rect = stop_image.get_rect(center=(buttons["chapter_1"].centerx, buttons["chapter_1"].top))

shop_start = False
kyara = ("rufi")
stop_image_rect = stop_image.get_rect(center=(buttons["chapter_1"].x + 50, buttons["chapter_1"].y + 10))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if buttons["shop_button"].collidepoint(event.pos):
                shop_start = True
            if game_started and chapter_screen:
                for btn_name, btn_rect in buttons.items():
                    if btn_name.startswith("chapter_") and btn_rect.collidepoint(event.pos):
                        goal_pos = button_targets.get(btn_name)
                        if goal_pos and not stop_image_rect.collidepoint(goal_pos):
                            move_path = find_route(stop_image_rect.center, goal_pos, route_points)
                            move_index = 1
                            moving = True
            if not game_started and start_button.collidepoint(event.pos):
                game_started = True
                kidou = True
            elif not chapter_screen and chapter_1_button.collidepoint(event.pos):
                chapter_screen = True
                chapter = 1
            elif game_started and buttons["return_4"].collidepoint(event.pos):
                if chapter_screen:
                    chapter_screen = False
                elif game_started:
                    game_started = False
            elif buttons["return_4"].collidepoint(event.pos):
                if shop_start:
                    shop_start = False
                    
            if not game_started and start_button.collidepoint(event.pos):
                game_started = True
                kidou = True
            elif not chapter_screen and chapter_1_button.collidepoint(event.pos):
                chapter_screen = True
                chapter = 1  
    if moving and move_index < len(move_path):
        target = move_path[move_index]
        dx = target[0] - stop_image_rect.centerx
        dy = target[1] - stop_image_rect.centery
        dist = math.hypot(dx, dy)
        if dist < speed:
            stop_image_rect.center = target
            move_index += 1
        else:
            stop_image_rect.centerx += int(speed * dx / dist)
            stop_image_rect.centery += int(speed * dy / dist)
    elif moving and move_index >= len(move_path):
        moving = False
    #ショップの場所
    if shop_start:
        screen.fill(BROWN)
        pygame.draw.rect(screen, GRAY, buttons["return_4"])
        button_text = font_button.render("↺", True, WHITE)
        button_text_rect = button_text.get_rect(center=(buttons["return_4"].x + 25, buttons["return_4"].y + 25))
        screen.blit(button_text, button_text_rect)

        pygame.draw.rect(screen, GRAY, shop_buttons["shop_title"])
        screen.blit(kazi, (850, 0))
        button_text = font_title.render("＄海賊サテライトショップ＄", True, WHITE)
        button_text_rect = button_text.get_rect(center=(shop_buttons["shop_title"].x + 500, shop_buttons["shop_title"].y + 75))
        screen.blit(button_text, button_text_rect)

        pygame.draw.rect(screen, GRAY, shop_buttons["rozya_syouhin"])
        button_text = font_sentence_3.render("ゴールドロジャー", True, WHITE)
        button_text_rect = button_text.get_rect(center=(shop_buttons["rozya_syouhin"].x + 75, shop_buttons["rozya_syouhin"].y + 10))
        screen.blit(button_text, button_text_rect)
        button_text = font_sentence_3.render("無料", True, WHITE)
        button_text_rect = button_text.get_rect(center=(shop_buttons["rozya_syouhin"].x + 75, shop_buttons["rozya_syouhin"].y + 35))
        screen.blit(button_text, button_text_rect)
        
        pygame.draw.rect(screen, GRAY, shop_buttons["Rocks_syouhin"])
        button_text = font_sentence_3.render("ロックス・D・ジーベック", True, WHITE)
        button_text_rect = button_text.get_rect(center=(shop_buttons["Rocks_syouhin"].x + 170 / 2, shop_buttons["Rocks_syouhin"].y + 10))
        screen.blit(button_text, button_text_rect)
        button_text = font_sentence_3.render("無料", True, WHITE)
        button_text_rect = button_text.get_rect(center=(shop_buttons["Rocks_syouhin"].x + 170 / 2, shop_buttons["Rocks_syouhin"].y + 35))
        screen.blit(button_text, button_text_rect)

        screen.blit(ikari, (-100, 245))
        screen.blit(rozya_stop_image, (50, 180))
        screen.blit(Rocks_image, (240, 176))
        
    elif event.type == pygame.MOUSEBUTTONDOWN:
        if buttons["shop_button"].collidepoint(event.pos):
            shop_start = True






        


        
    #目次画面
    elif game_started:
        screen.fill(BLACK)
        pygame.draw.rect(screen, GRAY, buttons["return_4"])
        button_text = font_button.render("↺", True, WHITE)
        button_text_rect = button_text.get_rect(center=(buttons["return_4"].x + 25, buttons["return_4"].y + 25))
        screen.blit(button_text, button_text_rect)

        if chapter_screen:
            pygame.draw.line(screen, (255, 255, 255), (850, 150), (770, 150), 5)
            pygame.draw.line(screen, (255, 255, 255), (770, 150), (770, 200), 5)
            pygame.draw.line(screen, (255, 255, 255), (720, 250), (615 + 25, 250), 5)
            pygame.draw.line(screen, (255, 255, 255), (615 + 25, 250), (615 + 25, 300), 5)
            
            
            pygame.draw.rect(screen, GRAY, buttons["chapter_1"])
            button_text = font_sentence_1.render("大海賊時代", True, WHITE)
            button_text_rect = button_text.get_rect(center=(buttons["chapter_1"].x + 50, buttons["chapter_1"].y + 50))
            screen.blit(button_text, button_text_rect)
            
            pygame.draw.rect(screen, GRAY, buttons["chapter_2"])
            button_text = font_sentence_2.render("クイズ", True, WHITE)
            button_text_rect = button_text.get_rect(center=(buttons["chapter_2"].x + 25, buttons["chapter_2"].y + 25))
            screen.blit(button_text, button_text_rect)
            
            pygame.draw.rect(screen, GRAY, buttons["chapter_3"])
            button_text = font_sentence_2.render("海賊王に俺はなる", True, WHITE)
            button_text_rect = button_text.get_rect(center=(buttons["chapter_3"].x + 50, buttons["chapter_3"].y + 50))
            screen.blit(button_text, button_text_rect)

            pygame.draw.rect(screen, GRAY, buttons["chapter_4"])

            pygame.draw.rect(screen, GRAY, buttons["chapter_5"])

            

            screen.blit(stop_image, stop_image_rect)
            

            


        else:

            start_text = font_title.render("目次", True, WHITE)
            screen.blit(start_text, (0, 50))
            
            pygame.draw.rect(screen, GRAY, chapter_1_button)
            button_text = font_button.render("1章 東の海", True, WHITE)
            button_text_rect = button_text.get_rect(center=(chapter_1_button.x + 100, chapter_1_button.y + 25))
            screen.blit(button_text, button_text_rect)

    else:
        screen.fill(WHITE)

        title_surface = font_title.render("ONE PIECE", True, BLACK)
        screen.blit(title_surface, (100, 50))

        pygame.draw.rect(screen, GRAY, start_button)
        button_text = font_button.render("スタート", True, WHITE)
        button_text_rect = button_text.get_rect(center=(start_button.x +100, start_button.y + 25))
        screen.blit(button_text, button_text_rect)

        pygame.draw.rect(screen, GRAY, save_button)
        button_text = font_button.render("セーブ", True, WHITE)
        button_text_rect = button_text.get_rect(center=(save_button.x +100, save_button.y + 25))
        screen.blit(button_text, button_text_rect)

        pygame.draw.rect(screen, GRAY, load_button)
        button_text = font_button.render("ロード", True, WHITE)
        button_text_rect = button_text.get_rect(center=(load_button.x +100, load_button.y + 25))
        screen.blit(button_text, button_text_rect)

        pygame.draw.rect(screen, GRAY, buttons["shop_button"])
        button_text = font_button.render("ショップ", True, WHITE)
        button_text_rect = button_text.get_rect(center=(buttons["shop_button"].x + 100, buttons["shop_button"].y + 25))
        screen.blit(button_text, button_text_rect)
    

        if image:
            screen.blit(image, (550, 100))

    pygame.display.flip()
