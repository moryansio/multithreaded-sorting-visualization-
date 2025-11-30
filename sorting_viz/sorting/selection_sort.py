import time
import threading
from .base import SorterBase, VisualizeCallback

class SelectionSort(SorterBase):
    def name(self) -> str:
        return "Selection Sort"

    def sort(self, visualize: VisualizeCallback, stop_event: threading.Event, sleep_factor: float) -> None:
        arr = self.arr
        n = len(arr)
        for i in range(n):
            if stop_event.is_set():
                return
            min_idx = i
            for j in range(i + 1, n):
                if stop_event.is_set():
                    return
                if arr[j] < arr[min_idx]:
                    min_idx = j
                visualize(arr, (min_idx, j))
                time.sleep(sleep_factor)
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            visualize(arr, (i, min_idx))
            time.sleep(sleep_factor)