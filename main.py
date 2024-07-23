import pygame
import random
#  TODO: MULTIPLE TARGETS(MAYBE) + HEARTS(MAYBE) + SHOOT ANIMATION(MAYBE) + ANIMATED LOGO(MAYBE)
pygame.init()

pygame.display.set_caption('Slice Strike')
screen = pygame.display.set_mode((1200, 800))
bg = pygame.image.load("bg_pizza1.xcf").convert()
pygame.mixer.music.load("bgm.mp3")
pygame.mixer.music.set_volume(.5)
ricochet1 = pygame.mixer.Sound("ricochet.mp3")
ricochet2 = pygame.mixer.Sound("ricochet1.mp3")
ricochet3 = pygame.mixer.Sound("ricochet2.mp3")
mamma_mia = pygame.mixer.Sound("mamma_mia.mp3")
special_hit = pygame.mixer.Sound("special_hit.mp3")
button_sound = pygame.mixer.Sound("button_sound.mp3")
level_up_sound = pygame.mixer.Sound("level_up_sound.mp3")
is_muted_music = False
is_muted_sounds = False
madman = False


cursor_img = pygame.transform.scale(pygame.image.load("crosshair1.png").convert_alpha(), (50, 50))
cursor_img_rect = cursor_img.get_rect()
pygame.mouse.set_visible(False)
normal_target = pygame.transform.scale(pygame.image.load("pizza1.png").convert_alpha(), (80, 80))
normal_target.set_colorkey((255, 255, 255))
special_target = pygame.transform.scale(pygame.image.load("badpizza1.png").convert_alpha(), (80, 80))
special_target.set_colorkey((255, 255, 255))
warning_sign = pygame.transform.scale(pygame.image.load("warning1.png").convert_alpha(), (50, 50))

clock = pygame.time.Clock()
initial_time = pygame.time.get_ticks()
menu_font = pygame.font.Font("pixelfont.ttf", 24)
enter_name_font = pygame.font.Font("pixelfont.ttf", 36)
little_font = pygame.font.Font("pixelfont.ttf", 12)
special_factor = 5


def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, 1, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)


def draw_esc(esc="<esc"):
    esc_box = pygame.transform.scale(pygame.image.load("menu_button.jpeg").convert_alpha(), (100, 50))
    screen.blit(esc_box, (0, 0))
    draw_text(esc, little_font, (255, 255, 255), screen, 23, 18)
    esc_rect = esc_box.get_rect()
    esc_rect.x = 20
    esc_rect.y = 18
    return esc_rect


player_name = ""


class Target:
    def __init__(self):
        self.is_special = False
        self.x = 0
        self.y = 0
        self.speed = 0
        self.speed_factor = random.randint(3, 6)
        self.deviation = random.random()
        self.points = 0


def generate_target(level):
    new_target = Target()
    new_target.x = random.randint(5, screen.get_width() - 90)
    new_target.y = -200
    if random.random() < 1/special_factor:
        new_target.is_special = True
        new_target.speed = (1 + level / 10) * special_factor
        new_target.points = level * special_factor
    else:
        new_target.is_special = False
        new_target.speed = 1 + level / 10
        new_target.points = level
    return new_target


def update_targets(target, level, shot, is_madman):  # 540
    target.y += target.speed * target.speed_factor
    if target.x > 0:
        target.x += target.deviation * level
    else:
        target.x += 1
    if target.is_special:
        target.speed = (1 + level / 8) * special_factor
        target.points = level * special_factor
    else:
        target.speed = 1 + level / 8
        target.points = level
    if (target.x < 0 and target.deviation < 0) or target.x > screen.get_width() - 80:
        target.deviation = target.deviation * (-1)
    if is_madman:
        if target.y > 540 or (target.y < 0 and target.speed_factor < 0):
            target.speed_factor = target.speed_factor * (-1)
        if shot:
            target.speed_factor = random.randint(3, 6)
            if random.random() < 1 / special_factor:
                target.is_special = True
                target.y = -125 * level
            else:
                target.is_special = False
                target.y = -200
    else:
        if target.y >= 800 or shot:
            target.x = random.randint(5, screen.get_width() - 90)
            if random.random() < 1/special_factor:
                target.is_special = True
                target.y = -125 * level
            else:
                target.is_special = False
                target.y = -200


