import threading
import time
import tkinter as tk
from typing import Optional

from data import generate_strict_random, generate_reverse_sorted_random
from ui import UI

from sorting.base import SorterBase
from sorting.insertion_sort import InsertionSort
from sorting.selection_sort import SelectionSort
from sorting.quicksort_3way import QuickSort3Way

N = 100_000  

class App:
    def __init__(self, root: tk.Tk):
        self.ui = UI(root)

        
        self.threads: list[threading.Thread] = []
        self.stop_event = threading.Event()
        self.lock = threading.Lock()

        
        self.ui.on_start = self.start
        self.ui.on_stop = self.stop

        
        self.base_arr: Optional[list[int]] = None

    def _generate_array(self) -> list[int]:
        dataset = self.ui.dataset_var.get()
        if dataset == "strict":
            return generate_strict_random(N)
        else:
            return generate_reverse_sorted_random(N)

    def start(self):
        self.stop_event.clear()
        self.ui.set_status("Generating array...")
        base = self._generate_array()
        self.base_arr = base

        shared = self.ui.shared_var.get()
        if shared:
            
            self.ui.set_status("General array mode: sort in sequence")
            self._run_shared_sequence(base)
        else:
            
            self.ui.set_status("Starting threads...")
            self._run_parallel(base)

    def stop(self):
        self.stop_event.set()
        self.ui.set_status("Stopping...")
        for t in self.threads:
            t.join(timeout=0.2)
        self.threads.clear()
        self.ui.set_status("Stopped.")

    
    def _visualize_to_canvas(self, idx: int):
        def cb(arr: list[int], highlight: Optional[tuple[int, int]]):
            
            self.ui.root.after(0, lambda: self.ui.set_canvas_data(idx, arr[:], highlight))
        return cb

    def _run_parallel(self, base: list[int]):
        
        sorters: list[SorterBase] = [
            InsertionSort(base[:]),
            SelectionSort(base[:]),
            QuickSort3Way(base[:]),
        ]

        
        for idx, sorter in enumerate(sorters):
            self.ui.set_canvas_data(idx, sorter.arr[:], None)

        self.threads = []
        for idx, sorter in enumerate(sorters):
            sleep_factor = self.ui.sliders[idx].sleep_factor()
            t = threading.Thread(
                target=sorter.sort,
                args=(self._visualize_to_canvas(idx), self.stop_event, sleep_factor),
                daemon=True
            )
            self.threads.append(t)
            t.start()

        self.ui.set_status("Streams are running (inserts, selection, fast 3-way).")

    def _run_shared_sequence(self, base: list[int]):
        
        idx = 0
        self.ui.set_canvas_data(idx, base[:], None)

        
        pipeline = [
            (InsertionSort, self.ui.sliders[0].sleep_factor()),
            (SelectionSort, self.ui.sliders[1].sleep_factor()),
            (QuickSort3Way, self.ui.sliders[2].sleep_factor()),
        ]

        def run_sequence():
            arr = base[:]
            for cls, sleep_factor in pipeline:
                if self.stop_event.is_set():
                    break
                sorter = cls(arr)
                sorter.sort(self._visualize_to_canvas(idx), self.stop_event, sleep_factor)
                
                self.ui.set_status(f"Stopped: {sorter.name()}")
                
                time.sleep(0.5)
                
                arr = sorter.arr

            self.ui.set_status("Shared array mode terminated.")

        t = threading.Thread(target=run_sequence, daemon=True)
        self.threads = [t]
        t.start()

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()