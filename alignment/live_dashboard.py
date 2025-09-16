from typing import List, Tuple
from rich.live import Live

# Import our custom classes - handle both relative and absolute imports
try:
   # Try relative imports first (when used as a package)
   from alignment.process_logger import ProcessLogger
   from alignment.progress_tracker import ProgressTracker
   from alignment.dashboard import Dashboard
except ImportError:
   # Fall back to absolute imports (when run directly)
   from process_logger import ProcessLogger
   from progress_tracker import ProgressTracker
   from dashboard import Dashboard

class LiveDashboard:
   """Manages live rendering and updates of the dashboard.

   Continuously updates to display progress and logs.
   """

   def __init__(self, total_supertasks: int, refresh_per_second: int = 2, labels: list[str] | None = None):
      self.logger = ProcessLogger()
      self.progress_tracker = ProgressTracker()
      self.dashboard = Dashboard(total_supertasks, labels=labels)
      self.current_supertask = 0
      self.live = None
      self.refresh_per_second = refresh_per_second

   def __enter__(self):
      self.live = Live(
         self.dashboard.render(self.current_supertask, self.progress_tracker, self.logger),
         refresh_per_second=self.refresh_per_second,
      )
      self.live.__enter__()
      return self

   def __exit__(self, exc_type, exc_val, exc_tb):
      if self.live:
         self.live.__exit__(exc_type, exc_val, exc_tb)

   def setup_supertask(self, supertask_idx: int, batches: List[Tuple]):
      self.current_supertask = supertask_idx
      self.progress_tracker.create_progress_bar(batches)
      self._update_display()

   def update_progress(self, task_id: int, step: int):
      self.progress_tracker.update_progress(task_id, step)
      self._update_display()

   def add_log(self, task_id: int, content: str):
      self.logger.add_log(task_id, content)
      self._update_display()

   def finalize_supertask(self):
      self._update_display()

   def _update_display(self):
      if self.live:
         self.live.update(
            self.dashboard.render(self.current_supertask, self.progress_tracker, self.logger)
         )