def draw_target(target):
    if target.is_special:
        screen.blit(special_target, (target.x, target.y))
    else:
        screen.blit(normal_target, (target.x, target.y))


def middle(n):
    return n[1]


def update_high_scores(name, score, combo):
    file = open("high_scores.txt", "r")
    players_number = 1
    players = [(name, score, combo)]
    players_number += int(file.readline())
    for i in range(players_number - 1):
        players.append((file.readline()[:-1], int(file.readline()), int(file.readline())))
    players.sort(key=middle, reverse=True)
    file.close()
    file = open("high_scores.txt", "w")
    if players_number > 10:
        players_number = 10
    file.write(str(players_number) + '\n')
    if players_number < 10:
        cap = players_number
    else:
        cap = 10
    for i in range(cap):
        file.write(players[i][0] + '\n')
        file.write(str(players[i][1]) + '\n')
        file.write(str(players[i][2]) + '\n')
    file.close()


def display_high_scores():
    big_box = pygame.transform.scale(pygame.image.load("high_scores_box.png").convert_alpha(), (1000, 725))
    screen.blit(big_box, (120, 40))
    draw_text("HIGH SCORES:", enter_name_font, (255, 255, 255), screen, 400, 100)
    draw_text("(TOP 10)", little_font, (150, 150, 150), screen, 850, 130)
    pygame.draw.line(screen, (255, 255, 255), (380, 140), (830, 140))
    draw_text("PLAYER:", little_font, (255, 255, 255), screen, 270, 190)
    draw_text("SCORE:", little_font, (255, 255, 255), screen, 570, 190)
    draw_text("MAX COMBO:", little_font, (255, 255, 255), screen, 870, 190)
    pygame.draw.line(screen, (255, 255, 255), (200, 210), (1030, 210))
    file = open("high_scores.txt", "r")
    number_of_players = int(file.readline())
    for i in range(number_of_players):
        draw_text(str(i + 1) + ".", little_font, (255, 255, 255), screen, 200, 235 + i * 50)
        draw_text(file.readline()[:-1], little_font, (255, 255, 255), screen, 270, 235 + i * 50)
        draw_text(str(file.readline())[:-1], little_font, (255, 255, 255), screen, 570, 235 + i * 50)
        draw_text(str(file.readline())[:-1], little_font, (255, 255, 255), screen, 870, 235 + i * 50)


def reset_high_scores():
    file = open("high_scores.txt", "w+")
    file.write(str(0))


def main_menu():
    running = True
    global player_name
    if not is_muted_music:
        pygame.mixer.music.play(-1)
    while running:
        player_name = ""
        ship_top = screen.get_height() - bg.get_height()
        ship_left = screen.get_width() / 2 - bg.get_width() / 2
        screen.blit(bg, (ship_left, ship_top))

        esc_rect = draw_esc()

        menu_icon = pygame.transform.scale(pygame.image.load("logo.png").convert_alpha(), (600, 400))  # to replace
        screen.blit(menu_icon, (300, 20))

        play_icon = pygame.transform.scale(pygame.image.load("menu_button.jpeg").convert_alpha(), (200, 100))
        screen.blit(play_icon, (500, 300))
        draw_text("PLAY", menu_font, (255, 255, 255), screen, 550, 340)
        draw_text("(enter)", little_font, (100, 100, 100), screen, 700, 350)
        high_scores_icon = pygame.transform.scale(pygame.image.load("menu_button.jpeg").convert_alpha(), (400, 100))
        screen.blit(high_scores_icon, (400, 450))
        draw_text("HIGH SCORES", menu_font, (255, 255, 255), screen, 470, 490)
        options_icon = pygame.transform.scale(pygame.image.load("menu_button.jpeg").convert_alpha(), (250, 100))
        screen.blit(options_icon, (475, 600))
        draw_text("OPTIONS", menu_font, (255, 255, 255), screen, 520, 640)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    button_sound.play()
                    running = False
                elif event.key == pygame.K_RETURN:
                    button_sound.play()
                    play()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                play_rect = pygame.Rect(500, 300, 200, 100)
                options_rect = pygame.Rect(500, 600, 200, 100)
                high_scores_rect = pygame.Rect(500, 450, 200, 100)
                if play_rect.collidepoint((mx, my)):
                    button_sound.play()
                    play()
                elif options_rect.collidepoint((mx, my)):
                    button_sound.play()
                    options()
                elif high_scores_rect.collidepoint((mx, my)):
                    button_sound.play()
                    high_scores()
                elif esc_rect.collidepoint((mx, my)):
                    button_sound.play()
                    running = False

        cursor_img_rect.center = pygame.mouse.get_pos()
        screen.blit(cursor_img, cursor_img_rect)

        pygame.display.update()
        clock.tick(60)


