from typing import List


class ProcessLogger:
   """
   Manages log collection and display for processes
   Keep track of which process wrote what, and only show the most recent entries.
   """
   def __init__(self, max_lines: int = 10):
      self.max_lines = max_lines  # How many log lines to keep visible
      self.log_lines = []  # List to store all the log messages
   
   def add_log(self, task_id: int, content: str):
      """Add a log entry from a specific process"""
      # Format: "[Process 0]: Loading model..." - so we know which process said what
      self.log_lines.append(f"[cyan]Process {task_id}[/cyan]: {content}")
   
   def get_recent_logs(self) -> List[str]:
      """Get the most recent log entries"""
      return self.log_lines[-self.max_lines:]
