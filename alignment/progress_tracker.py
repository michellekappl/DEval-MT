from typing import List, Tuple
from rich.progress import (
    Progress, TextColumn, BarColumn, TaskProgressColumn,
    TimeRemainingColumn, TimeElapsedColumn
)

class ProgressTracker:
    """
    Manages progress tracking for multiple processes
    → multiple progress bars - one for each CPU core working on a batch of translations.
    """
    def __init__(self):
        self.progress = None  # The Rich progress bar object (starts empty)
        self.task_ids = {}    # Dictionary mapping process number to its progress bar ID
    
    def create_progress_bar(self, batches: List[Tuple]):
        """Create a progress bar for the given batches"""
        # Create a new progress display with columns showing:
        # - Process number, progress bar, completion percentage, time elapsed, time remaining
        # This progress object handles multiple tasks (one for each process) and displays one bar for each.
        self.progress = Progress(
            TextColumn("[bold]Process {task.fields[task_id]}"),  # Shows "Process 0", "Process 1", etc.
            BarColumn(),                                          # The actual progress bar
            TaskProgressColumn(),                                 # Shows "50/100 (50%)"
            TimeElapsedColumn(),                                  # How long this has been running
            TimeRemainingColumn(),                                # Estimated time left
            expand=True
        )
        
        # Create one progress bar for each batch/process
        # batch[0] is the list of sentences this process will handle
        self.task_ids = {
            i: self.progress.add_task("", task_id=i, total=len(batch[0]))
            for i, batch in enumerate(batches)
        }
    
    def update_progress(self, task_id: int, step: int):
        """Update progress for a specific task (when a process finishes a sentence)"""
        if self.progress and task_id in self.task_ids:
            # Tell the progress bar: "Process X has now completed Y sentences"
            self.progress.update(self.task_ids[task_id], completed=step)
    
    def get_progress_display(self):
        """Get the progress bar for display (or empty one if not created yet)"""
        return self.progress or Progress()
