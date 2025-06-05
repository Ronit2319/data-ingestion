from collections import defaultdict
from typing import Dict, List
from .models import Priority

ingestions = {}
priority_queues = {
    Priority.HIGH: [],
    Priority.MEDIUM: [],
    Priority.LOW: []
}
