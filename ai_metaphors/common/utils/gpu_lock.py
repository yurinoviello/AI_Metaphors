import fcntl
import logging
import time


class GPULock:
    """
    Inter-process semaphore based on multiple file locks.
    Limits simultaneous GPU usage by different Gunicorn workers to a maximum number.
    """
    def __init__(self, base_lock_file: str = "/tmp/gpu_video_gen", max_parallel: int = 4):
        self.base_lock_file = base_lock_file
        self.max_parallel = max_parallel
        self._fd = None
        self._active_slot = -1

    def __enter__(self) -> 'GPULock':
        logging.info(f"Waiting for GPU access (max parallel: {self.max_parallel})...")
        try:
            while True:
                for slot in range(self.max_parallel):
                    lock_path = f"{self.base_lock_file}_{slot}.lock"
                    fd = open(lock_path, "w")
                    try:
                        # Try to acquire a non-blocking lock
                        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                        self._fd = fd
                        self._active_slot = slot
                        logging.info(f"GPU access acquired (slot {slot}).")
                        return self
                    except BlockingIOError:
                        # Slot is busy, close and try next
                        fd.close()
                        continue
                
                # All slots are busy, wait a bit and retry
                time.sleep(5)
        except Exception as e:
            logging.error(f"Unexpected error acquiring GPU lock: {e}")
            if self._fd:
                self._fd.close()
            raise

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        try:
            if self._fd:
                fcntl.flock(self._fd, fcntl.LOCK_UN)
                self._fd.close()
                self._fd = None
                logging.info(f"GPU access released (slot {self._active_slot}).")
                self._active_slot = -1
        except Exception as e:
            logging.error(f"Error releasing GPU lock: {e}")
