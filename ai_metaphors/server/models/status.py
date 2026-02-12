from enum import Enum

class Status(Enum):
    queued = 'queued'
    processing = 'processing'
    completed = 'completed'
    failed = 'failed'
