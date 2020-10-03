import random
import pygame
import sys
from math import floor

# global variables
WIDTH = 24
HEIGHT = 24
SIZE = 20
SCREEN_WIDTH = WIDTH * SIZE
SCREEN_HEIGHT = HEIGHT * SIZE
RESTART = True

DIR = {
    'u': (0, -1),  # north is -y
    'd': (0, 1),
    'l': (-1, 0),
    'r': (1, 0)
}


class Snake(object):
    l = 1
    body = [(WIDTH // 2, HEIGHT // 2)]
    direction = 'r'
    dead = False

    def __init__(self):
        pass

    def get_color(self, i):
        hc = (40, 50, 100)
        tc = (90, 130, 255)
        return tuple(map(lambda x, y: (x * (self.l - i) + y * i) / self.l, hc, tc))

    def get_head(self):
        return self.body[0]

    def turn(self, dir):
        # See section 3, "Turning the snake".
        self.direction = dir

    def collision(self, x, y):
        # See section 2, "Collisions", and section 4, "Self Collisions"
        if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
            return True
        if (x, y) in self.body:
            return True
        return False

    def coyote_time(self):
        # TODO: See section 13, "coyote time".
        pass

    def move(self):
        # TODO: See section 1, "Move the snake!". You will be revisiting this section a few times.
        newPos = (self.body[0][0]+DIR[self.direction][0],
                  self.body[0][1]+DIR[self.direction][1])
        if self.collision(newPos[0], newPos[1]):
            self.kill()
        print(self.body)
        self.body = [newPos] + self.body[:-1]
        print(len(self.body))

    def kill(self):
        # TODO: See section 11, "Try again!"
        self.dead = True

    def draw(self, surface):
        for i in range(len(self.body)):
            p = self.body[i]
            pos = (p[0] * SIZE, p[1] * SIZE)
            r = pygame.Rect(pos, (SIZE, SIZE))
            pygame.draw.rect(surface, self.get_color(i), r)

    def handle_keypress(self, k):
        if k == pygame.K_UP:
            self.turn('u')
        if k == pygame.K_DOWN:
            self.turn('d')
        if k == pygame.K_LEFT:
            self.turn('l')
        if k == pygame.K_RIGHT:
            self.turn('r')

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type != pygame.KEYDOWN:
                continue
            self.handle_keypress(event.key)

    def wait_for_key(self):
        # TODO: see section 10, "wait for user input".
        pass


# returns an integer between 0 and n, inclusive.
def rand_int(n):
    return random.randint(0, n)


class Apple(object):
    position = (10, 10)
    color = (233, 70, 29)

    def __init__(self):
        self.place([])

    def place(self, snake):
        # see section 6, "moving the apple".
        x = rand_int(WIDTH)
        y = rand_int(HEIGHT)
        if snake != []:
            while (x, y) in snake.body or x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
                x = rand_int(WIDTH)
                y = rand_int(HEIGHT)
        self.position = (x, y)

    def draw(self, surface):
        pos = (self.position[0] * SIZE, self.position[1] * SIZE)
        r = pygame.Rect(pos, (SIZE, SIZE))
        pygame.draw.rect(surface, self.color, r)


def draw_grid(surface):
    for y in range(0, HEIGHT):
        for x in range(0, WIDTH):
            r = pygame.Rect((x * SIZE, y * SIZE), (SIZE, SIZE))
            color = (169, 215, 81) if (x+y) % 2 == 0 else (162, 208, 73)
            pygame.draw.rect(surface, color, r)


def waitResponse():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                # pygame.quit()
                # sys.exit(0)
                main()
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit(0)
                return


def main():

    pygame.init()
    pygame.font.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    draw_grid(surface)

    snake = Snake()
    apple = Apple()

    refreshRate = 5

    score = 0

    while True:
        # TODO: see section 10, "incremental difficulty".
        clock.tick(refreshRate)
        snake.check_events()
        draw_grid(surface)
        snake.move()

        snake.draw(surface)
        apple.draw(surface)
        # see section 5, "Eating the Apple".
        if snake.body[0] == apple.position:
            snake.l += 1
            newPart = (snake.body[0][0]+DIR[snake.direction]
                        [0], snake.body[0][1]+DIR[snake.direction][1])
            snake.body = [newPart] + snake.body
            print(snake.body)
            apple.place(snake)
            score += 1
            if refreshRate < 15 and snake.l % 5 == 0:  # increase difficulty as length increases
                refreshRate += 1
        screen.blit(surface, (0, 0))
        # see section 8, "Display the Score"
        myfont = pygame.font.Font('Ubuntu-R.ttf', 30)
        scoreText = myfont.render(
            'Score: ' + str(score), False, (255, 255, 255))
        screen.blit(scoreText, (20, 20))

        pygame.display.update()
        if snake.dead:
            print(f'You died. Score: {score}')
            gameOverFont = pygame.font.Font('Ubuntu-R.ttf', 30)
            gameOverText = gameOverFont.render(
                'Game Over!', False, (255, 87, 51))
            screen.blit(gameOverText, (240, 240))
            pygame.display.update()
            waitResponse()


if __name__ == "__main__":
    main()
