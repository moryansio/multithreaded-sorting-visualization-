import time
import threading
from .base import SorterBase, VisualizeCallback

class QuickSort3Way(SorterBase):
    def name(self) -> str:
        return "Fast 3-way QuickSort"

    def sort(self, visualize: VisualizeCallback, stop_event: threading.Event, sleep_factor: float) -> None:
        arr = self.arr

        def qsort(lo: int, hi: int):
            if stop_event.is_set():
                return
            if hi <= lo:
                return
            lt, i, gt = lo, lo + 1, hi
            pivot = arr[lo]
            
            visualize(arr, (lo, hi))
            time.sleep(sleep_factor)
            while i <= gt:
                if stop_event.is_set():
                    return
                if arr[i] < pivot:
                    arr[lt], arr[i] = arr[i], arr[lt]
                    visualize(arr, (lt, i))
                    lt += 1
                    i += 1
                elif arr[i] > pivot:
                    arr[i], arr[gt] = arr[gt], arr[i]
                    visualize(arr, (i, gt))
                    gt -= 1
                else:
                    visualize(arr, (i, lt))
                    i += 1
                time.sleep(sleep_factor)
            qsort(lo, lt - 1)
            qsort(gt + 1, hi)

        qsort(0, len(arr) - 1)