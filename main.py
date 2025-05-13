import pygame
import random
import math
import os
import webbrowser
import datetime

pygame.init()

WIDTH, HEIGHT = 256 * 3, 240 * 3
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Duck Hunt")
pygame.display.set_icon(pygame.image.load("images/icon.ico"))

# Load and scale intro image
intro_img = pygame.image.load("images/intro.png").convert()
intro_img = pygame.transform.scale(intro_img, (WIDTH, HEIGHT))

# Load and scale backgrounds
background = pygame.image.load("images/bg.png").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background2 = pygame.image.load("images/bg2.png").convert()
background2 = pygame.transform.scale(background2, (WIDTH, HEIGHT))

# Load bush image
bush_img = pygame.image.load("images/bush.png").convert_alpha()
bush_img = pygame.transform.scale(bush_img, (256 * 3, (189 - 146) * 3))  # Size: (768, 129)
bush_rect = bush_img.get_rect(topleft=(0, 146 * 3))

# Load pause image
pause_img = pygame.image.load("images/pause.png").convert_alpha()
pause_img = pygame.transform.scale(pause_img, (pause_img.get_width() * 3, pause_img.get_height() * 3))
pause_img_rect = pause_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))

# Load button hover images
start_hover_img = pygame.image.load("images/p_start.png").convert_alpha()
start_hover_img = pygame.transform.scale(start_hover_img, (start_hover_img.get_width() * 3, start_hover_img.get_height() * 3))
reset_hover_img = pygame.image.load("images/p_reset.png").convert_alpha()
reset_hover_img = pygame.transform.scale(reset_hover_img, (reset_hover_img.get_width() * 3, reset_hover_img.get_height() * 3))

# Load end-of-round animation images
partial_success_img = pygame.image.load("images/1_f.png").convert_alpha()
partial_success_img = pygame.transform.scale(partial_success_img, (partial_success_img.get_width() * 3, partial_success_img.get_height() * 3))
perfect_success_img = pygame.image.load("images/2_f.png").convert_alpha()
perfect_success_img = pygame.transform.scale(perfect_success_img, (perfect_success_img.get_width() * 3, perfect_success_img.get_height() * 3))

# Load cursor image stalking
cursor_img = pygame.image.load("images/aim.png").convert_alpha()
cursor_img = pygame.transform.scale(cursor_img, (cursor_img.get_width() * 3, cursor_img.get_height() * 3))
cursor_img_rect = cursor_img.get_rect()

# Define duck types
duck_types = [
    {
        'color': 'green',
        'spawn_prob': 0.60,
        'points': 100,
        'angle_frames': [
            pygame.transform.scale(pygame.image.load(f"images/a_{i}_g.png").convert_alpha(), (64 * 1.5, 64 * 1.5))
            for i in range(1, 4)
        ],
        'straight_frames': [
            pygame.transform.scale(pygame.image.load(f"images/s_{i}_g.png").convert_alpha(), (64 * 1.5, 64 * 1.5))
            for i in range(1, 4)
        ],
        'dead_img': pygame.transform.scale(pygame.image.load("images/d_g.png").convert_alpha(), (64 * 1.5, 64 * 1.5)),
        'fall_frames': [
            pygame.transform.scale(
                pygame.image.load(f"images/f_{i}_g.png").convert_alpha(),
                (int(pygame.image.load(f"images/f_{i}_g.png").get_width() * 3), int(pygame.image.load(f"images/f_{i}_g.png").get_height() * 3))
            )
            for i in range(1, 5)
        ]
    },
    {
        'color': 'red',
        'spawn_prob': 0.25,
        'points': 200,
        'angle_frames': [
            pygame.transform.scale(pygame.image.load(f"images/a_{i}_r.png").convert_alpha(), (64 * 1.5, 64 * 1.5))
            for i in range(1, 4)
        ],
        'straight_frames': [
            pygame.transform.scale(pygame.image.load(f"images/s_{i}_r.png").convert_alpha(), (64 * 1.5, 64 * 1.5))
            for i in range(1, 4)
        ],
        'dead_img': pygame.transform.scale(pygame.image.load("images/d_r.png").convert_alpha(), (64 * 1.5, 64 * 1.5)),
        'fall_frames': [
            pygame.transform.scale(
                pygame.image.load(f"images/f_{i}_r.png").convert_alpha(),
                (int(pygame.image.load(f"images/f_{i}_r.png").get_width() * 3), int(pygame.image.load(f"images/f_{i}_r.png").get_height() * 3))
            )
            for i in range(1, 5)
        ]
    },
    {
        'color': 'blue',
        'spawn_prob': 0.15,
        'points': 500,
        'angle_frames': [
            pygame.transform.scale(pygame.image.load(f"images/a_{i}_b.png").convert_alpha(), (64 * 1.5, 64 * 1.5))
            for i in range(1, 4)
        ],
        'straight_frames': [
            pygame.transform.scale(pygame.image.load(f"images/s_{i}_b.png").convert_alpha(), (64 * 1.5, 64 * 1.5))
            for i in range(1, 4)
        ],
        'dead_img': pygame.transform.scale(pygame.image.load("images/d_b.png").convert_alpha(), (64 * 1.5, 64 * 1.5)),
        'fall_frames': [
            pygame.transform.scale(
                pygame.image.load(f"images/f_{i}_b.png").convert_alpha(),
                (int(pygame.image.load(f"images/f_{i}_b.png").get_width() * 3), int(pygame.image.load(f"images/f_{i}_b.png").get_height() * 3))
            )
            for i in range(1, 5)
        ]
    }
]

