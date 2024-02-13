import tracemalloc
import atexit


class MemSniff:

    def __init__(self):
        # Intialize all variables to their default by calling _reset method
        self._reset()

    def __call__(self, func):
        def wrapper_fn(*args, **kwargs):
            self.commence()
            res = func(*args, **kwargs)
            self.sniff_mem_leaks()
            self.halt()
            return res
        return wrapper_fn

    def _reset(self):
        self.tracking = False
        self.prev_snapshot = None
        self.snapshot_after = None
        self.stats = None

    def commence(self):
        if not self.tracking:
            self.tracking = True
            tracemalloc.start()
            atexit.register(tracemalloc.stop)
            self.prev_snapshot = tracemalloc.take_snapshot()

    def halt(self):
        self.tracking = False
        if self.tracking:
            tracemalloc.stop()

    def sniff_mem_leaks(self):
        if self.prev_snapshot is not None:
            self.snapshot_after = tracemalloc.take_snapshot()
            self.stats = self.snapshot_after.compare_to(
                self.prev_snapshot, 'lineno')

            if self.stats:
                print("\nDetected Memory Leaks")
                for stat in self.stats:
                    if stat.size_diff > 0:
                        traceback = stat.traceback
                        print("\tFile:", traceback[0].filename)
                        print("\tLine:", traceback[0].lineno)
                        print(
                            f"\tMemory Increase: {stat.size_diff / 1024:.2f} KiB")
