import pygame
import os
import math

from pygame import mixer
pygame.font.init()

score_font = pygame.font.Font(None, 36)
combo_font = pygame.font.Font(None, 48)

mixer.init()

hitsound_great = mixer.Sound('Great.mp3')
hitsound_great.set_volume(0.5)

hitsound_perfect = mixer.Sound('perfect.mp3')
hitsound_perfect.set_volume(0.5)

combo_break = mixer.Sound('combobreak.mp3')
combo_break.set_volume(0.6)

pygame.init()
WIDTH, HEIGHT = 720, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))

center_x = WIDTH // 2
center_y = HEIGHT // 2

speed = 10
timing = 1

miss = 0
great = 0
perfect = 0
combo = 0
sum = 1

class judgementLine:
    def __init__(self, start, end, color1, color2, positionNumber):
        self.start = start
        self.end = end
        self.color1 = color1
        self.color2 = color2
        self.positionNumber = positionNumber

        self.hit = False
        self.hitTime = 0

class judgement(pygame.sprite.Sprite):
    def __init__(self, positionNumber, type):
        super().__init__()
        self.positionNumber = positionNumber
        self.type = type

        if type == 1 :
            self.image = pygame.image.load(os.path.join("assets", "great.png")).convert_alpha()
        elif type == 2:
            self.image = pygame.image.load(os.path.join("assets", "perfect.png")).convert_alpha()
        else:
            self.image = pygame.image.load(os.path.join("assets", "miss.png")).convert_alpha()

        angle = math.radians(22.5 + self.positionNumber * 45)

        self.image = pygame.transform.scale(self.image, (100, 50))
        self.image = pygame.transform.rotate(self.image, angle)

        self.hitTime = pygame.time.get_ticks()
        
        self.x = center_x + 100 * math.cos(angle)
        self.y = center_y + 100 * math.sin(angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def update(self):
        if pygame.time.get_ticks() - self.hitTime >= 500:
            self.kill()


def judge(ya):
    ya.hitTime = pygame.time.get_ticks()

class player(pygame.sprite.Sprite):
    def __init__(self, x, y, size_x, size_y):
        super().__init__()
        self.image = pygame.image.load(os.path.join("assets", "LED.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

class entity(pygame.sprite.Sprite):
    def __init__(self,size_x, size_y, positionNumber,type):
        super().__init__()
        self.image = pygame.image.load(os.path.join("assets", "Entity.webp")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (size_x, size_y))
        self.positionNumber = positionNumber
        self.size_x = size_x
        self.size_y = size_y
        self.type = type
        angle = math.radians(22.5 + self.positionNumber * 45)
        self.x = center_x + 960 * math.cos(angle)
        self.y = center_y + 960 * math.sin(angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.judge = 0
        

    def update(self):
        # Update the entity's position or behavior here
        angle = math.radians(22.5 + self.positionNumber * 45)
        speedx = -math.cos(angle) * speed
        speedy = -math.sin(angle) * speed

        self.x += speedx
        self.y += speedy

        self.rect.center = (round(self.x), round(self.y))

        dx = self.rect.centerx + 2 - center_x
        dy = self.rect.centery + 2 - center_y

        distance = math.sqrt(dx * dx + dy * dy)

        if distance <= area_radius - 80:
            self.judge = -1
        elif distance <= area_radius - 45:
            self.judge = 1
        elif distance <= area_radius + 60:
            self.judge = 2
            # uncomment to auto
            if distance <= area_radius + 10:
                auto(self)
        elif distance <= area_radius + 80:
            self.judge = 3       

class area:
    def __init__(self, center, pos1, pos2, color1, color2):
        self.center = center
        self.pos1 = pos1
        self.pos2 = pos2
        self.color1 = color1
        self.color2 = color2

        self.hit = False
        self.hitTime = 0

def hitArea(ye):
    ye.hit = True
    ye.hitTime = pygame.time.get_ticks()

# angle positions
position = []

for i in range(8):
    angle = math.radians(i * 45)
    x = center_x + 120 * math.cos(angle)
    y = center_y + 120 * math.sin(angle)
    position.append((x, y))

# line judgment positions
Line = {}

for i in range(8):
    start = position[i]
    end = position[(i + 1) % 8]
    color1 = (125, 120, 120) if i % 2 == 0 else (120, 120, 125)
    color2 = (110, 100, 100) if i % 2 == 0 else (100, 100, 110)
    Line[i] = judgementLine(start, end, color1, color2, i)

# separator positions
Separator = {}

for i in range(8):
    start = position[i]

    dx = position[i][0] - center_x
    dy = position[i][1] - center_y

    end_x = position[i][0] + dx * 100
    end_y = position[i][1] + dy * 100

    end = (end_x, end_y)

    Separator[i + 1] = judgementLine(
        start,
        end,
        (120, 120, 120),
        (120, 120, 120),
        i + 1
    )

#area

areas = {}

for i in range(8):
    dx = position[i][0] - center_x
    dy = position[i][1] - center_y
    
    end_x = position[i][0] + dx * 100
    end_y = position[i][1] + dy * 100
    
    end1 = (end_x, end_y)

    dx = position[(i+1)%8][0] - center_x
    dy = position[(i+1)%8][1] - center_y
        
    end_x = position[(i+1)%8][0] + dx * 100
    end_y = position[(i+1)%8][1] + dy * 100

    end2 = (end_x, end_y)

    color1 = (40, 42, 40) if i % 2 == 0 else (40, 40, 42)
    color2 = (10, 15, 10) if i % 2 == 0 else (10, 10, 15)

    areas[i] = area((center_x, center_y), end1, end2, color1, color2)

# Background stuff lah
area_radius = 100
area_x = WIDTH // 2
area_y = HEIGHT // 2

playerX = center_x
playerY = center_y

LED = player(playerX, playerY, 80, 80)


player_sprites = pygame.sprite.Group()
player_sprites.add(LED)

entity_sprites = pygame.sprite.Group()

judgement_sprites = pygame.sprite.Group()

def auto(note):
    print("perfect")
    note.kill()
    hitsound_perfect.play()

def load(map):
    rects = []

    currentBPM = 121
    currentSplit = 4
    currentTime = 0

    f = open(map, 'r')
    data = f.readlines()

    for line in data:
        line = line.rstrip()

        if line.startswith("BPM"):
            currentBPM = float(line.split()[1])

        elif line.startswith("SPLIT"):
            currentSplit = float(line.split()[1])

        else:
            noteTime = 60000/currentBPM/currentSplit

            for x in range(len(line)):
                # hit only enemy
                if line[x] == '0':
                    rects.append((x , currentTime, 0))

            currentTime += noteTime
            
    return rects

def isInsideTriangle(point, triangle):
    px, py = point

    ax, ay = triangle.center
    bx, by = triangle.pos1
    cx, cy = triangle.pos2

    denominator = ((by - cy) * (ax - cx) +
                   (cx - bx) * (ay - cy))

    a = ((by - cy) * (px - cx) +
         (cx - bx) * (py - cy)) / denominator

    b = ((cy - ay) * (px - cx) +
         (ax - cx) * (py - cy)) / denominator

    c = 1 - a - b

    return 0 <= a <= 1 and 0 <= b <= 1 and 0 <= c <= 1

map_rect = load('wonder panda.txt')
    
mixer.music.load('wonder panda.mp3')
mixer.music.play()

map_index = 0
start_time = pygame.time.get_ticks()

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z or event.key == pygame.K_c:
                mousePos = pygame.mouse.get_pos()

                for i in range(8):
                    if isInsideTriangle(mousePos, areas[i]):
                        hitArea(areas[i])
                        hitArea(Line[i])

                        for note in entity_sprites:

                            if note.positionNumber == i:

                                if note.judge == 1:
                                    print("great (late)")
                                    great += 1
                                    note.kill()
                                    print("miss: ", miss, "great: ", great, "perfect: ", perfect)
                                    hitsound_great.play()
                                    combo += 1
                                    sum += 1

                                    judgements = judgement(i,1)

                                    judgement_sprites.add(judgements)

                                elif note.judge == 2:
                                    print("perfect")
                                    perfect += 1
                                    note.kill()
                                    print("miss: ", miss, "great: ", great, "perfect: ", perfect)
                                    hitsound_perfect.play()
                                    combo += 1
                                    sum += 1

                                    judgements = judgement(i,2)
                                    judgement_sprites.add(judgements)

                                elif note.judge == 3:
                                    print("great (early)")
                                    great += 1
                                    note.kill()
                                    print("miss: ", miss, "great: ", great, "perfect: ", perfect)
                                    hitsound_great.play()
                                    combo += 1
                                    sum += 1

                                    judgements = judgement(i,1)
                                    judgement_sprites.add(judgements)

                            break
                

    for note in entity_sprites:
        if note.judge == -1:
            print("miss")
            miss += 1
            note.kill()
            print("miss: ", miss, "great: ", great, "perfect: ", perfect)
            combo_break.play()
            combo = 0
            sum += 1

            judgements = judgement(note.positionNumber,0)
            judgement_sprites.add(judgements)

    screen.fill((225, 225, 250))

    for hit in areas.values():
        if hit.hit:
            pygame.draw.polygon(screen, hit.color2, (hit.center, hit.pos1, hit.pos2))

            if pygame.time.get_ticks() - hit.hitTime >= 50:
                hit.hit = False

        else:
            pygame.draw.polygon(screen, hit.color1, (hit.center, hit.pos1, hit.pos2))

    #pygame.draw.circle(screen, (255, 220, 230, 150), (area_x, area_y), area_radius)


    for separator in Separator.values():
        pygame.draw.line(screen, separator.color1, separator.start, separator.end, 3)

    for line in Line.values():
        if line.hit:
            pygame.draw.line(screen, line.color2, line.start, line.end, 5)

            if pygame.time.get_ticks() - line.hitTime >= 50:
                line.hit = False

        else:
            pygame.draw.line(screen, line.color1, line.start, line.end, 5)


    current_time = pygame.time.get_ticks() - start_time

    while map_index < len(map_rect):
        position, spawn_time, note_type = map_rect[map_index]

        if current_time < spawn_time:
            break

        entity_sprites.add(entity(80,80,position,note_type))

        map_index += 1

    acc = (perfect*3 + great*1) / (sum*3)

    score_text = score_font.render(f"Acc: {round(acc*100)}%", True, (20, 20, 20))
    screen.blit(score_text, (550, 50))

    combo_text = combo_font.render(f"{combo} COMBO", True, (20, 20, 20))
    screen.blit(combo_text, (center_x - combo_text.get_width() // 2, 50))

    judgement_sprites.update()
    judgement_sprites.draw(screen)

    player_sprites.update()
    player_sprites.draw(screen)


    entity_sprites.update()
    entity_sprites.draw(screen)

    pygame.display.update()
    
    clock.tick(60)


import pygame
import os
import math

from pygame import mixer
pygame.font.init()

score_font = pygame.font.Font(None, 36)
combo_font = pygame.font.Font(None, 48)

mixer.init()

hitsound_great = mixer.Sound('Great.mp3')
hitsound_great.set_volume(0.5)

hitsound_perfect = mixer.Sound('perfect.mp3')
hitsound_perfect.set_volume(0.5)

combo_break = mixer.Sound('combobreak.mp3')
combo_break.set_volume(0.6)

pygame.init()
WIDTH, HEIGHT = 720, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))

center_x = WIDTH // 2
center_y = HEIGHT // 2

speed = 10
timing = 1

miss = 0
great = 0
perfect = 0
combo = 0
sum = 1

class judgementLine:
    def __init__(self, start, end, color1, color2, positionNumber):
        self.start = start
        self.end = end
        self.color1 = color1
        self.color2 = color2
        self.positionNumber = positionNumber

        self.hit = False
        self.hitTime = 0

class judgement(pygame.sprite.Sprite):
    def __init__(self, positionNumber, type):
        super().__init__()
        self.positionNumber = positionNumber
        self.type = type

        if type == 1 :
            self.image = pygame.image.load(os.path.join("assets", "great.png")).convert_alpha()
        elif type == 2:
            self.image = pygame.image.load(os.path.join("assets", "perfect.png")).convert_alpha()
        else:
            self.image = pygame.image.load(os.path.join("assets", "miss.png")).convert_alpha()

        angle = math.radians(22.5 + self.positionNumber * 45)

        self.image = pygame.transform.scale(self.image, (100, 50))
        self.image = pygame.transform.rotate(self.image, angle)

        self.hitTime = pygame.time.get_ticks()
        
        self.x = center_x + 100 * math.cos(angle)
        self.y = center_y + 100 * math.sin(angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def update(self):
        if pygame.time.get_ticks() - self.hitTime >= 500:
            self.kill()


def judge(ya):
    ya.hitTime = pygame.time.get_ticks()

class player(pygame.sprite.Sprite):
    def __init__(self, x, y, size_x, size_y):
        super().__init__()
        self.image = pygame.image.load(os.path.join("assets", "LED.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

class entity(pygame.sprite.Sprite):
    def __init__(self,size_x, size_y, positionNumber,type):
        super().__init__()
        self.image = pygame.image.load(os.path.join("assets", "Entity.webp")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (size_x, size_y))
        self.positionNumber = positionNumber
        self.size_x = size_x
        self.size_y = size_y
        self.type = type
        angle = math.radians(22.5 + self.positionNumber * 45)
        self.x = center_x + 960 * math.cos(angle)
        self.y = center_y + 960 * math.sin(angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.judge = 0
        

    def update(self):
        # Update the entity's position or behavior here
        angle = math.radians(22.5 + self.positionNumber * 45)
        speedx = -math.cos(angle) * speed
        speedy = -math.sin(angle) * speed

        self.x += speedx
        self.y += speedy

        self.rect.center = (round(self.x), round(self.y))

        dx = self.rect.centerx + 2 - center_x
        dy = self.rect.centery + 2 - center_y

        distance = math.sqrt(dx * dx + dy * dy)

        if distance <= area_radius - 80:
            self.judge = -1
        elif distance <= area_radius - 45:
            self.judge = 1
        elif distance <= area_radius + 60:
            self.judge = 2
            # uncomment to auto
            #if distance <= area_radius + 10:
            #    auto(self)
        elif distance <= area_radius + 80:
            self.judge = 3       

class area:
    def __init__(self, center, pos1, pos2, color1, color2):
        self.center = center
        self.pos1 = pos1
        self.pos2 = pos2
        self.color1 = color1
        self.color2 = color2

        self.hit = False
        self.hitTime = 0

def hitArea(ye):
    ye.hit = True
    ye.hitTime = pygame.time.get_ticks()

# angle positions
position = []

for i in range(8):
    angle = math.radians(i * 45)
    x = center_x + 120 * math.cos(angle)
    y = center_y + 120 * math.sin(angle)
    position.append((x, y))

# line judgment positions
Line = {}

for i in range(8):
    start = position[i]
    end = position[(i + 1) % 8]
    color1 = (125, 120, 120) if i % 2 == 0 else (120, 120, 125)
    color2 = (110, 100, 100) if i % 2 == 0 else (100, 100, 110)
    Line[i] = judgementLine(start, end, color1, color2, i)

# separator positions
Separator = {}

for i in range(8):
    start = position[i]

    dx = position[i][0] - center_x
    dy = position[i][1] - center_y

    end_x = position[i][0] + dx * 100
    end_y = position[i][1] + dy * 100

    end = (end_x, end_y)

    Separator[i + 1] = judgementLine(
        start,
        end,
        (120, 120, 120),
        (120, 120, 120),
        i + 1
    )

#area

areas = {}

for i in range(8):
    dx = position[i][0] - center_x
    dy = position[i][1] - center_y
    
    end_x = position[i][0] + dx * 100
    end_y = position[i][1] + dy * 100
    
    end1 = (end_x, end_y)

    dx = position[(i+1)%8][0] - center_x
    dy = position[(i+1)%8][1] - center_y
        
    end_x = position[(i+1)%8][0] + dx * 100
    end_y = position[(i+1)%8][1] + dy * 100

    end2 = (end_x, end_y)

    color1 = (40, 42, 40) if i % 2 == 0 else (40, 40, 42)
    color2 = (10, 15, 10) if i % 2 == 0 else (10, 10, 15)

    areas[i] = area((center_x, center_y), end1, end2, color1, color2)

# Background stuff lah
area_radius = 100
area_x = WIDTH // 2
area_y = HEIGHT // 2

playerX = center_x
playerY = center_y

LED = player(playerX, playerY, 80, 80)


player_sprites = pygame.sprite.Group()
player_sprites.add(LED)

entity_sprites = pygame.sprite.Group()

judgement_sprites = pygame.sprite.Group()

def auto(note):
    print("perfect")
    note.kill()
    hitsound_perfect.play()

def load(map):
    rects = []

    currentBPM = 121
    currentSplit = 4
    currentTime = 0

    f = open(map, 'r')
    data = f.readlines()

    for line in data:
        line = line.rstrip()

        if line.startswith("BPM"):
            currentBPM = float(line.split()[1])

        elif line.startswith("SPLIT"):
            currentSplit = float(line.split()[1])

        else:
            noteTime = 60000/currentBPM/currentSplit

            for x in range(len(line)):
                # hit only enemy
                if line[x] == '0':
                    rects.append((x , currentTime, 0))

            currentTime += noteTime
            
    return rects

def isInsideTriangle(point, triangle):
    px, py = point

    ax, ay = triangle.center
    bx, by = triangle.pos1
    cx, cy = triangle.pos2

    denominator = ((by - cy) * (ax - cx) +
                   (cx - bx) * (ay - cy))

    a = ((by - cy) * (px - cx) +
         (cx - bx) * (py - cy)) / denominator

    b = ((cy - ay) * (px - cx) +
         (ax - cx) * (py - cy)) / denominator

    c = 1 - a - b

    return 0 <= a <= 1 and 0 <= b <= 1 and 0 <= c <= 1

map_rect = load('wonder panda.txt')
    
mixer.music.load('wonder panda.mp3')
mixer.music.play()

map_index = 0
start_time = pygame.time.get_ticks()

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z or event.key == pygame.K_c:
                mousePos = pygame.mouse.get_pos()

                for i in range(8):
                    if isInsideTriangle(mousePos, areas[i]):
                        hitArea(areas[i])
                        hitArea(Line[i])

                        for note in entity_sprites:

                            if note.positionNumber == i:

                                if note.judge == 1:
                                    print("great (late)")
                                    great += 1
                                    note.kill()
                                    print("miss: ", miss, "great: ", great, "perfect: ", perfect)
                                    hitsound_great.play()
                                    combo += 1
                                    sum += 1

                                    judgements = judgement(i,1)

                                    judgement_sprites.add(judgements)

                                elif note.judge == 2:
                                    print("perfect")
                                    perfect += 1
                                    note.kill()
                                    print("miss: ", miss, "great: ", great, "perfect: ", perfect)
                                    hitsound_perfect.play()
                                    combo += 1
                                    sum += 1

                                    judgements = judgement(i,2)
                                    judgement_sprites.add(judgements)

                                elif note.judge == 3:
                                    print("great (early)")
                                    great += 1
                                    note.kill()
                                    print("miss: ", miss, "great: ", great, "perfect: ", perfect)
                                    hitsound_great.play()
                                    combo += 1
                                    sum += 1

                                    judgements = judgement(i,1)
                                    judgement_sprites.add(judgements)

                            break
                

    for note in entity_sprites:
        if note.judge == -1:
            print("miss")
            miss += 1
            note.kill()
            print("miss: ", miss, "great: ", great, "perfect: ", perfect)
            combo_break.play()
            combo = 0
            sum += 1

            judgements = judgement(note.positionNumber,0)
            judgement_sprites.add(judgements)

    screen.fill((225, 225, 250))

    for hit in areas.values():
        if hit.hit:
            pygame.draw.polygon(screen, hit.color2, (hit.center, hit.pos1, hit.pos2))

            if pygame.time.get_ticks() - hit.hitTime >= 50:
                hit.hit = False

        else:
            pygame.draw.polygon(screen, hit.color1, (hit.center, hit.pos1, hit.pos2))

    #pygame.draw.circle(screen, (255, 220, 230, 150), (area_x, area_y), area_radius)


    for separator in Separator.values():
        pygame.draw.line(screen, separator.color1, separator.start, separator.end, 3)

    for line in Line.values():
        if line.hit:
            pygame.draw.line(screen, line.color2, line.start, line.end, 5)

            if pygame.time.get_ticks() - line.hitTime >= 50:
                line.hit = False

        else:
            pygame.draw.line(screen, line.color1, line.start, line.end, 5)


    current_time = pygame.time.get_ticks() - start_time

    while map_index < len(map_rect):
        position, spawn_time, note_type = map_rect[map_index]

        if current_time < spawn_time:
            break

        entity_sprites.add(entity(80,80,position,note_type))

        map_index += 1

    acc = (perfect*3 + great*1) / (sum*3)

    score_text = score_font.render(f"Acc: {round(acc*100)}%", True, (20, 20, 20))
    screen.blit(score_text, (550, 50))

    combo_text = combo_font.render(f"{combo} COMBO", True, (20, 20, 20))
    screen.blit(combo_text, (center_x - combo_text.get_width() // 2, 50))

    judgement_sprites.update()
    judgement_sprites.draw(screen)

    player_sprites.update()
    player_sprites.draw(screen)


    entity_sprites.update()
    entity_sprites.draw(screen)

    pygame.display.update()
    
    clock.tick(60)

pygame.quit()