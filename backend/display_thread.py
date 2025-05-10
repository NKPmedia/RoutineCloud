"""
display_thread.py

This module provides a thread for displaying the current task and playing sounds using pygame.
"""
import pyrootutils

root = pyrootutils.setup_root(
    search_from=__file__,
    indicator=["pyproject.toml", ".git"],
    pythonpath=True,
    cwd=True
)



import threading
import time
import os
import pygame
from typing import Optional, Tuple
import colors
from pygame.display import is_fullscreen

from routine_state import routine_state

class DisplayThread(threading.Thread):
    """
    A thread that displays the current task and plays sounds using pygame.
    """
    
    def __init__(self, 
                 sound_dir: str = "sounds",
                 screen_size: Tuple[int, int] = (1024, 600),  # Common Raspberry Pi display size
                 fps: int = 30):
        """
        Initialize the display thread.
        
        Args:
            sound_dir: Directory containing sound files
            screen_size: Size of the display (width, height)
            fps: Frames per second for the display
        """
        super().__init__(daemon=True)  # Run as daemon thread
        self.sound_dir = sound_dir
        self.screen_size = screen_size
        self.fps = fps
        self.running = False
        self.current_sound_playing = None
        
        # Create the sounds directory if it doesn't exist
        os.makedirs(sound_dir, exist_ok=True)
        
        # Initialize pygame
        pygame.init()
        pygame.mixer.init()
        
        # Set up the display
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption("Bedtime Routine")
        
        # Set up fonts
        self.title_font = pygame.font.Font(None, 72)
        self.task_font = pygame.font.Font(None, 48)
        
        # Clock for controlling frame rate
        self.clock = pygame.time.Clock()
    
    def run(self):
        """Main thread loop."""
        self.running = True
        
        while self.running:
            # Handle pygame events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self._handle_full_screen_toggle(event, screen=self.screen)
            
            # Clear the screen
            self.screen.fill(colors.BACKGROUND)
            
            # Get the current state
            is_active = routine_state.is_routine_active
            current_task = routine_state.current_task
            current_sound = routine_state.current_sound
            
            # Draw the title
            title_text = "Bedtime Routine"
            title_surface = self.title_font.render(title_text, True, colors.TEXT_LIGHT_BEIGE)
            title_rect = title_surface.get_rect(center=(self.screen_size[0] // 2, 50))
            self.screen.blit(title_surface, title_rect)
            
            # Draw the current task if active
            if is_active and current_task:
                task_text = f"Current Task: {current_task['name']}"
                task_surface = self.task_font.render(task_text, True, colors.TEXT_LIGHT_BEIGE)
                task_rect = task_surface.get_rect(center=(self.screen_size[0] // 2, self.screen_size[1] // 2))
                self.screen.blit(task_surface, task_rect)
            else:
                # Draw inactive message
                inactive_text = "No Active Routine"
                inactive_surface = self.task_font.render(inactive_text, True, colors.TEXT_LIGHT_BEIGE)
                inactive_rect = inactive_surface.get_rect(center=(self.screen_size[0] // 2, self.screen_size[1] // 2))
                self.screen.blit(inactive_surface, inactive_rect)
            
            # Play sound if needed
            self._handle_sound(current_sound)
            
            # Update the display
            pygame.display.flip()
            
            # Control the frame rate
            self.clock.tick(self.fps)
        
        # Clean up pygame
        pygame.quit()
    
    def _handle_sound(self, sound_name: Optional[str]):
        """
        Handle playing the current sound.
        
        Args:
            sound_name: Name of the sound file to play
        """
        if sound_name is None:
            # Stop any playing sound if no sound is requested
            if self.current_sound_playing:
                pygame.mixer.music.stop()
                self.current_sound_playing = None
            return
        
        # If a new sound is requested and it's different from the current one
        if sound_name != self.current_sound_playing:
            # Stop any currently playing sound
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
            
            # Try to play the new sound
            sound_path = os.path.join(self.sound_dir, sound_name)
            if os.path.exists(sound_path):
                try:
                    pygame.mixer.music.load(sound_path)
                    pygame.mixer.music.play()
                    self.current_sound_playing = sound_name
                except pygame.error as e:
                    print(f"Error playing sound {sound_name}: {e}")
                    self.current_sound_playing = None
            else:
                print(f"Sound file not found: {sound_path}")
                self.current_sound_playing = None
    
    def stop(self):
        """Stop the display thread."""
        self.running = False

    def _handle_full_screen_toggle(self, event, screen, key=pygame.K_F11):
        if event.type == pygame.KEYDOWN and event.key == key:
            is_fullscreen = screen.get_flags() & pygame.FULLSCREEN
            if is_fullscreen:
                screen = pygame.display.set_mode(self.screen_size)
            else:
                screen = pygame.display.set_mode(self.screen_size, pygame.FULLSCREEN)
        return screen


# Function to start the display thread
def start_display_thread(sound_dir: str = "sounds", 
                         screen_size: Tuple[int, int] = (1024, 600),
                         fps: int = 30) -> DisplayThread:
    """
    Start the display thread.
    
    Args:
        sound_dir: Directory containing sound files
        screen_size: Size of the display (width, height)
        fps: Frames per second for the display
        
    Returns:
        The started display thread
    """
    display_thread = DisplayThread(sound_dir=sound_dir, screen_size=screen_size, fps=fps)
    display_thread.start()
    return display_thread

if __name__ == "__main__":
    # Test the display thread
    thread = start_display_thread()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        thread.stop()