def play():
    global player_name, initial_time
    enter_name()
    tutorial()

    targets = []
    targets_number = 0
    player_score = 0

    was_hit = False
    combo = 0
    biggest_combo = 0

    current_level = 1
    to_next_level = 10

    time_for_level = 20
    initial_time = pygame.time.get_ticks()
    game_over = False

    while not game_over:
        screen.fill((0, 0, 0))
        screen.blit(bg, (0, 0))
        if (targets_number < 6 and random.random() < 0.02) or targets_number == 0:
            targets.append(generate_target(current_level))
            targets_number += 1
            if targets[targets_number - 1].is_special:
                screen.blit(warning_sign, (targets[targets_number - 1].x, 0))

        for i in range(targets_number):
            draw_target(targets[i])

        esc_rect = draw_esc("quit")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    button_sound.play()
                    game_over = True
                elif event.key == pygame.K_p:
                    button_sound.play()
                    time_for_level += int(pause() / 1000)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                for i in range(targets_number):
                    if (((mx - (targets[i].x + 40)) ** 2 + (my - (targets[i].y + 40)) ** 2) ** .5) <= 40:  # and targets[i].x < 540
                        was_hit = True
                        if targets[i].is_special and not is_muted_sounds:
                            special_hit.play()
                        else:
                            if random.random() < 0.5 and not is_muted_sounds:
                                ricochet1.play()
                            elif not is_muted_sounds:
                                ricochet2.play()
                        if combo % 10 == 0 and combo != 0 and not is_muted_sounds:
                            mamma_mia.play()
                        player_score += targets[i].points
                        to_next_level -= targets[i].points
                        update_targets(targets[i], current_level, True, madman)
                if was_hit:
                    combo += 1
                else:
                    combo = 0
                was_hit = False
                if esc_rect.collidepoint((mx, my)):
                    button_sound.play()
                    game_over = True
        if biggest_combo < combo:
            biggest_combo = combo

        if to_next_level <= 0:
            level_up_sound.play()
            current_level += 1
            time_for_level = 20
            to_next_level = 10 + current_level ** 2
            initial_time = pygame.time.get_ticks()

        passed_time = (pygame.time.get_ticks() - initial_time) // 1000
        time_left = time_for_level - passed_time

        if time_left <= 0:
            game_over = True

        for i in range(targets_number):
            update_targets(targets[i], current_level, False, madman)
            if targets[i].is_special:
                screen.blit(warning_sign, (targets[i].x, 0))

        stats_box = pygame.transform.scale(pygame.image.load("stats_box.png").convert_alpha(), (1200, 200))
        screen.blit(stats_box, (0, 620))
        cursor_img_rect.center = pygame.mouse.get_pos()
        screen.blit(cursor_img, cursor_img_rect)

        draw_text("TIME LEFT:", menu_font, (255, 255, 255), screen, 750, 675)
        draw_text(str(time_left), menu_font, (255, 255, 255), screen, 1000, 675)

        draw_text("LVL ", enter_name_font, (255, 255, 255), screen, 500, 700)
        draw_text(str(current_level), enter_name_font, (255, 255, 255), screen, 650, 700)

        draw_text("SCORE:", menu_font, (255, 255, 255), screen, 150, 675)
        draw_text(str(player_score), menu_font, (255, 255, 255), screen, 300, 675)

        draw_text("TO NEXT:", menu_font, (255, 255, 255), screen, 150, 735)
        draw_text(str(to_next_level), menu_font, (255, 255, 255), screen, 350, 735)

        draw_text("COMBO:", menu_font, (255, 255, 255), screen, 850, 735)
        draw_text(str(combo), menu_font, (255, 255, 255), screen, 1000, 735)

        pygame.display.update()
        clock.tick(60)
    if not madman:
        update_high_scores(player_name, player_score, biggest_combo)

    game_over_screen(player_name, player_score, biggest_combo, madman)


