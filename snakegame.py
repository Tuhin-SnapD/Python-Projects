"""
Enhanced Snake Game

A feature-rich implementation with multiple difficulty levels,
power-ups, enhanced graphics, and improved gameplay mechanics.
"""

import pygame
import random
import sys
import time
from typing import List, Tuple, Optional
from enum import Enum


class Direction(Enum):
    """Snake movement directions."""
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


class PowerUp(Enum):
    """Power-up types."""
    SPEED_UP = "speed_up"
    SPEED_DOWN = "speed_down"
    DOUBLE_POINTS = "double_points"
    SHIELD = "shield"
    GHOST = "ghost"


class SnakeGame:
    """Enhanced Snake game with advanced features."""
    
    def __init__(self):
        pygame.init()
        
        # Game settings
        self.width = 800
        self.height = 600
        self.grid_size = 20
        self.grid_width = self.width // self.grid_size
        self.grid_height = self.height // self.grid_size
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)
        self.PURPLE = (128, 0, 128)
        self.ORANGE = (255, 165, 0)
        self.GRAY = (128, 128, 128)
        
        # Game state
        self.snake = [(self.grid_width // 2, self.grid_height // 2)]
        self.direction = Direction.RIGHT
        self.food = self.generate_food()
        self.power_up = None
        self.power_up_pos = None
        self.power_up_timer = 0
        self.score = 0
        self.high_score = 0
        self.level = 1
        self.speed = 10
        self.game_over = False
        self.paused = False
        self.shield_active = False
        self.ghost_active = False
        self.double_points_active = False
        
        # Initialize display
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("🐍 Enhanced Snake Game")
        self.clock = pygame.time.Clock()
        
        # Load fonts
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        # Load high score
        self.load_high_score()
    
    def load_high_score(self):
        """Load high score from file."""
        try:
            with open("snake_high_score.txt", "r") as f:
                self.high_score = int(f.read())
        except:
            self.high_score = 0
    
    def save_high_score(self):
        """Save high score to file."""
        try:
            with open("snake_high_score.txt", "w") as f:
                f.write(str(self.high_score))
        except:
            pass
    
    def generate_food(self) -> Tuple[int, int]:
        """Generate food at random position."""
        while True:
            x = random.randint(0, self.grid_width - 1)
            y = random.randint(0, self.grid_height - 1)
            if (x, y) not in self.snake:
                return (x, y)
    
    def generate_power_up(self):
        """Generate a power-up."""
        if random.random() < 0.1:  # 10% chance
            self.power_up = random.choice(list(PowerUp))
            while True:
                x = random.randint(0, self.grid_width - 1)
                y = random.randint(0, self.grid_height - 1)
                if (x, y) not in self.snake and (x, y) != self.food:
                    self.power_up_pos = (x, y)
                    self.power_up_timer = 100  # Power-up lasts for 100 frames
                    break
    
    def get_power_up_color(self, power_up: PowerUp) -> Tuple[int, int, int]:
        """Get color for power-up."""
        if power_up == PowerUp.SPEED_UP:
            return self.YELLOW
        elif power_up == PowerUp.SPEED_DOWN:
            return self.BLUE
        elif power_up == PowerUp.DOUBLE_POINTS:
            return self.PURPLE
        elif power_up == PowerUp.SHIELD:
            return self.ORANGE
        elif power_up == PowerUp.GHOST:
            return self.GRAY
        return self.WHITE
    
    def apply_power_up(self, power_up: PowerUp):
        """Apply power-up effect."""
        if power_up == PowerUp.SPEED_UP:
            self.speed = min(20, self.speed + 2)
        elif power_up == PowerUp.SPEED_DOWN:
            self.speed = max(5, self.speed - 2)
        elif power_up == PowerUp.DOUBLE_POINTS:
            self.double_points_active = True
        elif power_up == PowerUp.SHIELD:
            self.shield_active = True
        elif power_up == PowerUp.GHOST:
            self.ghost_active = True
    
    def update_power_ups(self):
        """Update power-up timers."""
        if self.power_up_timer > 0:
            self.power_up_timer -= 1
            if self.power_up_timer == 0:
                # Reset power-up effects
                self.shield_active = False
                self.ghost_active = False
                self.double_points_active = False
                self.power_up = None
                self.power_up_pos = None
        
        # Generate new power-up
        if self.power_up is None and random.random() < 0.005:  # 0.5% chance per frame
            self.generate_power_up()
    
    def move_snake(self):
        """Move the snake."""
        head = self.snake[0]
        dx, dy = self.direction.value
        new_head = (head[0] + dx, head[1] + dy)
        
        # Check for wall collision (unless ghost mode is active)
        if not self.ghost_active:
            if (new_head[0] < 0 or new_head[0] >= self.grid_width or
                new_head[1] < 0 or new_head[1] >= self.grid_height):
                if not self.shield_active:
                    self.game_over = True
                return
        
        # Wrap around if ghost mode is active
        if self.ghost_active:
            new_head = (new_head[0] % self.grid_width, new_head[1] % self.grid_height)
        
        # Check for self collision (unless ghost mode is active)
        if not self.ghost_active and new_head in self.snake:
            if not self.shield_active:
                self.game_over = True
            return
        
        # Move snake
        self.snake.insert(0, new_head)
        
        # Check for food collision
        if new_head == self.food:
            self.score += 10 * (2 if self.double_points_active else 1)
            self.food = self.generate_food()
            # Increase level every 100 points
            self.level = self.score // 100 + 1
            self.speed = min(20, 10 + self.level)
        else:
            self.snake.pop()
        
        # Check for power-up collision
        if self.power_up_pos and new_head == self.power_up_pos:
            self.apply_power_up(self.power_up)
            self.power_up = None
            self.power_up_pos = None
            self.power_up_timer = 0
    
    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pygame.K_r and self.game_over:
                    self.reset_game()
                elif not self.paused and not self.game_over:
                    if event.key == pygame.K_UP and self.direction != Direction.DOWN:
                        self.direction = Direction.UP
                    elif event.key == pygame.K_DOWN and self.direction != Direction.UP:
                        self.direction = Direction.DOWN
                    elif event.key == pygame.K_LEFT and self.direction != Direction.RIGHT:
                        self.direction = Direction.LEFT
                    elif event.key == pygame.K_RIGHT and self.direction != Direction.LEFT:
                        self.direction = Direction.RIGHT
        
        return True
    
    def draw_snake(self):
        """Draw the snake."""
        for i, segment in enumerate(self.snake):
            color = self.GREEN if i == 0 else self.GREEN  # Head and body same color for now
            if self.shield_active:
                color = self.ORANGE  # Shield effect
            elif self.ghost_active:
                color = self.GRAY  # Ghost effect
            
            x, y = segment
            rect = pygame.Rect(x * self.grid_size, y * self.grid_size, 
                             self.grid_size, self.grid_size)
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, self.BLACK, rect, 1)
    
    def draw_food(self):
        """Draw the food."""
        x, y = self.food
        rect = pygame.Rect(x * self.grid_size, y * self.grid_size, 
                          self.grid_size, self.grid_size)
        pygame.draw.rect(self.screen, self.RED, rect)
        pygame.draw.rect(self.screen, self.BLACK, rect, 1)
    
    def draw_power_up(self):
        """Draw the power-up."""
        if self.power_up and self.power_up_pos:
            x, y = self.power_up_pos
            rect = pygame.Rect(x * self.grid_size, y * self.grid_size, 
                             self.grid_size, self.grid_size)
            color = self.get_power_up_color(self.power_up)
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, self.BLACK, rect, 2)
    
    def draw_ui(self):
        """Draw user interface."""
        # Score and level
        score_text = self.font_medium.render(f"Score: {self.score}", True, self.WHITE)
        level_text = self.font_medium.render(f"Level: {self.level}", True, self.WHITE)
        speed_text = self.font_medium.render(f"Speed: {self.speed}", True, self.WHITE)
        
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(level_text, (10, 40))
        self.screen.blit(speed_text, (10, 70))
        
        # High score
        high_score_text = self.font_medium.render(f"High Score: {self.high_score}", True, self.WHITE)
        self.screen.blit(high_score_text, (self.width - 200, 10))
        
        # Power-up status
        if self.shield_active:
            shield_text = self.font_small.render("SHIELD ACTIVE", True, self.ORANGE)
            self.screen.blit(shield_text, (10, 100))
        
        if self.ghost_active:
            ghost_text = self.font_small.render("GHOST MODE", True, self.GRAY)
            self.screen.blit(ghost_text, (10, 120))
        
        if self.double_points_active:
            double_text = self.font_small.render("DOUBLE POINTS", True, self.PURPLE)
            self.screen.blit(double_text, (10, 140))
        
        # Instructions
        if not self.game_over:
            instructions = [
                "Arrow Keys: Move",
                "Space: Pause",
                "ESC: Quit"
            ]
            for i, instruction in enumerate(instructions):
                text = self.font_small.render(instruction, True, self.WHITE)
                self.screen.blit(text, (10, self.height - 80 + i * 20))
    
    def draw_game_over(self):
        """Draw game over screen."""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(128)
        overlay.fill(self.BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Game over text
        game_over_text = self.font_large.render("GAME OVER", True, self.RED)
        text_rect = game_over_text.get_rect(center=(self.width // 2, self.height // 2 - 50))
        self.screen.blit(game_over_text, text_rect)
        
        # Final score
        final_score_text = self.font_medium.render(f"Final Score: {self.score}", True, self.WHITE)
        score_rect = final_score_text.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(final_score_text, score_rect)
        
        # Restart instruction
        restart_text = self.font_medium.render("Press R to Restart", True, self.WHITE)
        restart_rect = restart_text.get_rect(center=(self.width // 2, self.height // 2 + 50))
        self.screen.blit(restart_text, restart_rect)
    
    def draw_pause(self):
        """Draw pause screen."""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(128)
        overlay.fill(self.BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Pause text
        pause_text = self.font_large.render("PAUSED", True, self.YELLOW)
        text_rect = pause_text.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(pause_text, text_rect)
        
        # Resume instruction
        resume_text = self.font_medium.render("Press Space to Resume", True, self.WHITE)
        resume_rect = resume_text.get_rect(center=(self.width // 2, self.height // 2 + 50))
        self.screen.blit(resume_text, resume_rect)
    
    def reset_game(self):
        """Reset the game."""
        self.snake = [(self.grid_width // 2, self.grid_height // 2)]
        self.direction = Direction.RIGHT
        self.food = self.generate_food()
        self.power_up = None
        self.power_up_pos = None
        self.power_up_timer = 0
        self.score = 0
        self.level = 1
        self.speed = 10
        self.game_over = False
        self.paused = False
        self.shield_active = False
        self.ghost_active = False
        self.double_points_active = False
    
    def run(self):
        """Main game loop."""
        running = True
        
        while running:
            running = self.handle_events()
            
            if not self.game_over and not self.paused:
                self.move_snake()
                self.update_power_ups()
                
                # Update high score
                if self.score > self.high_score:
                    self.high_score = self.score
                    self.save_high_score()
            
            # Draw everything
            self.screen.fill(self.BLACK)
            self.draw_snake()
            self.draw_food()
            self.draw_power_up()
            self.draw_ui()
            
            if self.game_over:
                self.draw_game_over()
            elif self.paused:
                self.draw_pause()
            
            pygame.display.flip()
            self.clock.tick(self.speed)
        
        pygame.quit()
        sys.exit()


def main():
    """Main function to start the game."""
    try:
        game = SnakeGame()
        game.run()
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please try running the game again.")


if __name__ == "__main__":
    main()