import time
import threading
from .base import SorterBase, VisualizeCallback

class InsertionSort(SorterBase):
    def name(self) -> str:
        return "Insertion Sort"

    def sort(self, visualize: VisualizeCallback, stop_event: threading.Event, sleep_factor: float) -> None:
        arr = self.arr
        n = len(arr)
        for i in range(1, n):
            if stop_event.is_set():
                return
            key = arr[i]
            j = i - 1
           
            visualize(arr, (i, j))
            time.sleep(sleep_factor)
            while j >= 0 and arr[j] > key:
                if stop_event.is_set():
                    return
                arr[j + 1] = arr[j]
                j -= 1
                visualize(arr, (j, j + 1))
                time.sleep(sleep_factor)
            arr[j + 1] = key
            visualize(arr, (j + 1, i))
            time.sleep(sleep_factor)