def enter_name():
    running = True
    global player_name
    while running:

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.unicode.isalnum() and len(player_name) < 9:
                    player_name += event.unicode
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                elif event.key == pygame.K_RETURN and len(player_name) > 2:
                    button_sound.play()
                    running = False
            elif event.type == pygame.QUIT:
                main_menu()

        screen.fill((0, 0, 0))
        screen.blit(bg, (0, 0))
        enter_name_box = pygame.transform.scale(pygame.image.load("stats_box.png").convert_alpha(), (600, 150))
        screen.blit(enter_name_box, (300, 150))
        draw_text("ENTER NAME:", enter_name_font, (255, 255, 255), screen, 410, 190)
        draw_text("between 3-9 alphanumerical characters", little_font, (255, 255, 255), screen, 365, 245)
        name_box = pygame.transform.scale(pygame.image.load("menu_button.jpeg").convert_alpha(), (300, 100))
        screen.blit(name_box, (450, 350))
        block = menu_font.render(player_name, True, (255, 255, 255))
        rect = block.get_rect()
        rect.center = screen.get_rect().center
        screen.blit(block, rect)

        pygame.display.update()
        clock.tick(60)


def tutorial():
    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(bg, (0, 0))

        next_button = pygame.transform.scale(pygame.image.load("menu_button.jpeg").convert_alpha(), (200, 100))
        screen.blit(next_button, (1000, 700))
        draw_text("ENTER>", menu_font, (255, 255, 255), screen, 1035, 738)

        tutorial_icon = pygame.transform.scale(pygame.image.load("tutorial.png").convert_alpha(), (1000, 700))
        screen.blit(tutorial_icon, (100, 50))

        tutorial_box = pygame.transform.scale(pygame.image.load("menu_button.jpeg").convert_alpha(), (400, 100))
        screen.blit(tutorial_box, (400, 10))
        draw_text("TUTORIAL", menu_font, (255, 255, 255), screen, 510, 50)

        draw_text("TRY TO SHOOT AS MANY TARGETS AS YOU ", menu_font, (255, 255, 255), screen, 180, 500)
        draw_text("CAN BEFORE THE TIME RUNS OUT. ", menu_font, (255, 255, 255), screen, 180, 550)
        draw_text("GOOD LUCK!:) ", little_font, (255, 255, 255), screen, 880, 560)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    button_sound.play()
                    running = False

        pygame.display.update()
        clock.tick(60)


