import pygame
from snake import Snake
pygame.init()


class Game:
    def __init__(self, display_width: int, display_height: int) -> None:
        # Display init
        self.display_width = display_width
        self.display_height = display_height
        self.display = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption("Snek")

        # FPS clock
        self.clock = pygame.time.Clock()

        # Init snake object
        self.snake = Snake(self.display)

        # Init pressed keys list
        self.keys_pressed = list()
    
    def draw_grid(self) -> None:
        for i in range(self.display_width//self.snake.get_node_radius() + 1):
            pygame.draw.line(self.display, pygame.Color(255, 255, 255), (self.snake.get_node_radius() * 2 * i, 0), (self.snake.get_node_radius() * 2 * i, self.display_height))
        for i in range(self.display_height//self.snake.get_node_radius() + 1):
            pygame.draw.line(self.display, pygame.Color(255, 255, 255), (0, self.snake.get_node_radius() * 2 * i), (self.display_width, self.snake.get_node_radius() * 2 * i))
    
    def is_in_bounds(self) -> bool:
        snake_x, snake_y = self.snake.get_coords()
        if 0 < snake_x < self.display_width and 0 < snake_y < self.display_height:
            return True
        return False

    def play(self) -> None:
        def deathScreen() -> None:
            nonlocal run
            print("you died")
            run = False

        run = True
        while run:
            self.clock.tick(7)
            self.display.fill(pygame.Color(0, 0, 0))

            for event in pygame.event.get():
                # Quits game when quit button is pressed
                if event.type == pygame.QUIT:
                    run = False
                
                # Listens for key presses
                elif event.type == pygame.KEYDOWN:
                    self.keys_pressed.append(event.key)

            if self.keys_pressed:
                key = self.keys_pressed.pop(0)
                if key == pygame.K_w and self.snake.get_direction() != "down":
                    self.snake.set_direction("up")
                elif key == pygame.K_s and self.snake.get_direction() != "up":
                    self.snake.set_direction("down")
                elif key == pygame.K_a and self.snake.get_direction() != "right":
                    self.snake.set_direction("left")
                elif key == pygame.K_d and self.snake.get_direction() != "left":
                    self.snake.set_direction("right")
            
            # Checks if snake touched the apple
            if self.snake.get_apple_rect() and self.snake.get_apple_rect().colliderect(self.snake.get_nodes().get_head().value.get_rect()):
                self.snake.set_is_eating(2)


            if self.is_in_bounds() and not self.snake.check_loop_collision():  # Checks if snake is in game area and doesn't loop on itself
                if self.snake.get_direction():                                 # Checks if the player pressed the first move key
                    self.snake.move()
                self.snake.draw()
            else:
                deathScreen()
            
            self.draw_grid()
            pygame.display.update()


if __name__ == "__main__":
    game = Game(450, 450)
    game.play()