# Create mirrored frames for each duck type
for duck_type in duck_types:
    duck_type['angle_frames_mirrored'] = [pygame.transform.flip(frame, True, False) for frame in duck_type['angle_frames']]
    duck_type['straight_frames_mirrored'] = [pygame.transform.flip(frame, True, False) for frame in duck_type['straight_frames']]

# Load pass and fail duck images
pass_duck_img = pygame.image.load("images/pass_duck.png").convert_alpha()
pass_duck_img = pygame.transform.scale(pass_duck_img, (pass_duck_img.get_width() * 3, pass_duck_img.get_height() * 3))
fail_duck_img = pygame.image.load("images/fail_duck.png").convert_alpha()
fail_duck_img = pygame.transform.scale(fail_duck_img, (fail_duck_img.get_width() * 3, fail_duck_img.get_height() * 3))

# Load sounds
shot_sound = pygame.mixer.Sound("sound/shot.wav")
duck_sound = pygame.mixer.Sound("sound/duck.wav")
next_round_sound = pygame.mixer.Sound("sound/round.wav")
click_sound = pygame.mixer.Sound("sound/click.wav")
lose_sound = pygame.mixer.Sound("sound/lose.wav")
bush_sound = pygame.mixer.Sound("sound/bush.wav")
empty_sound = pygame.mixer.Sound("sound/empty.wav")
reload_sound = pygame.mixer.Sound("sound/reload.wav")
day_sound = pygame.mixer.Sound("sound/day.wav")
night_sound = pygame.mixer.Sound("sound/night.wav")
day_sound.set_volume(0.5)
night_sound.set_volume(0.5)

# Load font
score_font = pygame.font.Font("font/font.otf", 8 * 3)
round_font = pygame.font.Font("font/font.otf", 7 * 3)
credit_font = pygame.font.Font("font/font.otf", 21)
plus_100_font = pygame.font.Font("font/font.otf", 5 * 3)

# Scores
score = 0
try:
    with open("data.dat", "r") as f:
        high_score = int(f.read())
except:
    high_score = 0

# Game state
rectangles = []
birds = []
dead_ducks = []
falling_ducks = []
plus_100_texts = []
animation_speed = 0.1
spawn_timer = 0
spawn_interval = 2000
round_num = 1
game_started = False
paused = False
round_end_timer = 0
round_end_duration = 6.5
round_end_animation = None
reload_timer = 0
is_reloading = False
reload_duration = 1.7  # 1.7 seconds for reload
current_sound = None
duck_fall_complete = False  # NEW: Flag to track if duck has fallen into bush