def options():
    global is_muted_music, is_muted_sounds, madman
    running = True
    checked = pygame.transform.scale(pygame.image.load("muted.png").convert_alpha(), (50, 50))
    unchecked = pygame.transform.scale(pygame.image.load("unmuted.png").convert_alpha(), (50, 50))
    if is_muted_music:
        music_image = checked
    else:
        music_image = unchecked
    if is_muted_sounds:
        sound_image = checked
    else:
        sound_image = unchecked
    if madman:
        madman_image = checked
    else:
        madman_image = unchecked
    music_image_rect = music_image.get_rect()
    sound_image_rect = sound_image.get_rect()
    madman_image_rect = madman_image.get_rect()
    music_image_rect.x = 650
    music_image_rect.y = 250
    sound_image_rect.x = 650
    sound_image_rect.y = 330
    madman_image_rect.x = 650
    madman_image_rect.y = 410

    while running:
        screen.fill((0, 0, 0))
        screen.blit(bg, (0, 0))
        esc_rect = draw_esc("back")

        options_box = pygame.transform.scale(pygame.image.load("high_scores_box.png").convert_alpha(), (700, 300))
        screen.blit(options_box, (250, 205))
        draw_text("MUSIC:", menu_font, (255, 255, 255), screen, 450, 255)
        draw_text("SOUND:", menu_font, (255, 255, 255), screen, 450, 340)
        draw_text("MADMAN:", menu_font, (255, 255, 255), screen, 450, 425)
        draw_text("(score will not be registered)", little_font, (155, 155, 155), screen, 400, 465)
        screen.blit(music_image, (650, 250))
        screen.blit(sound_image, (650, 330))
        screen.blit(madman_image, (650, 410))

        reset_hs_box = pygame.transform.scale(pygame.image.load("menu_button.jpeg").convert_alpha(), (550, 150))
        screen.blit(reset_hs_box, (325, 550))
        reset_hs_box_rect = reset_hs_box.get_rect()
        reset_hs_box_rect.x = 325
        reset_hs_box_rect.y = 550
        draw_text("RESET HIGHSCORES", menu_font, (255, 255, 255), screen, 410, 610)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if music_image_rect.collidepoint((mx, my)):
                    button_sound.play()
                    if music_image == unchecked:
                        music_image = checked
                        pygame.mixer.music.pause()
                        is_muted_music = True
                    else:
                        music_image = unchecked
                        pygame.mixer.music.play(-1)
                        is_muted_music = False
                elif sound_image_rect.collidepoint((mx, my)):
                    button_sound.play()
                    if sound_image == unchecked:
                        sound_image = checked
                        is_muted_sounds = True
                    else:
                        sound_image = unchecked
                        is_muted_sounds = False
                elif madman_image_rect.collidepoint((mx, my)):
                    button_sound.play()
                    if madman_image == unchecked:
                        madman_image = checked
                        madman = True
                    else:
                        madman_image = unchecked
                        madman = False
                elif reset_hs_box_rect.collidepoint((mx, my)):
                    button_sound.play()
                    reset_high_scores()
                elif esc_rect.collidepoint((mx, my)):
                    button_sound.play()
                    running = False

        cursor_img_rect.center = pygame.mouse.get_pos()
        screen.blit(cursor_img, cursor_img_rect)
        pygame.display.update()
        clock.tick(60)


def high_scores():
    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(bg, (0, 0))
        esc_rect = draw_esc("back")

        display_high_scores()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    button_sound.play()
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if esc_rect.collidepoint((mx, my)):
                    button_sound.play()
                    running = False

        cursor_img_rect.center = pygame.mouse.get_pos()
        screen.blit(cursor_img, cursor_img_rect)
        pygame.display.update()
        clock.tick(60)


def game_over_screen(name, score, combo, is_madman):
    running = True
    while running:
        screen.blit(bg, (0, 0))
        text_box = pygame.transform.scale(pygame.image.load("menu_button.jpeg").convert_alpha(), (475, 150))
        screen.blit(text_box, (350, 300))
        draw_text("GAME OVER", enter_name_font, (255, 0, 0), screen, 425, 350)
        draw_text("press enter", little_font, (175, 175, 175), screen, 515, 400)

        stats_box = pygame.transform.scale(pygame.image.load("menu_button.jpeg").convert_alpha(), (900, 100))
        screen.blit(stats_box, (150, 100))
        draw_text("PLAYER:", little_font, (255, 255, 255), screen, 275, 140)
        draw_text(name, little_font, (255, 255, 255), screen, 375, 140)
        draw_text("SCORE:", little_font, (255, 255, 255), screen, 525, 140)
        draw_text(str(score), little_font, (255, 255, 255), screen, 600, 140)
        draw_text("MAX COMBO:", little_font, (255, 255, 255), screen, 750, 140)
        draw_text(str(combo), little_font, (255, 255, 255), screen, 880, 140)
        if is_madman:
            draw_text("what a madman", little_font, (175, 175, 175), screen, 515, 450)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    button_sound.play()
                    running = False
        pygame.display.update()
        clock.tick(60)


def pause():
    running = True
    pause_time = pygame.time.get_ticks()
    pause_box = pygame.transform.scale(pygame.image.load("menu_button.jpeg").convert_alpha(), (475, 150))
    screen.blit(pause_box, (350, 300))
    draw_text("PAUSED", enter_name_font, (255, 255, 255), screen, 475, 350)
    draw_text("enter to unpause", little_font, (155, 155, 155), screen, 480, 400)
    pygame.display.update()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    button_sound.play()
                    running = False
    return pygame.time.get_ticks() - pause_time


main_menu()
pygame.quit()
