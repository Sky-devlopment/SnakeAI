import pygame
import random
import math

# Project Configuration
SIZE = 20  # Map size (grid width and height)
CELL_SIZE = 20  # Size of each cell in pixels
WINDOW_SIZE = SIZE * CELL_SIZE  # Size of the game window

class Game:
    def __init__(self):
        # Initialize the game window
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption("Snake Game")
        
        # Initialize the game clock
        self.clock = pygame.time.Clock()
        
        # Initialize the game state
        self.reset()
        
        # Initialize the score
        self.highscore = 0

    def reset(self):
        self.snake = [(SIZE // 2, SIZE // 2)]  # List of (x, y) positions
        self.direction = (0, -1)  # Initial direction (up)
        self.food = self.place_food()
        self.score = 0
        self.game_over = False

    def place_food(self):
        while True:
            food_position = (random.randint(0, SIZE - 1), random.randint(0, SIZE - 1))
            if food_position not in self.snake:
                return food_position

    def get_pos(self, target):
        if target == "head":
            return self.snake[0]
        elif target == "food":
            return self.food
        elif target == "tail":
            return self.snake[-1]
        else:
            raise ValueError("Unknown target: {}".format(target))

    def dist(self, target1, target2):
        pos1 = self.get_pos(target1)
        pos2 = self.get_pos(target2)
        return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

    def size(self):
        return len(self.snake)

    def draw_grid(self):
        for x in range(0, WINDOW_SIZE, CELL_SIZE):
            for y in range(0, WINDOW_SIZE, CELL_SIZE):
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, (40, 40, 40), rect, 1)

    def draw_snake(self):
        for segment in self.snake:
            rect = pygame.Rect(segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.screen, (0, 255, 0), rect)

    def draw_food(self):
        rect = pygame.Rect(self.food[0] * CELL_SIZE, self.food[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.screen, (255, 0, 0), rect)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()  # Exit the program immediately
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.up()
                elif event.key == pygame.K_DOWN:
                    self.down()
                elif event.key == pygame.K_LEFT:
                    self.left()
                elif event.key == pygame.K_RIGHT:
                    self.right()

    def up(self):
        if self.direction != (0, 1):
            self.direction = (0, -1)

    def down(self):
        if self.direction != (0, -1):
            self.direction = (0, 1)

    def left(self):
        if self.direction != (1, 0):
            self.direction = (-1, 0)

    def right(self):
        if self.direction != (-1, 0):
            self.direction = (1, 0)

    def update(self):
        if not self.game_over:
            # Move the snake
            new_head = (self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1])
            self.snake.insert(0, new_head)
            
            # Check if the snake has eaten the food
            if new_head == self.food:
                self.food = self.place_food()
                self.score += 1
                self.highscore = max(self.highscore, self.score)
            else:
                self.snake.pop()

            # Check for collisions
            if (new_head[0] < 0 or new_head[0] >= SIZE or
                new_head[1] < 0 or new_head[1] >= SIZE or
                new_head in self.snake[1:]):
                self.game_over = True

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.draw_grid()
        self.draw_snake()
        self.draw_food()
        self.draw_score()
        pygame.display.flip()

    def draw_score(self):
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        highscore_text = font.render(f"High Score: {self.highscore}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(highscore_text, (10, 50))

    def run(self):
        while True:
            self.handle_events()
            if not self.game_over:
                self.update()
                self.draw()
                self.clock.tick(5)  # Reduced game speed (frames per second)
            else:
                self.reset()

if __name__ == "__main__":
    game = Game()
    game.run()
          
