"""
Word Alignment Processing Module

This module provides tools for processing word alignments between source and target sentences
using parallel processing with a live dashboard interface.

Main components:
- AlignmentProcessor: Main class for processing alignments
- LiveDashboard: Interactive display showing progress and logs
- ProcessLogger: Manages log collection from worker processes
- ProgressTracker: Tracks progress across multiple processes
- Dashboard: Renders the overall dashboard display
"""

from .alignment_processor import AlignmentProcessor
from .live_dashboard import LiveDashboard
from .process_logger import ProcessLogger
from .progress_tracker import ProgressTracker
from .dashboard import Dashboard
from .output_capture import capture_all_output

__all__ = [
    'alignment_processor',
    'LiveDashboard', 
    'ProcessLogger',
    'ProgressTracker',
    'Dashboard',
    'capture_all_output'
]
