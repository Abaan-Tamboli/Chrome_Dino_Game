import pygame
import os
import random

pygame.init()

# Global Constants
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dino Game")  # Change window name to "Dino Game"

RUNNING = [pygame.image.load(os.path.join("Assets/Dino", f"DinoRun{i}.png")) for i in range(1, 3)]
JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
DUCKING = [pygame.image.load(os.path.join("Assets/Dino", f"DinoDuck{i}.png")) for i in range(1, 3)]

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", f"SmallCactus{i}.png")) for i in range(1, 4)]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", f"LargeCactus{i}.png")) for i in range(1, 4)]

BIRD = [pygame.image.load(os.path.join("Assets/Bird", f"Bird{i}.png")) for i in range(1, 3)]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))

# Load highest score from a file
def load_high_score():
    try:
        with open("highest_score.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

# Save highest score to a file
def save_high_score(score):
    with open("highest_score.txt", "w") as file:
        file.write(str(score))

class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect(topleft=(self.X_POS, self.Y_POS))

    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        elif self.dino_run:
            self.run()
        elif self.dino_jump:
            self.jump()

        self.step_index = (self.step_index + 1) % 10

        if userInput[pygame.K_UP] and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect(topleft=(self.X_POS, self.Y_POS_DUCK))

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect(topleft=(self.X_POS, self.Y_POS))

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, self.dino_rect)


class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect(topleft=(SCREEN_WIDTH, 0))

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class SmallCactus(Obstacle):
    def __init__(self, image):
        super().__init__(image, random.randint(0, 2))
        self.rect.y = 325


class LargeCactus(Obstacle):
    def __init__(self, image):
        super().__init__(image, random.randint(0, 2))
        self.rect.y = 300


class Bird(Obstacle):
    def __init__(self, image):
        super().__init__(image, 0)
        self.rect.y = 250
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1


def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, highest_score
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    highest_score = load_high_score()  # Load highest score from file
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []

    def score():
        global points, game_speed, highest_score
        points += 1
        if points % 100 == 0:
            game_speed += 1

        text = font.render("Points: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect(center=(1000, 40))
        SCREEN.blit(text, textRect)

        # Display highest score
        highest_score_text = font.render("Highest Score: " + str(highest_score), True, (0, 0, 0))
        highest_score_rect = highest_score_text.get_rect(center=(1000, 60))
        SCREEN.blit(highest_score_text, highest_score_rect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()

        player.draw(SCREEN)
        player.update(userInput)

        if len(obstacles) == 0:
            obstacle_type = random.choice([SmallCactus, LargeCactus, Bird])
            obstacle_images = SMALL_CACTUS if obstacle_type == SmallCactus else (LARGE_CACTUS if obstacle_type == LargeCactus else BIRD)
            obstacles.append(obstacle_type(obstacle_images))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if not player.dino_duck and player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(2000)
                if points > highest_score:
                    highest_score = points  # Update highest score
                    save_high_score(highest_score)  # Save highest score to file
                menu()

        background()

        cloud.draw(SCREEN)
        cloud.update()

        score()

        clock.tick(30)
        pygame.display.update()


def menu():
    global points, highest_score
    run = True
    death_count = 0
    
    # Retrieve highest score
    highest_score = load_high_score()

    while run:
        SCREEN.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 30)

        # Display highest score on the home screen
        highest_score_text = font.render("Highest Score: " + str(highest_score), True, (0, 0, 0))
        highest_score_rect = highest_score_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        SCREEN.blit(highest_score_text, highest_score_rect)

        if death_count == 0:
            text = font.render("Press any Key to Start", True, (0, 0, 0))
        else:
            text = font.render("Press any Key to Restart", True, (0, 0, 0))
            score_text = font.render("Your Score: " + str(points), True, (0, 0, 0))
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            SCREEN.blit(score_text, score_rect)

        textRect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.KEYDOWN:
                points = 0
                main()
                death_count += 1


menu()
