import tkinter as tk
from tkinter import ttk
from typing import Optional, Callable
import threading
import time



class ArrayCanvas:
    def __init__(self, parent: tk.Frame, width=600, height=180, sample=800):
        self.canvas = tk.Canvas(parent, width=width, height=height, bg="white")
        self.canvas.pack(fill="x", padx=6, pady=4)
        self.width = width
        self.height = height
        self.sample = sample  
        self.current_arr = []
        self.highlight: Optional[tuple[int, int]] = None

    def set_data(self, arr: list[int], highlight: Optional[tuple[int, int]] = None):
        self.current_arr = arr
        self.highlight = highlight
        self.draw()

    def draw(self):
        self.canvas.delete("all")
        if not self.current_arr:
            return
        arr = self.current_arr
        n = len(arr)
        
        min_v = min(arr)
        max_v = max(arr)
        rng = max(1, max_v - min_v)
        
        step = max(1, n // self.sample)
        x_step = self.width / (self.sample + 1)

        for k, i in enumerate(range(0, n, step)):
            v = arr[i]
            norm = (v - min_v) / rng
            y = self.height - norm * (self.height - 10)
            x = (k + 1) * x_step
            color = "#3b82f6"
            if self.highlight:
                a, b = self.highlight
                if i == a or i == b:
                    color = "#ef4444"
            self.canvas.create_line(x, self.height, x, y, fill=color)

class PrioritySlider(ttk.Scale):
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, from_=1, to=10, orient="horizontal", **kwargs)
        self.set(5)

    def sleep_factor(self) -> float:
        
        v = self.get()
        return 0.0005 + (v - 1) * (0.0011)

class StatusBar(ttk.Label):
    def set(self, text: str):
        self.config(text=text)

class UI:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("Real-Time Sorting Visualization")

       
        ctrl = ttk.Frame(root)
        ctrl.pack(fill="x")

        self.dataset_var = tk.StringVar(value="strict")
        ttk.Label(ctrl, text="inputs:").pack(side="left", padx=4)
        ttk.Radiobutton(ctrl, text="random", variable=self.dataset_var, value="strict").pack(side="left")
        ttk.Radiobutton(ctrl, text="«Sorted backwords»", variable=self.dataset_var, value="reverse").pack(side="left")

        self.shared_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(ctrl, text="General array (in turn)", variable=self.shared_var).pack(side="left", padx=10)

        self.start_btn = ttk.Button(ctrl, text="Start")
        self.stop_btn = ttk.Button(ctrl, text="Stop")
        self.start_btn.pack(side="right", padx=5)
        self.stop_btn.pack(side="right")

        sep = ttk.Separator(root)
        sep.pack(fill="x", pady=6)

        
        self.frames = [ttk.LabelFrame(root, text=ttl) for ttl in [
            "Stream 1 — Inserts",
            "Stream 2 — Selection",
            "Stream 3 — Quick 3-way"
        ]]
        for fr in self.frames:
            fr.pack(fill="x", padx=6, pady=2)

        self.canvases = [ArrayCanvas(fr) for fr in self.frames]

        
        self.sliders = []
        for fr in self.frames:
            row = ttk.Frame(fr)
            row.pack(fill="x")
            ttk.Label(row, text="priority:").pack(side="left", padx=6)
            slider = PrioritySlider(row)
            slider.pack(side="left", fill="x", expand=True)
            self.sliders.append(slider)

        self.status = StatusBar(root)
        self.status.pack(fill="x", padx=6, pady=4)

        
        self.on_start: Optional[Callable[[], None]] = None
        self.on_stop: Optional[Callable[[], None]] = None

        self.start_btn.config(command=self._start_clicked)
        self.stop_btn.config(command=self._stop_clicked)

    def _start_clicked(self):
        if self.on_start:
            self.on_start()

    def _stop_clicked(self):
        if self.on_stop:
            self.on_stop()

    
    def set_canvas_data(self, idx: int, arr: list[int], highlight: Optional[tuple[int, int]] = None):
        self.canvases[idx].set_data(arr, highlight)

    def set_status(self, text: str):
        self.status.set(text)