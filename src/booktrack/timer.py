import time
from typing import Callable, Optional


class Timer:
    """Timer class for tracking reading sessions."""
    
    def __init__(self):
        self.start_time: Optional[float] = None
        self.elapsed_time: float = 0.0
        self.is_running: bool = False
        self.on_tick_callback: Optional[Callable[[float], None]] = None
    
    def start(self):
        """Start the timer."""
        if not self.is_running:
            self.start_time = time.time()
            self.is_running = True
    
    def stop(self) -> float:
        """Stop the timer and return elapsed time in seconds."""
        if self.is_running and self.start_time:
            self.elapsed_time += time.time() - self.start_time
            self.is_running = False
            self.start_time = None
        return self.elapsed_time
    
    def pause(self):
        """Pause the timer."""
        if self.is_running and self.start_time:
            self.elapsed_time += time.time() - self.start_time
            self.is_running = False
            self.start_time = None
    
    def resume(self):
        """Resume the timer."""
        if not self.is_running:
            self.start_time = time.time()
            self.is_running = True
    
    def reset(self):
        """Reset the timer to zero."""
        self.start_time = None
        self.elapsed_time = 0.0
        self.is_running = False
    
    def get_elapsed_time(self) -> float:
        """Get current elapsed time in seconds."""
        current_elapsed = self.elapsed_time
        if self.is_running and self.start_time:
            current_elapsed += time.time() - self.start_time
        return current_elapsed
    
    def format_time(self, seconds: Optional[float] = None) -> str:
        """Format time as HH:MM:SS."""
        if seconds is None:
            seconds = self.get_elapsed_time()
        
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)
        
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def set_on_tick_callback(self, callback: Callable[[float], None]):
        """Set a callback function to be called periodically during timing."""
        self.on_tick_callback = callback