# Duck positions and tracking
duck_positions = [(x * 3, 210 * 3) for x in [96, 104, 112, 120, 128, 136, 144, 152, 160, 168]]
current_duck_index = 0
duck_results = []
duck_display_timer = 0
duck_display_duration = 1000

# Rectangle toggle for duck positions
rect_toggle_timer = 0
rect_toggle_duration = 1000
rect_visible = True

# Button rectangles (scaled by 3)
start_button_rect = pygame.Rect(95 * 3, 147 * 3, (159 - 96) * 3, (163 - 148) * 3)
reset_button_rect = pygame.Rect(92 * 3, 184 * 3, (161 - 93) * 3, (199 - 185) * 3)

# Easter egg rectangles (scaled by 3)
duck_section_rect = pygame.Rect(35 * 3, 32 * 3, (182 - 35) * 3, (70 - 32) * 3)
hunt_section_rect = pygame.Rect(74 * 3, 88 * 3, (221 - 74) * 3, (125 - 88) * 3)

# Credit text and rectangle
credit_text = credit_font.render("Arman Jabari", True, (234, 155, 34))
credit_rect = credit_text.get_rect(bottomleft=(10, HEIGHT - 10))
credit_link = "https://github.com/ArmanJ786"

pygame.mouse.set_visible(True)
clock = pygame.time.Clock()

def setup():
    global score, high_score, rectangles, birds, dead_ducks, falling_ducks, spawn_timer, round_num
    global current_duck_index, duck_results, duck_display_timer, rect_toggle_timer, rect_visible, paused
    global round_end_timer, round_end_animation
    global reload_timer, is_reloading
    global plus_100_texts, duck_fall_complete  # MODIFIED: Added duck_fall_complete
    score = 0
    try:
        with open("data.dat", "r") as f:
            high_score = int(f.read())
    except:
        high_score = 0
    rectangles = []
    birds = []
    dead_ducks = []
    falling_ducks = []
    plus_100_texts = []
    spawn_timer = 0
    round_num = 1
    current_duck_index = 0
    duck_results = []
    duck_display_timer = 0
    rect_toggle_timer = 0
    rect_visible = True
    paused = False
    round_end_timer = 0
    round_end_animation = None
    reload_timer = 0
    is_reloading = False
    duck_fall_complete = False  # NEW: Initialize duck_fall_complete

setup()

