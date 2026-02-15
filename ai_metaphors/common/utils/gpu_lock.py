import fcntl
import logging

class GPULock:
    """
    Inter-process lock based on file locking (fcntl).
    Limits simultaneous GPU usage by different Gunicorn workers.
    """
    def __init__(self, lock_file: str = "/tmp/gpu_video_gen.lock"):
        self.lock_file = lock_file
        self._fd = None

    def __enter__(self) -> 'GPULock':
        logging.info("Waiting for GPU access...")
        try:
            self._fd = open(self.lock_file, "w")
            # Lock the file. If another process already holds the lock, fcntl.flock will wait.
            fcntl.flock(self._fd, fcntl.LOCK_EX)
            logging.info("GPU access acquired.")
        except Exception as e:
            logging.error(f"Error acquiring GPU lock: {e}")
            if self._fd:
                self._fd.close()
            raise
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        try:
            if self._fd:
                fcntl.flock(self._fd, fcntl.LOCK_UN)
                self._fd.close()
                self._fd = None
            logging.info("GPU access released.")
        except Exception as e:
            logging.error(f"Error releasing GPU lock: {e}")
