"""Public API for the alignment subpackage.

Only ``AlignmentProcessor`` is exported for external users. All other
modules (dashboard, logging, progress tracking, etc.) are considered
internal implementation details and may change without notice.

Usage:
    from deval_mt.alignment import AlignmentProcessor

If you previously relied on other names from ``deval_mt.alignment``,
import them directly from their module paths (e.g.
``from deval_mt.alignment.live_dashboard import LiveDashboard``) but
be aware those are internal and not part of the stable API.
"""

from alignment.alignment_processor import AlignmentProcessor  # re-export

__all__ = ["AlignmentProcessor"]

