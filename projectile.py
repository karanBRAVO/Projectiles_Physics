import pygame
import math
import random
import pyttsx3

pygame.init()
engine = pyttsx3.init()

text = "Hello user, Welcome to projectile demonstrations try to hit the target using accurate calculations."

engine.say(text)
engine.runAndWait()

clock = pygame.time.Clock()
fps = 60

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

font = pygame.font.SysFont("serif", 14, False)

windowWidth = 700
windowHeight = 400
window = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("Projectile Motion")
print("*** Range and Max Height Problems ***")

ground_rect = pygame.Rect(0, 350, windowWidth, 100)

stone_rect = pygame.Rect(0, ground_rect.y - 10, 10, 10)

x = random.randrange(50, windowWidth - 25, 10)
y = random.randrange(0, ground_rect.y - 25, 10)
hole_rect_hor = pygame.Rect(x, ground_rect.y, 25, 7)
hole_rect_vert = pygame.Rect(windowWidth - 8, y, 7, 25)

mouse_x = 0
mouse_y = 0

u = 0  # initial speed
phi = 0  # initial angle
g = 9.8  # gravity
R = 0  # Range
H = 0  # max height
T = 0  # time period
launch = False  # when to launch
div_R = None
t = 0  # timer
lst = []  # stores path of stone

score = 0


def show_score(text):
    msg = font.render(f"Score: {text}", True, red)
    window.blit(msg, (windowWidth - 350, 40))


def hole_vert():
    global score

    if stone_rect.colliderect(hole_rect_vert):
        score += 10
        hole_rect_vert.y = random.randrange(0, ground_rect.y - hole_rect_vert.height, 10)

    pygame.draw.rect(window, black, hole_rect_vert)


def hole_hor():
    global score

    if stone_rect.colliderect(hole_rect_hor):
        score += 20
        hole_rect_hor.x = random.randrange(70, windowWidth - 25, 10)

    pygame.draw.rect(window, black, hole_rect_hor)


def Reset():
    global launch, div_R, t, mouse_y, mouse_x, stone_rect
    launch = False
    div_R = None
    t = 0
    mouse_x = 0
    mouse_y = 0
    stone_rect = pygame.Rect(0, ground_rect.y - 10, 10, 10)
    lst.clear()


def motion():
    global mouse_x, mouse_y, u, phi, R, H, T, launch, div_R, t

    if pygame.mouse.get_pressed(3):
        mouse_x, mouse_y = pygame.mouse.get_pos()

    if not launch:
        u = ((stone_rect.centerx - mouse_x) ** 2 + (stone_rect.centery - mouse_y) ** 2) ** 0.5
        try:
            phi = math.atan(abs(stone_rect.centery - mouse_y) / abs(stone_rect.centerx - mouse_x))
        except ZeroDivisionError:
            phi = math.pi / 2
        R = ((u ** 2) * 2 * math.sin(phi) * math.cos(phi)) / g
        H = ((u ** 2) * ((math.sin(phi)) ** 2)) / (2 * g)
        T = (2 * u * math.sin(phi)) / g

    msg1 = font.render(f"Initial speed: {u}", True, black, None)
    msg2 = font.render(f"Angle: {math.degrees(phi)}", True, black, None)
    msg3 = font.render(f"Range: {R}", True, black, None)
    msg4 = font.render(f"Max. Height: {H}", True, black, None)
    msg5 = font.render(f"Time_Period: {T}", True, black, None)
    window.blit(msg1, (2, 0))
    window.blit(msg2, (2, 20))
    window.blit(msg3, (2, 40))
    window.blit(msg4, (2, 60))
    window.blit(msg5, (2, 80))

    if pygame.mouse.get_pressed(3)[0] and not launch:
        # print("u: ", u, "phi: ", math.degrees(phi), "\nR: ", R, "H: ", H, "\nT: ", T)
        # print("initial_x_vel: ", u * math.cos(phi), "initial_y_vel: ", u * math.sin(phi))
        launch = True
        if mouse_x < stone_rect.centerx:
            Reset()

    if pygame.mouse.get_pressed(3)[2]:
        Reset()

    if launch:
        if t <= T:
            t += 0.1

        if R > windowWidth * 10:
            div_R = 100
        else:
            div_R = 10

        if phi != 0:
            stone_rect.centerx += ((u * math.cos(phi)) / 10)
            stone_rect.centery -= ((u * math.sin(phi)) + (-g * t)) / 10
            lst.append([stone_rect.centerx, stone_rect.centery])

        if stone_rect.centerx >= R / div_R and stone_rect.y >= ground_rect.y - stone_rect.height:
            launch = False
            div_R = None
            t = 0

    pygame.draw.rect(window, black, stone_rect)
    if not launch:
        pygame.draw.line(window, blue, start_pos=(stone_rect.centerx, stone_rect.centery), end_pos=(mouse_x, mouse_y), width=1)
    if len(lst) > 0:
        for item in lst:
            pygame.draw.rect(window, black, (item[0], item[1], 1, 1))


def redrawGameWindow():
    window.fill(white)
    pygame.draw.rect(window, green, ground_rect)
    motion()
    hole_hor()
    hole_vert()
    show_score(score)


def mainLoop():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                run = False

        redrawGameWindow()
        pygame.display.update()
        clock.tick(fps)
    pygame.quit()


if __name__ == "__main__":
    mainLoop()
