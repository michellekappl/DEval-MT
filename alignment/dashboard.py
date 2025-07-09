from rich.panel import Panel
from rich.console import Group
from rich.align import Align
from rich import box

# Import our custom classes - handle both relative and absolute imports
try:
    # Try relative imports first (when used as a package)
    from .process_logger import ProcessLogger
    from .progress_tracker import ProgressTracker
except ImportError:
    # Fall back to absolute imports (when run directly)
    from process_logger import ProcessLogger
    from progress_tracker import ProgressTracker


class Dashboard:
    """
    Manages the overall dashboard display
    Shows:
    - Which translation set we're currently processing
    - Progress bars for each CPU core
    - Recent log messages from all processes
    """
    def __init__(self, total_supertasks: int):
        self.total_supertasks = total_supertasks  # Total number of translation sets to process
    
    def render(self, current_super: int, progress_tracker: ProgressTracker, logger: ProcessLogger):
        """Render the complete dashboard"""
        # Get the recent log messages and put them in a nice box
        log_text = "\n".join(logger.get_recent_logs())
        log_panel = Panel(log_text, title="Logs", box=box.ROUNDED, padding=(1, 2))

        # Show which translation set we're currently working on
        supertask_content = Align.center(f"[bold yellow]Processing Translation Set {current_super + 1} of {self.total_supertasks}")
        supertask_panel = Panel(
            supertask_content,
            box=box.ROUNDED,
            padding=(0, 2)
        )

        # Combine everything into one display: title, progress bars, logs
        return Group(
            supertask_panel,              # Top: "Processing Translation Set 1 of 3"
            progress_tracker.get_progress_display(),  # Middle: Progress bars for each process
            log_panel                     # Bottom: Recent log messages
        )