while True:
    dt = clock.tick(60) / 1000
    if game_started and not paused:
        spawn_timer += dt * 1000
        if round_end_animation:
            round_end_timer += dt
        if is_reloading:
            reload_timer += dt
            if reload_timer >= reload_duration:
                rectangles.clear()
                is_reloading = False
                reload_timer = 0
        for text in plus_100_texts[:]:
            text['timer'] -= dt
            if text['timer'] <= 0:
                plus_100_texts.remove(text)

    mouse_pos = pygame.mouse.get_pos()
    start_hovered = start_button_rect.collidepoint(mouse_pos)
    reset_hovered = reset_button_rect.collidepoint(mouse_pos)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and game_started:
                paused = not paused
                if paused:
                    if current_sound:
                        current_sound.stop()
                else:
                    current_time = datetime.datetime.now().time()
                    if datetime.time(3, 30) <= current_time <= datetime.time(20, 0):
                        current_sound = day_sound
                        day_sound.play(loops=-1)
                    else:
                        current_sound = night_sound
                        night_sound.play(loops=-1)
        elif event.type == pygame.MOUSEBUTTONDOWN and not paused:
            mouse_pos = event.pos
            if not game_started:
                if event.button == 1:
                    if start_button_rect.collidepoint(mouse_pos):
                        click_sound.play()
                        game_started = True
                        pygame.mouse.set_visible(False)
                        current_time = datetime.datetime.now().time()
                        if datetime.time(3, 30) <= current_time <= datetime.time(20, 0):
                            current_sound = day_sound
                            day_sound.play(loops=-1)
                        else:
                            current_sound = night_sound
                            night_sound.play(loops=-1)
                    elif reset_button_rect.collidepoint(mouse_pos):
                        click_sound.play()
                        high_score = 0
                        with open("data.dat", "w") as f:
                            f.write("0")
                    elif credit_rect.collidepoint(mouse_pos):
                        click_sound.play()
                        webbrowser.open(credit_link)
                    elif duck_section_rect.collidepoint(mouse_pos):
                        duck_sound.play()
                    elif hunt_section_rect.collidepoint(mouse_pos):
                        shot_sound.play()
            else:
                if event.button == 1:
                    if not is_reloading:
                        if len(rectangles) >= 3:
                            empty_sound.play()
                        else:
                            shot_sound.play()
                            for bird in birds[:]:
                                bird_rect = bird['frames'][bird['frame']].get_rect(topleft=(bird['x'], bird['y']))
                                if bird_rect.collidepoint(mouse_pos):
                                    duck_sound.play()
                                    points = bird['duck_type']['points']
                                    plus_text = plus_100_font.render(f"+{points}", True, (255, 255, 255))
                                    text_rect = plus_text.get_rect(centerx=bird['x'] + bird['duck_type']['dead_img'].get_width() / 2, bottom=bird['y'] - 10)
                                    plus_100_texts.append({'text': plus_text, 'rect': text_rect, 'timer': 0.5})
                                    dead_ducks.append({'img': bird['duck_type']['dead_img'], 'x': bird['x'], 'y': bird['y'], 'timer': 0.4, 'duck_type': bird['duck_type']})
                                    birds.remove(bird)
                                    score += points
                                    if score > high_score:
                                        high_score = score
                                        with open("data.dat", "w") as f:
                                            f.write(str(high_score))
                                    if current_duck_index < 10:
                                        duck_results.append((duck_positions[current_duck_index][0], duck_positions[current_duck_index][1], pass_duck_img))
                                        current_duck_index += 1
                                        spawn_timer = 0
                            if len(rectangles) < 3:
                                x = 126 - len(rectangles) * 25
                                rectangles.append((x, 624, 14, 24))
                elif event.button == 3:
                    if len(rectangles) >= 3 and not is_reloading:
                        reload_sound.play()
                        is_reloading = True
                        reload_timer = 0

    if game_started and not paused:
        for bird in birds[:]:
            bird['time_on_screen'] += dt
            bird_rect = bird['frames'][bird['frame']].get_rect(topleft=(bird['x'], bird['y']))
            mouse_distance = math.hypot(mouse_pos[0] - (bird['x'] + bird_rect.width / 2), mouse_pos[1] - (bird['y'] + bird_rect.height / 2))
            if mouse_distance < 100 and random.random() < 0.02 and round_num >= 3:
                bird['movement_type'] = random.choice(['zigzag', 'wavy', 'dash'])
                bird['evasion_timer'] = 1.0
                bird['speed_multiplier'] *= 1.5
            if 'evasion_timer' in bird:
                bird['evasion_timer'] -= dt
                if bird['evasion_timer'] <= 0:
                    bird['movement_type'] = bird.get('original_movement_type', 'wavy')
                    bird['speed_multiplier'] = bird.get('original_speed_multiplier', 1.0)
            if bird['time_on_screen'] < 3:
                base_vx = 1 if bird['direction'] == 'left_to_right' else -1
                movement_type = bird.get('movement_type', 'wavy')
                if movement_type == 'wavy':
                    bird['x'] += base_vx * dt * 150 * bird.get('speed_multiplier', 1)
                    bird['y'] = bird['base_y'] + math.sin(bird['time_on_screen'] * 3) * 50
                elif movement_type == 'zigzag':
                    bird['x'] += base_vx * dt * 150 * bird.get('speed_multiplier', 1)
                    bird['y'] = bird['base_y'] + math.sin(bird['time_on_screen'] * 6) * 30
                elif movement_type == 'dash':
                    bird['x'] += base_vx * dt * 200 * bird.get('speed_multiplier', 1)
                    bird['y'] = bird['base_y']
            else:
                bird['x'] += bird['vx'] * dt * 300
                bird['y'] += bird['vy'] * dt * 300
            bird['frame_time'] += dt
            if bird['frame_time'] >= animation_speed:
                bird['frame'] = (bird['frame'] + 1) % 3
                bird['frame_time'] = 0
            if (bird['x'] > WIDTH or 
                bird['x'] < -bird['frames'][bird['frame']].get_width() or 
                bird['y'] < 0 or 
                bird['y'] > HEIGHT):
                birds.remove(bird)
                if current_duck_index < 10:
                    duck_results.append((duck_positions[current_duck_index][0], duck_positions[current_duck_index][1], fail_duck_img))
                    current_duck_index += 1
                    spawn_timer = 0

        for dead in dead_ducks[:]:
            dead['timer'] -= dt
            if dead['timer'] <= 0:
                falling_ducks.append({
                    'x': dead['x'], 
                    'y': dead['y'], 
                    'frame': 0, 
                    'frame_time': 0, 
                    'fall_speed': 0,
                    'fall_frames': dead['duck_type']['fall_frames'],
                    'bush_sound_played': False,
                    'duck_type': dead['duck_type']
                })
                dead_ducks.remove(dead)

        for fall_duck in falling_ducks[:]:
            fall_duck['y'] += fall_duck['fall_speed'] * dt
            fall_duck['fall_speed'] += 400 * dt
            fall_duck['frame_time'] += dt
            if fall_duck['frame_time'] >= 0.1:
                fall_duck['frame'] = (fall_duck['frame'] + 1) % 4
                fall_duck['frame_time'] = 0
            if fall_duck['y'] >= 155 * 3:
                if not fall_duck['bush_sound_played']:
                    bush_sound.play()
                    fall_duck['bush_sound_played'] = True
                falling_ducks.remove(fall_duck)
                duck_fall_complete = True  # NEW: Set flag when duck falls into bush

        if spawn_timer >= spawn_interval and current_duck_index < 10 and not round_end_animation:
            max_birds = 2 if round_num >= 5 else 1
            if len(birds) < max_birds:
                # Select duck type based on spawn probabilities
                duck_type = random.choices(
                    duck_types,
                    weights=[dt['spawn_prob'] for dt in duck_types],
                    k=1
                )[0]
                bird_type = random.choice(['angle', 'straight'])
                direction = random.choice(['left_to_right', 'right_to_left'])
                spawn_y = random.randint(130, 240)
                frames_key = 'angle_frames' if bird_type == 'angle' else 'straight_frames'
                frames_key += '_mirrored' if direction != 'left_to_right' else ''
                frames = duck_type[frames_key]
                x_start = 0 if direction == 'left_to_right' else WIDTH
                vx = 1 if direction == 'left_to_right' else -1
                speed_multiplier = 1 + (round_num * 0.15 if round_num >= 5 else 0)
                movement_type = random.choice(['wavy', 'zigzag', 'dash']) if round_num >= 3 else 'wavy'
                birds.append({
                    'x': x_start, 'y': spawn_y, 'base_y': spawn_y,
                    'vx': vx * speed_multiplier, 'vy': 0,
                    'direction': direction, 'frames': frames,
                    'frame': 0, 'frame_time': 0, 'time_on_screen': 0,
                    'speed_multiplier': speed_multiplier,
                    'movement_type': movement_type,
                    'original_movement_type': movement_type,
                    'original_speed_multiplier': speed_multiplier,
                    'duck_type': duck_type
                })
                spawn_timer = 0

        if current_duck_index >= 10 and not round_end_animation:
            if len(duck_results) == 10 and sum(1 for _, _, img in duck_results if img == fail_duck_img) > 5:
                lose_sound.play()
                pygame.time.wait(int(lose_sound.get_length() * 1000))
                pygame.quit()
                exit()
            if len(duck_results) == 10:
                pass_count = sum(1 for _, _, img in duck_results if img == pass_duck_img)
                if pass_count == 10:
                    score += 500
                    round_end_animation = 'perfect'
                    round_end_timer = 0
                elif pass_count >= 6:
                    round_end_animation = 'partial'
                    round_end_timer = 0
                if score > high_score:
                    high_score = score
                    with open("data.dat", "w") as f:
                        f.write(str(high_score))
        if round_end_timer >= round_end_duration and round_end_animation:
            duck_results.clear()
            current_duck_index = 0
            rectangles.clear()
            round_num += 1
            next_round_sound.play()
            if round_num >= 5:
                animation_speed = max(0.05, 0.1 - (round_num - 5) * 0.01)
                spawn_interval = max(1000, 2000 - (round_num - 5) * 100)
            round_end_animation = None
            round_end_timer = 0
            spawn_timer = 0
            duck_fall_complete = False  # NEW: Reset flag for next round

        if duck_results:
            duck_display_timer += dt * 1000
            if duck_display_timer >= duck_display_duration:
                duck_display_timer = 0
                if len(duck_results) > len(duck_positions):
                    duck_results.pop(0)

        if birds:
            rect_toggle_timer += dt * 1000
            if rect_toggle_timer >= rect_toggle_duration:
                rect_toggle_timer = 0
                rect_visible = not rect_visible
        else:
            rect_visible = False

    if not game_started:
        screen.blit(intro_img, (0, 0))
        if start_hovered:
            screen.blit(start_hover_img, start_button_rect.topleft)
        if reset_hovered:
            screen.blit(reset_hover_img, reset_button_rect.topleft)
        screen.blit(credit_text, credit_rect)
    else:
        current_time = datetime.datetime.now().time()
        if datetime.time(3, 30) <= current_time <= datetime.time(20, 0):
            screen.blit(background, (0, 0))
            if current_sound != day_sound:
                if current_sound:
                    current_sound.stop()
                current_sound = day_sound
                day_sound.play(loops=-1)
        else:
            screen.blit(background2, (0, 0))
            if current_sound != night_sound:
                if current_sound:
                    current_sound.stop()
                current_sound = night_sound
                night_sound.play(loops=-1)
        for fall_duck in falling_ducks:
            screen.blit(fall_duck['fall_frames'][fall_duck['frame']], (fall_duck['x'], fall_duck['y']))
        if round_end_animation and round_end_timer < round_end_duration and duck_fall_complete:  # MODIFIED: Added duck_fall_complete check
            img = partial_success_img if round_end_animation == 'partial' else perfect_success_img
            t = round_end_timer / round_end_duration
            if t < 0.4615:
                y = 146 * 3 - (146 * 3 - 125 * 3) * (t / 0.4615)
            elif t < 0.6923:
                y = 125 * 3
            else:
                y = 125 * 3 + (146 * 3 - 125 * 3) * ((t - 0.6923) / 0.3077)
            img_rect = img.get_rect(centerx=128 * 3, top=y)
            screen.blit(img, img_rect)
        screen.blit(bush_img, bush_rect)
        for bird in birds:
            screen.blit(bird['frames'][bird['frame']], (bird['x'], bird['y']))
        for dead in dead_ducks:
            screen.blit(dead['img'], (dead['x'], dead['y']))
        for text in plus_100_texts:
            screen.blit(text['text'], text['rect'])
        if rect_visible and birds and current_duck_index < len(duck_positions):
            x, y = duck_positions[current_duck_index]
            pygame.draw.rect(screen, (30, 17, 17), (x, y, 7 * 3, 7 * 3))
        for x, y, img in duck_results:
            screen.blit(img, (x, y))
        for rect in rectangles:
            pygame.draw.rect(screen, (30, 17, 17), rect)
        high_score_str = str(high_score).rjust(8, '0')
        score_str = str(score).rjust(8, '0')
        round_text = round_font.render(str(round_num).rjust(3, '0'), True, (255, 255, 255))
        text_high = score_font.render(high_score_str, True, (255, 255, 255))
        text_score = score_font.render(score_str, True, (255, 255, 255))
        screen.blit(round_text, (29 * 3, 193 * 3))
        screen.blit(text_high, (193 * 3, 207 * 3))
        screen.blit(text_score, (193 * 3, 216 * 3))

        if paused:
            screen.blit(pause_img, pause_img_rect)

    if game_started:
        mouse_pos = pygame.mouse.get_pos()
        cursor_img_rect.center = mouse_pos
        screen.blit(cursor_img, cursor_img_rect)

    pygame.display.flip()
