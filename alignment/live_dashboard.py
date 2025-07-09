from typing import List, Tuple
from rich.live import Live

# Import our custom classes - handle both relative and absolute imports
try:
    # Try relative imports first (when used as a package)
    from .process_logger import ProcessLogger
    from .progress_tracker import ProgressTracker
    from .dashboard import Dashboard
except ImportError:
    # Fall back to absolute imports (when run directly)
    from process_logger import ProcessLogger
    from progress_tracker import ProgressTracker
    from dashboard import Dashboard


class LiveDashboard:
   """
   Manages live rendering and updates of the dashboard

   Continuously updates to display progress and logs.
   It refreshes automatically every 0.5 seconds to show the latest progress.
   """
   def __init__(self, total_supertasks: int, refresh_per_second: int = 2):
      # Create all the components we need
      self.logger = ProcessLogger()              # For collecting log messages
      self.progress_tracker = ProgressTracker()  # For tracking progress bars
      self.dashboard = Dashboard(total_supertasks)  # For organizing the display
      self.current_supertask = 0  # Which translation set we're currently on
      self.live = None           # The actual "live display" object
      self.refresh_per_second = refresh_per_second  # How often to update the screen
   
   def __enter__(self):
      """Start the live dashboard (called automatically when entering 'with' block)"""
      # Create the live display and start it
      self.live = Live(
         self.dashboard.render(self.current_supertask, self.progress_tracker, self.logger),
         refresh_per_second=self.refresh_per_second
      )
      self.live.__enter__()  # Start the live display
      return self  # Return ourselves so we can be used as 'live_dashboard'
   
   def __exit__(self, exc_type, exc_val, exc_tb):
      """Stop the live dashboard (called automatically when exiting 'with' block)"""
      if self.live:
         self.live.__exit__(exc_type, exc_val, exc_tb)  # Stop the live display
   
   def setup_supertask(self, supertask_idx: int, batches: List[Tuple]):
      """Setup a new supertask with its batches"""
      self.current_supertask = supertask_idx
      self.progress_tracker.create_progress_bar(batches)  # Create progress bars for all processes
      self._update_display()  # Refresh the screen
   
   def update_progress(self, task_id: int, step: int):
      """Update progress for a specific task """
      self.progress_tracker.update_progress(task_id, step)
      self._update_display()  # Refresh the screen
   
   def add_log(self, task_id: int, content: str):
      """Add a log entry from a process"""
      self.logger.add_log(task_id, content)
      self._update_display()  # Refresh the screen
   
   def finalize_supertask(self):
      """Finalize the current supertask"""
      self._update_display()  # Final refresh of the screen
   
   def _update_display(self):
      """Internal method to update the live display (refreshes what you see on screen)"""
      if self.live:
         self.live.update(
               self.dashboard.render(self.current_supertask, self.progress_tracker, self.logger)
         )
