"""
routine_state.py

This module provides a thread-safe singleton state for managing the child's bedtime routine.
It tracks the current task, sound to play, and overall routine state.
"""

import threading
from typing import List, Dict, Optional, Any

class RoutineState:
    """
    A thread-safe singleton class that maintains the state of the current routine.
    """
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(RoutineState, cls).__new__(cls)
                cls._instance._initialize()
            return cls._instance
    
    def _initialize(self):
        """Initialize the state with default values."""
        self._state_lock = threading.RLock()
        self._tasks = [
            {"id": 1, "name": "Brush Teeth", "sound": "brush_teeth.mp3", "duration": 120},
            {"id": 2, "name": "Put on Pajamas", "sound": "pajamas.mp3", "duration": 180},
            {"id": 3, "name": "Read a Book", "sound": "book.mp3", "duration": 300},
            {"id": 4, "name": "Go to Sleep", "sound": "sleep.mp3", "duration": 60}
        ]
        self._current_task_index = -1  # No task active initially
        self._is_routine_active = False
        self._current_sound = None
    
    @property
    def tasks(self) -> List[Dict[str, Any]]:
        """Get the list of tasks in the routine."""
        with self._state_lock:
            return self._tasks.copy()
    
    @property
    def current_task(self) -> Optional[Dict[str, Any]]:
        """Get the current active task or None if no task is active."""
        with self._state_lock:
            if 0 <= self._current_task_index < len(self._tasks):
                return self._tasks[self._current_task_index].copy()
            return None
    
    @property
    def is_routine_active(self) -> bool:
        """Check if a routine is currently active."""
        with self._state_lock:
            return self._is_routine_active
    
    @property
    def current_sound(self) -> Optional[str]:
        """Get the current sound to play."""
        with self._state_lock:
            return self._current_sound
    
    def start_routine(self) -> Dict[str, Any]:
        """Start the routine from the beginning."""
        with self._state_lock:
            self._is_routine_active = True
            self._current_task_index = 0
            current_task = self._tasks[self._current_task_index]
            self._current_sound = current_task["sound"]
            return current_task.copy()
    
    def next_task(self) -> Optional[Dict[str, Any]]:
        """
        Move to the next task in the routine.
        Returns the next task or None if the routine is complete.
        """
        with self._state_lock:
            if not self._is_routine_active:
                return None
                
            self._current_task_index += 1
            
            # Check if we've reached the end of the routine
            if self._current_task_index >= len(self._tasks):
                self._is_routine_active = False
                self._current_task_index = -1
                self._current_sound = None
                return None
            
            # Set the current sound to the new task's sound
            current_task = self._tasks[self._current_task_index]
            self._current_sound = current_task["sound"]
            return current_task.copy()
    
    def play_sound(self, sound_name: str) -> bool:
        """
        Set a specific sound to play.
        Returns True if the sound was set successfully.
        """
        with self._state_lock:
            self._current_sound = sound_name
            return True
    
    def stop_routine(self) -> None:
        """Stop the current routine."""
        with self._state_lock:
            self._is_routine_active = False
            self._current_task_index = -1
            self._current_sound = None

# Create a global instance that can be imported
routine_state = RoutineState()