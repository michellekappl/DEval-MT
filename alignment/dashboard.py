from rich.panel import Panel
from rich.console import Group
from rich.align import Align
from rich import box

# Import our custom classes - handle both relative and absolute imports
try:
    # Try relative imports first (when used as a package)
    from alignment.process_logger import ProcessLogger
    from alignment.progress_tracker import ProgressTracker
except ImportError:
    # Fall back to absolute imports (when run directly)
    from process_logger import ProcessLogger
    from progress_tracker import ProgressTracker


class Dashboard:
    """Manages the overall dashboard display.

    Shows:
    - Which translation set (by label) we're currently processing
    - Progress bars for each CPU core
    - Recent log messages from all processes
    """

    def __init__(self, total_supertasks: int, labels: list[str] | None = None):
        self.total_supertasks = total_supertasks
        self.labels = labels or [f"Set {i+1}" for i in range(total_supertasks)]

    def render(self, current_super: int, progress_tracker: ProgressTracker, logger: ProcessLogger):
        """Render the complete dashboard"""
        log_text = "\n".join(logger.get_recent_logs())
        log_panel = Panel(log_text, title="Logs", box=box.ROUNDED, padding=(1, 2))

        label = self.labels[current_super] if 0 <= current_super < len(self.labels) else f"Set {current_super+1}"
        supertask_content = Align.center(
            f"[bold yellow]Processing {label} ({current_super + 1}/{self.total_supertasks})"
        )
        supertask_panel = Panel(
            supertask_content,
            box=box.ROUNDED,
            padding=(0, 2)
        )

        return Group(
            supertask_panel,
            progress_tracker.get_progress_display(),
            log_panel
        )
